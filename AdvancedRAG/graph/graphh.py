from dotenv import load_dotenv
import os

from langgraph.graph import END, START, StateGraph

from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.router import question_router, RouteQuery
from graph.node_constants import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import GraphState


load_dotenv()
def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return "web_search_node"
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # Invoke hallucination grader and handle score
    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"


def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return "web_search_node"
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE
    else:
        print("---DEFAULT ROUTE TO RETRIEVE---")
        return RETRIEVE  # Varsayılan düğüm

workflow = StateGraph(GraphState)

# Set initial state and entry point
initial_state = {
    "question": None,
    "documents": [],
    "generation": None,
    "web_search": False,
    "__start__": True,
}
workflow.set_entry_point(RETRIEVE)
workflow.initial_state = initial_state  # Set initial state on the workflow

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node("web_search_node", web_search)  # WEBSEARCH için benzersiz bir ad kullandık

workflow.set_conditional_entry_point(
    route_question,
    {
        "web_search_node": "web_search_node",  # WEBSEARCH yerine benzersiz ad kullanıyoruz
        RETRIEVE: RETRIEVE,
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        "web_search_node": "web_search_node",  # WEBSEARCH yerine benzersiz ad kullanıyoruz
        GENERATE: GENERATE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": "web_search_node",  # WEBSEARCH yerine benzersiz ad kullanıyoruz
    },
)
workflow.add_edge("web_search_node", GENERATE)  # WEBSEARCH yerine benzersiz ad kullanıyoruz
workflow.add_edge(GENERATE, END)

app = workflow.compile()

try:
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")
except AttributeError:
    print("Warning: draw_mermaid_png method is not supported in the current graph object.")
