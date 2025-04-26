# backend/langchain_app/scripts/retrieval_pipeline.py

import sys
import os

# Setup sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from backend.langchain_app.chains.retriever_chain import build_rag_chain, run_query


def run_retrieval_pipeline(
    collection_name: str = "manuals",
    user_query: str = "How do I reset my Samsung convection oven?",
):
    """
    Runs the retrieval pipeline:
    - Builds a RAG chain with the specified collection
    - Runs the query against the chain

    Args:
        collection_name (str): Name of the Qdrant collection to retrieve from.
        user_query (str): User query to search for.
    """
    # Build retrieval chain
    chain = build_rag_chain(collection_name=collection_name)

    # Run the query
    result = run_query(chain, user_query)

    return result


# If you want it runnable directly too
if __name__ == "__main__":
    run_retrieval_pipeline(collection_name="manuals", user_query="How do I reset my Samsung convection oven?")
