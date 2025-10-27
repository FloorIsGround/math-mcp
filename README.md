
# math-operations-mcp

Short instructions to install dependencies and run the project.

Prerequisites
- Python 3.11+ (project pyproject requires >=3.11; use your system Python or a virtualenv)

Create a virtual environment and install dependencies

With python:
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
# If the project has no local installable package, install the runtime deps directly:
# pip install fastapi uvicorn pydantic
```

With uv package manager:
```bash
# install uv if needed
pip install uv

# create (and usually activate) a virtual environment
uv venv

# If uv does not activate the venv automatically, activate it manually:
# Linux/WSL:
source .venv/bin/activate

# upgrade pip and install the project
uv sync

# If the project has no local installable package, install runtime deps directly:
# pip install fastapi uvicorn pydantic
```

Run the server

```bash
# run directly with python
python main.py

#with uv package manager

uv run main.py
```

What to expect
- The API root will be available at http://localhost:8000/
- The MCP endpoint is mounted at /math/mcp/ (see `main.py`) and a streaming HTTP app at /math/

Notes
- If you run into dependency issues, check the `pyproject.toml` in the repository root and install listed packages manually.


README.md created with Generative AI.
