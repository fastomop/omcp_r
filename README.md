# OMOP MCP Server

A Python sandbox server for the Observational Medical Outcomes Partnership (OMOP) Common Data Model. This project provides a controlled environment for executing and validating protocols, highlighting the use of UV to enhance performance.

## Overview

The OMOP MCP Server allows you to:
- Execute Python code in an isolated environment.
- Capture and manage outputs and errors.
- Leverage UV for efficient asynchronous operations.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- (Optional) A virtual environment tool (recommended)

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

   > **Note:** If UV is not already included in `requirements.txt`, install it separately using:
   >
   > ```sh
   > pip install uv
   > ```

## Running the Server

To run the server using UV, use the following command (adjust the entry point as needed):

```sh
uv --app omcp_py:app --reload
```

This command tells UV to start the application defined in the `omcp_py` module with auto-reload enabled.

## Documentation

Project documentation is managed through MkDocs. To serve the documentation locally, run:

```sh
mkdocs serve
```

Then open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Contributing

Contributions are welcome! If you find an issue or have suggestions for improvement, please open an issue or a pull request.

## License

This project is licensed under the MIT License.