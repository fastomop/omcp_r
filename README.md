# OMOP MCP Server

A Python sandbox server for the Observational Medical Outcomes Partnership (OMOP) Common Data Model. This project provides a controlled environment for executing and validating protocols, highlighting the use of UV for enhanced performance. It also offers a Docker-based deployment option using Deno to run an SSE server for asynchronous tool execution.

## Overview

The OMOP MCP Server allows you to:
- Execute Python code in an isolated environment.
- Capture and manage outputs and errors.
- Leverage UV for efficient asynchronous operations.
- Run commands via a Docker container with an SSE interface.

## Code Structure

- **Server Initialization (`server.py`):**  
  Sets up the MCP server with one or more tools (such as `RunPythonTool`) that execute Python code safely. The server is launched using a stdio interface or can be connected via SSE when deployed in Docker.

- **Tool Implementation:**  
  Tools (located in the tools directory) wrap functionality such as executing Python code in a sandboxed environment and capturing outputs.

- **Python Execution Utility (`omcp_py/utils/omcp_py.py`):**  
  Provides a function to execute arbitrary Python code, capturing stdout, stderr, and any exceptions.

- **Docker Integration:**  
  The project includes a Dockerfile and a docker-compose.yml for containerizing the SSE server. The Docker image is built using Deno and runs the `mcp-run-python` command to serve on port **8000**.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- (Optional) A virtual environment tool (recommended)
- Docker (if using the containerized setup)

### External Dependencies

In addition to the Python dependencies listed in `requirements.txt`, the sandbox depends on some external tools:
- **Docker:** Used to containerize the SSE server.  
  [Docker Installation Guide](https://docs.docker.com/get-docker/)
- **Deno:** The Deno runtime is required to run the `mcp-run-python` module via npm.  
  [Deno Installation Guide](https://deno.land/#installation)
- **Pyodide:** Loaded by Deno via npm as part of the `jsr:@pydantic/mcp-run-python` module. No separate installation is required.

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/fastomop/omcp_py.git
   cd omcp_py
   ```

2. **Create and activate a virtual environment (recommended):**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   > **Note:** If UV is not already in `requirements.txt`, install it separately:
   >
   > ```sh
   > pip install uv
   > ```

## Running the Server Locally

To run the server using UV (with auto-reload) or directly via Python, use one of the following commands:

- **Using UV:**

  ```sh
  uv --app omcp_py:app --reload
  ```

- **Directly with Python:**

  ```sh
  python server.py
  ```

## Docker Setup

### Using Docker Directly

1. **Build the Docker Image:**

   ```sh
   docker build -t mcp-run-python .
   ```

2. **Run the Docker Container:**

   ```sh
   docker run -p 8000:8000 mcp-run-python
   ```

### Using Docker Compose

You can also leverage the provided `docker-compose.yml` to build and run the container:

```sh
docker-compose up --build
```

This starts the container with port **8000** exposed and mounts the volume for `node_modules`.

## Documentation

Project documentation is managed with MkDocs and the Material theme. To serve the documentation locally, run:

```sh
mkdocs serve
```

Then, open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.