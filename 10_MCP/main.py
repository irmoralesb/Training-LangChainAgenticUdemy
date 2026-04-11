import asyncio
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent


CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")


llm = ChatOpenAI()

stdio_server_params = StdioServerParameters(
    command="python",
    args=[f"{CURRENT_DIRECTORY}/servers/math_server.py"],
)


async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            # tools = await session.list_tools()
            tools = await load_mcp_tools(session)
            print("tools loaded")
            agent = create_agent(llm, tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
