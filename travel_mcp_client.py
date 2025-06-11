import gradio as gr

from smolagents import CodeAgent, tool, LiteLLMModel
from smolagents.mcp_client import MCPClient

@tool
def self_introduction() -> str:
    """
    Provides information about the agent's identity and capabilities.
    
    This tool should be triggered when the user asks questions like:
    - "What's your name?"
    - "Who are you?"
    - "What can you do?"
    - "Tell me about yourself"
    - "What are your capabilities?"
    - Any other introductory or identity-related queries
    
    Returns:
        str: A friendly introduction explaining the agent's purpose and capabilities. You are free to rewrite the introduction but need to keep the same meaning.
    """
    return "Hello! I am your travel documentation Agent. I can help you find out what documetations are required for your trip, get me your original coutry, destionation country, trip duration and purpose and I can help you."


mcp_client = MCPClient(
        {"url": "http://127.0.0.1:7861/gradio_api/mcp/sse"}
    )

try:
    tools = mcp_client.get_tools()

    # for local testing
    model = LiteLLMModel(
        model_id="ollama_chat/gemma3:4b",
        api_base="http://127.0.0.1:11434",
        num_ctx=8192,
    )
    agent = CodeAgent(tools=[*tools], model=model)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=["Your trip plan..."],
        title="Travel documentation agent",
        description="This is a simple agent that uses MCP tools to help you find out required documentations for your international trip.",
    )

    demo.launch()
finally:
    mcp_client.disconnect()