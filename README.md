
# math-operations-mcp (mcp-server-3)

Short instructions to install dependencies and run the project.

Prerequisites
- Python 3.11+ (project pyproject requires >=3.11; use your system Python or a virtualenv)

Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
# If the project has no local installable package, install the runtime deps directly:
# pip install fastapi uvicorn pydantic
```

Run the server

```bash
# start with uvicorn (recommended for development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# or run directly with python
python main.py
```

What to expect
- The API root will be available at http://localhost:8000/
- The MCP endpoint is mounted at /math/mcp/ (see `main.py`) and a streaming HTTP app at /math/

Notes
- If you run into dependency issues, check the `pyproject.toml` in the repository root and install listed packages manually.
- On production, run with a process manager (systemd, gunicorn with uvicorn workers, or docker).

