from typing import Dict, List, Any, Literal, Annotated, Union, Optional
from pydantic import BaseModel, Field

### TOOL ARGUMENT AND OPERATION MODELS ###

class BaseOp(BaseModel):
    id: Optional[str] = None

class sumArg(BaseModel):
    nums: List[float]
class sumOp(BaseOp):
    name: Literal["sum"]
    arguments: sumArg

class subtractArg(BaseModel):
    num_1: float
    num_2: float
class subtractOp(BaseOp):
    name: Literal["subtract"]
    arguments: subtractArg

class multiplyArg(BaseModel):
    num_1: float
    num_2: float
class multiplyOp(BaseOp):
    name: Literal["multiply"]
    arguments: multiplyArg

class divideArg(BaseModel):
    num_1: float
    num_2: float
class divideOp(BaseOp):
    name: Literal["divide"]
    arguments: divideArg

class powerArg(BaseModel):
    base: float
    exponent: float
class powerOp(BaseOp):
    name: Literal["power"]
    arguments: powerArg

class modulusArg(BaseModel):
    num_1: float
    num_2: float
class modulusOp(BaseOp):
    name: Literal["modulus"]
    arguments: modulusArg

class floorDivideArg(BaseModel):
    num_1: float
    num_2: float
class floorDivideOp(BaseOp):
    name: Literal["floor_divide"]
    arguments: floorDivideArg

class absoluteArg(BaseModel):
    num: float
class absoluteOp(BaseOp):
    name: Literal["absolute"]
    arguments: absoluteArg

class negateArg(BaseModel):
    num: float
class negateOp(BaseOp):
    name: Literal["negate"]
    arguments: negateArg

class squareArg(BaseModel):
    num: float
class squareOp(BaseOp):
    name: Literal["square"]
    arguments: squareArg

class squareRootArg(BaseModel):
    num: float
class squareRootOp(BaseOp):
    name: Literal["square_root"]
    arguments: squareRootArg

class averageArg(BaseModel):
    nums: List[float]
class averageOp(BaseOp):
    name: Literal["average"]
    arguments: averageArg

class maxValueArg(BaseModel):
    nums: List[float]
class maxValueOp(BaseOp):
    name: Literal["max_value"]
    arguments: maxValueArg

class minValueArg(BaseModel):
    nums: List[float]
class minValueOp(BaseOp):
    name: Literal["min_value"]
    arguments: minValueArg

class factorialArg(BaseModel):
    num: int
class factorialOp(BaseOp):
    name: Literal["factorial"]
    arguments: factorialArg

class complementArg(BaseModel):
    num: float
class complementOp(BaseOp):
    name: Literal["complement"]
    arguments: complementArg

### Batch Operation Models
BatchOp = Annotated[Union[sumOp, subtractOp, multiplyOp, divideOp, powerOp, modulusOp, floorDivideOp, absoluteOp, negateOp, squareOp, squareRootOp, averageOp, maxValueOp, minValueOp, factorialOp, complementOp], Field(discriminator="name")]
class BatchRequest(BaseModel):
    mode: Literal["parallel", "sequential"] = "parallel"
    break_on_error: bool = True
    ops: list[BatchOp]

class BatchItemResult(BaseModel):
    id: Optional[str] = None
    name: str
    ok: bool
    result: Optional[Any] = None
    error: Optional[str] = None
class BatchResponse(BaseModel):
    mode: str
    results: List[BatchItemResult]