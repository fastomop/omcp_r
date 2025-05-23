import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to the Docker container's MCP server
    async with sse_client("http://localhost:8000") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {len(tools.tools)}")
            print(f"Tool name: {tools.tools[0].name}")
            
            # Example Python code to run
            code = """
import numpy as np
import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

print("DataFrame created:")
print(df)

# Return the sum of all values
df.values.sum()
"""
            
            # Call the run_python_code tool
            result = await session.call_tool('run_python_code', {'python_code': code})
            print("\nResult from MCP server:")
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
