from typing import Any, Dict

from langchain_core.documents import Document
from langchain_tavily import TavilySearch

from graph.state import GraphState
from dotenv import load_dotenv
from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")

web_search_tool = TavilySearch(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]

    tavily_results = web_search_tool.invoke({"query": question})

    # Tavily response format can vary by version:
    # - list[dict] with "content"
    # - dict with "results": list[dict]
    # - string
    results_list = tavily_results.get("results", []) if isinstance(tavily_results, dict) else tavily_results
    if isinstance(results_list, list):
        joined_tavily_result = "\n".join(
            result.get("content", str(result)) if isinstance(result, dict) else str(result)
            for result in results_list
        )
    else:
        joined_tavily_result = str(results_list)

    web_results = Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}


if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": None})