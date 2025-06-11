---
title: Travel Documentation MCP Server
emoji: 🌴
sdk: gradio
sdk_version: 5.33.0
app_file: travel_mcp_server.py
pinned: false
short_description: MCP hackathon 2025
---

# Travel Documentation MCP Server

> An AI-powered travel documentation assistant built with Gradio's MCP server capabilities and smolagents for the Hugging Face MCP Hackathon 2025.

## What This Project Does

This project creates an intelligent travel documentation agent that helps travelers understand what documents they need for international trips. It consists of:

1. **MCP Server** (`travel_mcp_server.py`) - A Gradio interface that exposes travel documentation analysis as an MCP tool, mocking data is used for demonstration
2. **MCP Client** (`travel_mcp_client.py`) - An AI agent that uses smolagents to interact with the MCP server and provide conversational assistance


## Technical Implementation
- **Gradio MCP Server**: Uses Gradio's built-in MCP server functionality
- **smolagents Integration**: AI agent framework for tool execution and conversation
- **Local LLM Support**: Uses Ollama for local AI inference

## Installation & Setup

### Prerequisites
- Python 3.8+
- Ollama (for local LLM)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Ollama (for the AI agent)
```bash
# Install Ollama from https://ollama.ai
# Pull the required model
ollama pull gemma3:4b
```

### 3. Start the MCP Server
```bash
python travel_mcp_server.py
```
The server will start at `http://127.0.0.1:7861` with MCP endpoint at `http://127.0.0.1:7861/gradio_api/mcp/sse`

### 4. Start the AI Agent Client
```bash
python travel_mcp_client.py
```

## Usage

### Direct Web Interface
Visit `http://127.0.0.1:7861` to use the travel documentation tool directly:

**Input Parameters:**
- **Your Citizenship Country**: e.g., "Canada", "China", "India"
- **Destination Country**: e.g., "Japan", "USA", "Germany"
- **Trip Duration**: Number of days (1-365)
- **Trip Purpose**: tourism, business, study, transit, work, family visit

**Example Output:**
```json
{
  "trip_info": {
    "from_country": "Canada",
    "to_country": "Japan",
    "duration_days": 30,
    "purpose": "Tourism"
  },
  "visa_requirements": {
    "visa_required": false,
    "max_stay": "90 days"
  },
  "required_documents": [
    {
      "document_type": "Passport",
      "required": true,
      "description": "Valid passport with at least 6 months validity remaining"
    }
  ],
  "summary": {
    "required_count": 5,
    "optional_count": 1,
    "visa_needed": false
  }
}
```

### AI Agent Chat Interface
Use the conversational agent for natural language queries:

**Example Conversations:**
```
User: "I'm a Canadian citizen planning to visit Japan for 2 weeks for tourism"
Agent: "..."

User: "What documents do I need for business travel from China to USA?"
Agent: "..."
```
