from langchain.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

import sys
import os

# Setup sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.db.qdrant_client import get_qdrant_client
from backend.langchain_app.embeddings.embed_utils import get_embedder

from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()


# Setup logger
logger = logging.getLogger(__name__)


def get_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.0):
    """
    Returns an instance of ChatOpenAI configured for Groq.
    """
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY"), 
    )


def get_qdrant_retriever(collection_name: str, source_filter: str = None):
    """
    Returns a retriever object configured to query the specified Qdrant collection.
    Optionally applies a source filter.
    """
    client = get_qdrant_client()
    embedder = get_embedder()

    qdrant = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embedder,
    )

    search_kwargs = {"k": 3}

    if source_filter:
        logger.info(f"Applying filter for source: {source_filter}")
        search_kwargs["filter"] = Filter(
            must=[FieldCondition(key="source", match=MatchValue(value=source_filter))]
        )

    return qdrant.as_retriever(search_kwargs=search_kwargs)


# Define QA prompt expecting context and question
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant for Samsung product support.
Use the following context to answer the user's question.

Context:
{context}

Question:
{question}

Answer:"""
)


def build_rag_chain(
    collection_name: str,
    model_name: str = "llama-3.1-8b-instant",
    temperature: float = 0.0,
    source_filter: str = None
) -> ConversationalRetrievalChain:
    """
    Builds a Conversational Retrieval-Augmented Generation (RAG) chain 
    using a specified Qdrant collection and LLM model.
    """
    print("RAG Chain STARTING")
    retriever = get_qdrant_retriever(collection_name, source_filter)
    print("RAG Chain retriever created")
    llm = get_llm(model_name=model_name, temperature=temperature)
    print("RAG Chain LLM created")

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    print("RAG Chain memory created")

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": qa_prompt
        },
        return_source_documents=True,
        output_key="answer"
    ) 
    


def run_query(chain: ConversationalRetrievalChain, query: str):
    """
    Executes a query using the provided RAG chain and prints the answer and source documents.
    """
    logger.info(f"Running RAG query: {query}")
    result = chain.invoke({"question": query})

    print("\nAnswer:\n", result)

    print("\nSource Documents:")
    try:
        for doc in chain.memory.chat_memory.messages[-1].additional_kwargs.get('source_documents', []):
            source = doc.metadata.get('source', 'unknown')
            product = doc.metadata.get('product', '')
            preview = doc.page_content[:180].replace('\n', ' ') + "..."
            print(f"- [{source}] {product} → {preview}")
    except Exception:
        print("(No metadata or source documents returned)")

    return result
