# test_retrieval.py
import sys
import os

# Setup sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from backend.langchain_app.chains.retriever_chain import build_rag_chain, run_query

if __name__ == "__main__":
    # Basic run without filters
    chain = build_rag_chain(collection_name="manuals")
    run_query(chain, "How do I reset my Samsung convection oven?")
