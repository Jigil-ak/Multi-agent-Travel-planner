import os
import asyncio
import certifi
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq


os.environ["SSL_CERT_FILE"]=certifi.where()
os.environ["REQUESTS_CA_BUNDLE"]=certifi.where()

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


client = MultiServerMCPClient(
    {
        "tavily":{
            "transport":"streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },

        "aviationstack": {
            "transport" : "stdio",
            "command": "uvx",
            "args": [
            "aviationstack-mcp"
                 ],
            "env": {
            "AVIATIONSTACK_API_KEY": AVIATIONSTACK_API_KEY,
        }
    }
    }
)

#check if the client is connected to all servers
async def get_all_tools():
    tools = await client.get_tools()
    print("\nAvailable MCP Tools:\n")
    
    for tool in tools:
        print(tool.name)



#tavily and aviation tools

search_tool = None
aviation_tools = {}
async def intelligence_mcp9():

    global search_tool
    global aviation_tools

    if search_tool is not None and aviation_tools:
        return

    tools = await client.get_tools()

    print("nAvailable MCP tools:\n")

    for tool in tools:
        print(tool.name)

    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )    

    aviation_tools = next(
        tool.name: tool
        for tool in tools
        if tool.name !="tavily_search"
    )



async def tavily_mcp_search(query: str):
    await initialize_mcp()
    result = await search_tool.ainvoke(
        {
            "query": query
            }
        )
    return result



#which tool will use in aviation stack    

async def aviation_mcp_call(
        tool_name: str,
        tool_args: dict = None
):

    tools = await client.get_tools()

    tool = next(
        t for t in tools
        if t.name == tool_name
    )

    result = await tool.ainvoke(
        tool_args or {}
    )

    return result


