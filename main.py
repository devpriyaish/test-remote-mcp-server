import json
import random 

from fastmcp import FastMCP


# Create the FastMCP server instance
mcp = FastMCP("Simple Calculator Server")

# Tool: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Tool: Add two numbers
    Parameters:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The sum of the two numbers
    """
    return a + b

# Tool: Generate a random number
@mcp.tool()
def random_number(min_val: int=1, max_val: int=100) -> int:
    """
    Tool: Generate a random number
    Parameters:
        min_val (int): The minimum value of the random number
        max_val (int): The maximum value of the random number
    Returns:
        int: A random number between min_val and max_val
    """
    return random.randint(min_val, max_val)

# Resource: Server Information
@mcp.resource("info://server")
def server_info() -> str:
    """
    Resource: Server Information
    Returns:
        str: A JSON string containing information about the server
    """
    info = {
        "name": "Simple Calculator Server",
        "description": "A simple calculator server",
        "version": "1.0",
        "tools": ["add", "random_number"],
        "author": "John Doe"
    }
    return json.dumps(info, indent=2)

# Start ther server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)