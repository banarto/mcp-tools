from mcp.server import MCPServer
from datetime import datetime

mcp = MCPServer("clock")

@mcp.tool()
def get_current_time() -> str:
    return f"現在の時刻：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

if __name__ == "__main__":
    mcp.run()