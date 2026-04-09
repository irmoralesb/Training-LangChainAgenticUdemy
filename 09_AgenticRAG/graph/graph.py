from pathlib import Path
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.consts import *
from graph.state import GraphState


CURRENT_DIRECTORY = Path(__file__).resolve().parent
ROOT = CURRENT_DIRECTORY.parent
load_dotenv(ROOT / ".env")

from graph.nodes import generate, grade_documents, retrieve, web_search


def decide_to_generate(state):
    print("---ASSESS GRADE DOCUMENTS---")
    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE---"
        )
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    path_map={
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    }
)

workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")