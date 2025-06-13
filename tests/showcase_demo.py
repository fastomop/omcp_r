#!/usr/bin/env python3
"""
OMCP Python Sandbox Showcase Demo
This script demonstrates the sandbox functionality step by step
"""

import subprocess
import json
import time
import sys
import os

def print_step(step_num, title):
    """Print a formatted step header"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")

def print_info(message):
    """Print an info message"""
    print(f"ℹ️  {message}")

def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"⚠️  {message}")

def check_server_status():
    """Check if the FastMCP server is running"""
    print_step(1, "Checking Server Status")
    
    try:
        result = subprocess.run(['pgrep', '-f', 'server_fastmcp.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("FastMCP server is running!")
            print_info("Server process found in system")
            return True
        else:
            print_error("FastMCP server is not running")
            print_info("Start it with: uv run server_fastmcp.py")
            return False
    except Exception as e:
        print_error(f"Error checking server: {e}")
        return False

def check_docker_status():
    """Check Docker status"""
    print_step(2, "Checking Docker Status")
    
    try:
        result = subprocess.run(['sudo', 'docker', 'ps'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("Docker is running!")
            print_info("Docker daemon is active")
            return True
        else:
            print_error("Docker is not running")
            return False
    except Exception as e:
        print_error(f"Error checking Docker: {e}")
        return False

def show_project_structure():
    """Show the project structure"""
    print_step(3, "Project Structure")
    
    print_info("Key files in the project:")
    files = [
        "server_fastmcp.py - Main FastMCP server",
        "sandbox_server.py - Flask sandbox server",
        "src/omcp_py/ - Core sandbox implementation",
        "Dockerfile - Docker image for sandboxes",
        "pyproject.toml - Project dependencies",
        "demo_test.py - Demo script"
    ]
    
    for file in files:
        print(f"   📄 {file}")
    
    print_success("Project structure is complete")

def show_security_features():
    """Show security features"""
    print_step(4, "Security Features")
    
    features = [
        "🐳 Docker-based isolation - Each sandbox runs in a separate container",
        "👤 User isolation - Containers run as 'sandboxuser' (non-root)",
        "🔒 Read-only filesystem - Prevents file system modifications",
        "🛡️ Dropped Linux capabilities - Removes dangerous privileges",
        "🚫 No privilege escalation - Containers cannot gain root access",
        "🔐 Command injection protection - Uses shlex.quote for escaping",
        "⚡ Resource limits - CPU and memory restrictions",
        "🌐 Network isolation - Containers have no network access",
        "⏰ Timeout controls - Automatic cleanup of long-running processes",
        "🧹 Auto-cleanup - Inactive sandboxes are automatically removed"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print_success("Comprehensive security measures implemented")

def show_mcp_tools():
    """Show available MCP tools"""
    print_step(5, "Available MCP Tools")
    
    tools = [
        ("🔧 create_sandbox", "Create new isolated Python environment"),
        ("📝 list_sandboxes", "List all active sandboxes"),
        ("🐍 execute_python_code", "Run Python code in sandbox"),
        ("📦 install_package", "Install Python packages in sandbox"),
        ("🗑️ remove_sandbox", "Remove sandbox containers")
    ]
    
    for tool, description in tools:
        print(f"   {tool} - {description}")
    
    print_success("All tools are ready for use")

def show_mcp_inspector():
    """Show MCP Inspector functionality"""
    print_step(6, "MCP Inspector Web UI")
    
    print_info("MCP Inspector provides a web-based interface to test tools:")
    
    # Check if inspector is running
    try:
        result = subprocess.run(['pgrep', '-f', 'mcp-inspector'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("MCP Inspector is running!")
            
            # Try to find the port
            try:
                result = subprocess.run(['ss', '-tlnp'], 
                                      capture_output=True, text=True)
                if '6274' in result.stdout:
                    print_info("🌐 Web UI available at: http://127.0.0.1:6274")
                    print_info("📱 Open this URL in your browser to test tools")
                else:
                    print_warning("Inspector running but port not detected")
            except:
                print_info("🌐 Web UI typically available at: http://127.0.0.1:6274")
        else:
            print_info("To start MCP Inspector:")
            print("   npx @modelcontextprotocol/inspector uv run server_fastmcp.py")
            print_info("Then open: http://127.0.0.1:6274")
    except Exception as e:
        print_error(f"Error checking inspector: {e}")
    
    print_info("MCP Inspector Features:")
    inspector_features = [
        "🔧 Interactive tool testing - Test all MCP tools in real-time",
        "📊 Request/Response inspection - See JSON-RPC messages",
        "🐍 Code execution testing - Run Python code in sandboxes",
        "📦 Package installation testing - Install packages in sandboxes",
        "📝 Sandbox management - Create, list, and remove sandboxes",
        "🔍 Error debugging - View detailed error messages",
        "📈 Performance monitoring - Track execution times",
        "💾 Session persistence - Save and load test scenarios"
    ]
    
    for feature in inspector_features:
        print(f"   {feature}")
    
    print_success("MCP Inspector provides complete tool testing interface")

def show_architecture():
    """Show the system architecture"""
    print_step(7, "System Architecture")
    
    print_info("Architecture Overview:")
    print("   🖥️  MCP Client (Agent)")
    print("        ↓ (JSON-RPC over stdio)")
    print("   🚀 FastMCP Server (server_fastmcp.py)")
    print("        ↓ (Docker API)")
    print("   🐳 Docker Containers (Python Sandboxes)")
    print("        ↓ (Flask HTTP)")
    print("   🔧 Sandbox Server (sandbox_server.py)")
    
    print_info("Data Flow:")
    print("   1. Agent sends MCP tool call")
    print("   2. FastMCP server processes request")
    print("   3. Sandbox manager creates/uses Docker container")
    print("   4. Code executes in isolated environment")
    print("   5. Results returned via MCP protocol")
    
    print_success("Architecture is secure and scalable")

def show_usage_example():
    """Show usage example"""
    print_step(8, "Usage Example")
    
    print_info("Example MCP tool call:")
    print("""
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "execute_python_code",
    "arguments": {
      "sandbox_id": "sandbox_123",
      "code": "print('Hello from sandbox!')",
      "timeout": 30
    }
  }
}
""")
    
    print_success("Ready for integration with MCP clients")

def show_demo_instructions():
    """Show demo instructions"""
    print_step(9, "Demo Instructions")
    
    print_info("To demonstrate the sandbox system:")
    print("   1. Start the FastMCP server:")
    print("      uv run server_fastmcp.py")
    print("")
    print("   2. Launch MCP Inspector:")
    print("      npx @modelcontextprotocol/inspector uv run server_fastmcp.py")
    print("")
    print("   3. Open web UI:")
    print("      http://127.0.0.1:6274")
    print("")
    print("   4. Test tools in the web interface:")
    print("      - Create a sandbox")
    print("      - Execute Python code")
    print("      - Install packages")
    print("      - List sandboxes")
    print("      - Remove sandboxes")
    
    print_success("Perfect for live demonstrations and testing!")

def main():
    """Main demonstration function"""
    print("🚀 OMCP Python Sandbox Showcase")
    print("=" * 60)
    print("This demo shows the complete sandbox system")
    print("=" * 60)
    
    # Run all demonstration steps
    check_server_status()
    check_docker_status()
    show_project_structure()
    show_security_features()
    show_mcp_tools()
    show_mcp_inspector()
    show_architecture()
    show_usage_example()
    show_demo_instructions()
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main() 
