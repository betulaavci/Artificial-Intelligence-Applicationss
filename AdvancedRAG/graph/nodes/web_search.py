from typing import Any, Dict
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import GraphState

web_search_tool = TavilySearchResults(k=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state.get("question", "")
    documents = state.get("documents", [])

    # Web arama sonuçlarını al ve birleştir
    docs = web_search_tool.invoke({"query": question})
    web_results_content = "\n".join([d["content"] for d in docs])
    web_result_document = Document(page_content=web_results_content)

    # Sadece `documents` anahtarını tek adımda güncelleyerek döndür
    documents.append(web_result_document)
    return {
        "documents": documents  # Sadece `documents` güncelleniyor
    }


