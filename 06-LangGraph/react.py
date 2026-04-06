from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_tavily import TavilySearch


load_dotenv()

@tool
def triple(num: float) -> float:
    """
    Multiply the given number by 3 and return the result.

    Args:
        num (float): The number to be tripled.

    Returns:
        float: The tripled value.
    """
    return float(num) * 3


tools = [TavilySearch(max_results=1), triple]

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0).bind_tools(tools)
