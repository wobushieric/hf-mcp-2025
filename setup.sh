#!/bin/bash
# Setup script for Travel Documentation MCP Server

echo "Setting up Travel Documentation MCP Server"
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt


echo "Setup complete!"
echo ""
echo "To run the applications:"
echo "  MCP Server: python travel_mcp_server.py"
echo "  MCP Client with Agent: python travel_mcp_client.py"
echo ""
echo "Access the web interface at: http://127.0.0.1:7860"
