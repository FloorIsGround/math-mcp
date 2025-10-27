from mcp.server.fastmcp import FastMCP, Context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from dotenv import load_dotenv
load_dotenv()

from pydantic_models import (
    BatchOp,
    BatchRequest,
    BatchItemResult,
    BatchResponse,
)
from middleware.auth import VerifyAuthenticationMiddleware
from middleware.proc import AddProcessTimeHeaderMiddleware


mcp = FastMCP("math-operations", stateless_http=True)




@mcp.tool()
async def sum(nums: List[float]) -> float:
    total = 0
    for num in nums:
        total += num
    return total

@mcp.tool()
async def subtract(num_1: float, num_2: float) -> float:
    return num_1 - num_2

@mcp.tool()
async def multiply(num_1: float, num_2: float) -> float:
    return num_1 * num_2

@mcp.tool()
async def divide(num_1: float, num_2: float) -> float:
    if num_2 == 0:
        raise ValueError("Division by zero is not allowed.")
    return num_1 / num_2

@mcp.tool()
async def power(base: float, exponent: float) -> float:
    return base ** exponent


@mcp.tool()
async def modulus(num_1: float, num_2: float) -> float:
    return num_1 % num_2


@mcp.tool()
async def floor_divide(num_1: float, num_2: float) -> float:
    return num_1 // num_2

@mcp.tool()
async def absolute(num: float) -> float:
    return abs(num)

@mcp.tool()
async def negate(num: float) -> float:
    return -num

@mcp.tool()
async def square(num: float) -> float:
    return num * num

@mcp.tool()
async def square_root(num: float) -> float:
    if num < 0:
        raise ValueError("Square root of negative number is not allowed.")
    return num ** 0.5

@mcp.tool()
async def average(nums: List[float]) -> float:
    if not nums:
        raise ValueError("The list is empty.")
    return float(await sum(nums)) / float(len(nums))

@mcp.tool()
async def max_value(nums: List[float]) -> float:
    if not nums:
        raise ValueError("The list is empty.")
    return max(nums)

@mcp.tool()
async def min_value(nums: List[float]) -> float:
    if not nums:
        raise ValueError("The list is empty.")
    return min(nums)

@mcp.tool()
async def factorial(num: int) -> int:
    if num < 0:
        raise ValueError("Factorial of negative number is not allowed.")
    result = 1
    for i in range(2, num + 1):
        result *= i
    return result

@mcp.tool()
async def complement(num: float) -> float:
    return 1 - num


### Batch Tooling
async def _run_one(idx: int, op: BatchOp) -> BatchItemResult:
    try:
        if op.name == "sum":
            out = await sum(**op.arguments.model_dump())
        elif op.name == "subtract":
            out = await subtract(**op.arguments.model_dump())
        elif op.name == "multiply":
            out = await multiply(**op.arguments.model_dump())
        elif op.name == "divide":
            out = await divide(**op.arguments.model_dump())
        elif op.name == "power":
            out = await power(**op.arguments.model_dump())
        elif op.name == "modulus":
            out = await modulus(**op.arguments.model_dump())
        elif op.name == "floor_divide":
            out = await floor_divide(**op.arguments.model_dump())
        elif op.name == "absolute":
            out = await absolute(**op.arguments.model_dump())
        elif op.name == "negate":
            out = await negate(**op.arguments.model_dump())
        elif op.name == "square":
            out = await square(**op.arguments.model_dump())
        elif op.name == "square_root":
            out = await square_root(**op.arguments.model_dump())
        elif op.name == "average":
            out = await average(**op.arguments.model_dump())
        elif op.name == "max_value":
            out = await max_value(**op.arguments.model_dump())
        elif op.name == "min_value":
            out = await min_value(**op.arguments.model_dump())
        elif op.name == "factorial":
            out = await factorial(**op.arguments.model_dump())
        elif op.name == "complement":
            out = await complement(**op.arguments.model_dump())
        else:
            return ValueError(f"Unknown operation: {op.name}")
        return BatchItemResult(id=op.id or str(idx), name=op.name, ok=True, result=out)
    except Exception as e:
        return BatchItemResult(id=op.id or str(idx), name=op.name, ok=False, error=str(e))
    
@mcp.tool(
    name="batch",
    description=(
        "Run multiple tools in one call. Use when you need several actions at once.\n"
        "Input:\n"
        "{\n"
        '  "mode": "parallel" | "sequential",\n'
        '  "ops": [\n'
        '    {"name":"sum","arguments":{"nums": [1.0,2.0,3.0,4.0]},"id":"sum1"},\n'
        '    {"name":"subtract","arguments":{"num_1": 5.0, "num_2": 1.0}}\n'
        "  ]\n"
        "}\n"
        "Returns results in the same order; each item has {id?, name, ok, result?, error?}."
    ),
    annotations={"idempotentHint": True}
)
async def batch(req: BatchRequest, ctx: Context) -> BatchResponse:
    results: List[BatchItemResult] = []
    if req.mode == "parallel":
        import asyncio
        tasks = []
        for idx, op in enumerate(req.ops):
            tasks.append(_run_one(idx, op))
        completed = await asyncio.gather(*tasks)
        for res in completed:
            results.append(res)
    else:  # sequential
        for idx, op in enumerate(req.ops):
            res = await _run_one(idx, op)
            results.append(res)
            if not res.ok and req.break_on_error:
                break
    return BatchResponse(mode=req.mode, results=results)

### FastAPI App Setup
app = FastAPI(lifespan=lambda _app: mcp.session_manager.run())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],  
)
app.add_middleware(VerifyAuthenticationMiddleware)
app.add_middleware(AddProcessTimeHeaderMiddleware)

app.mount("/math", mcp.streamable_http_app())

@app.get("/")
def root():
    return {"ok": True, "name": "math-operations-mcp", "mcp_endpoint": "/math/mcp/"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
