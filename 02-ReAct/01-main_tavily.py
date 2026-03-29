from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


tavily = TavilyClient()


def get_chat_llm(provider_name: str, **kwargs) -> BaseChatModel:

    factories = {
        "openai": lambda: ChatOpenAI(model="gpt-4o-mini", **kwargs),
        # "openai": lambda: ChatOpenAI(model="gpt-5", **kwargs),
        "anthropic": lambda: ChatAnthropic(model="claude-haiku-4-5", **kwargs),
        # "ollama": lambda : ChatOllama (model="gemma3:270m", **kwargs),
        "ollama": lambda: ChatOllama(model="gpt-oss:20b", **kwargs),
        # "ollama": lambda : ChatOllama (model="qwen3:1.7b", **kwargs),
    }

    return factories[provider_name]()


@tool
def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: The query to search for
    Returns:
        The search result
    """
    return tavily.search(query=query)


llm = get_chat_llm("openai", temperature=0)
tools = [search]
agent = create_agent(model=llm, tools=tools)


def main():
    print("Hello ReAct")

    # query = "What is the weather in Tokyo?"
    query = "search for 3 job posting for an ai engineer using langchain in the bay area on linkedin and list their details"

    result = agent.invoke({"messages": HumanMessage(content=query)})
    print(result)


if __name__ == "__main__":
    main()
