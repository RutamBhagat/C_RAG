from typing import Any, Dict

from app.graph.state import GraphState
from app.graph.chains.retrieval_grader import retrieval_grader


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """Determines whether the retrieved documents are relevant to the question while taking into account the recent chat history context.
    If any document is not relevant we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated is_web_search_needed flag
    """

    question = state.question
    documents = state.documents
    chat_history = state.chat_history

    filtered_docs = []
    is_web_search_needed = False

    grades = retrieval_grader.batch(
        [
            {"question": question, "chat_history": chat_history or [], "document": doc}
            for doc in documents
        ]
    )

    for index, grade in enumerate(grades):
        if grade.is_document_relevant:
            filtered_docs.append(documents[index])
        else:
            is_web_search_needed = True
            break

    return {
        "documents": filtered_docs,
        "is_web_search_needed": is_web_search_needed,
    }
