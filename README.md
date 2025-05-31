# OMCP Python Sandbox Server

A simple, safe, and sandboxed Python code execution environment for MCP servers. This project uses a Dockerized Python HTTP server as a sandbox, and a Python MCP proxy that communicates with it.

---

## Features
- **Sandboxed Python execution** via Docker
- **HTTP API** for code execution
- **Easy integration** with MCP via a Python proxy
- **Fast Python workflow** using [uv](https://github.com/astral-sh/uv)

---

## Prerequisites

- **Python 3.8+** (for MCP server and uv)
- **Docker** (for sandboxed code execution)
- **uv** (for fast Python dependency management and running scripts)
- **git** (to clone the repository)

---

## 1. Clone the Repository
```sh
git clone https://github.com/fastomop/omcp_py.git
cd omcp_py
```

---

## 2. Install Docker
- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- Make sure Docker is running:
  ```sh
  docker --version
  ```

---

## 3. Install uv (if not already installed)
- Install with pip:
  ```sh
  pip install uv
  ```
- Or with pipx (recommended):
  ```sh
  pipx install uv
  ```
- Check uv is installed:
  ```sh
  uv --version
  ```

---

## 4. Build and Run the Python Sandbox Server (Docker)
This server runs in a container and exposes `/run` for code execution.

```sh
docker build -t python-sandbox-server .
docker run -p 8000:8000 python-sandbox-server
```
- The server will be available at `http://localhost:8000/run`.
- Leave this terminal running.

---

## 5. Install Python Dependencies with uv
In a new terminal, from your project directory:
```sh
uv pip install -r requirements.txt
```

---

## 6. Run the MCP Python Server
```sh
uv run server.py
```
- The MCP server will now proxy all Python code execution requests to the sandbox server via HTTP.

---

## 7. Test the Sandbox Server Directly
You can test the sandbox server with curl:
```sh
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" -d '{"code": "print(1+1)\n2+2"}'
```
Response:
```json
{"result": 4, "output": "2\n", "error": null}
```

---

## Project Structure
```
.
├── server.py            # MCP Python proxy server
├── sandbox_server.py    # Flask-based Python sandbox HTTP server
├── Dockerfile           # Builds the sandbox server
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── ...
```

---

## Development & Customization
- Use `uv` for all Python dependency management and running scripts.
- Use Docker for sandbox isolation.
- You can add more endpoints or security to `sandbox_server.py` as needed.
- To update dependencies, edit `requirements.txt` and run `uv pip install -r requirements.txt` again.

---

## Troubleshooting
- **Docker build fails:** Make sure Docker is installed and running. Try `docker system prune` if you have disk space issues.
- **uv not found:** Make sure you installed uv and your PATH is set correctly.
- **Python module errors:** Ensure you installed all dependencies with `uv pip install -r requirements.txt`.
- **Port conflicts:** Make sure nothing else is running on port 8000.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

---

## FAQ

**Q: Is the sandbox server secure?**
A: The server runs in Docker and restricts code to a namespace, but for production, consider additional Docker resource limits and security measures.

**Q: Can I use a different port?**
A: Yes, change the port in `sandbox_server.py` and update the Docker run command accordingly.

**Q: How do I add more Python packages to the sandbox?**
A: Edit the Dockerfile to install more packages with pip, then rebuild the image.

---

## License
MIT