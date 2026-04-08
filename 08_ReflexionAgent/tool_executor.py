from dotenv import load_dotenv
from pathlib import Path
from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from schemas import AnswerQuestion, ReviseAnswer


CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")

tavily_tool = TavilySearch(max_results=5)


def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries"""
    return tavily_tool.batch([{"query": query} for query in search_queries])


execute_tools = ToolNode(
    [
        StructuredTool.from_function(
            run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)
