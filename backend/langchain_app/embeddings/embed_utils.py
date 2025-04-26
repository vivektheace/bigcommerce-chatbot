# backend/langchain_app/embeddings/embed_utils.py

from typing import List, Optional
from uuid import uuid4
import os

from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Qdrant

from qdrant_client.http.models import Distance, VectorParams

from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from qdrant_client.http.models import Distance, VectorParams

from backend.db.qdrant_client import get_qdrant_client


# Import shared DB functions
from backend.db.qdrant_client import get_qdrant_client

def get_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.0):
    """
    Returns an instance of ChatOpenAI configured for Groq.
    """
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=os.getenv("GROQ_API_KEY"),   # You should set this in your .env
    )

def get_embedder(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """
    Returns a HuggingFaceEmbeddings instance for the given model.
    """
    return HuggingFaceEmbeddings(model_name=model_name)


def store_documents_in_qdrant(
    documents: List[Document],
    collection_name: str,
    embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    test_query: Optional[str] = None
):
    """
    Embeds documents using HuggingFace and stores them in Qdrant.

    Args:
        documents (List[Document]): List of LangChain Document objects to store.
        collection_name (str): Name of the Qdrant collection.
        embedder_model (str): Embedding model to use for vectorization.
    """

    # Initialize embedder and Qdrant client
    embedder = get_embedder(embedder_model)
    qdrant_client = get_qdrant_client()

    # Set embedding dimension manually
    embedding_dimension = 384  # For sentence-transformers/all-MiniLM-L6-v2

    # Check if the collection exists, else create it
    existing_collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in existing_collections]

    if collection_name not in collection_names:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=embedding_dimension,
                distance=Distance.COSINE
            )
        )

    # Connect LangChain's Qdrant wrapper
    qdrant = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedder
    )

    # Enrich documents with unique UUIDs
    enriched_docs = [
        Document(
            page_content=doc.page_content,
            metadata={**doc.metadata, "uuid": str(uuid4())}
        )
        for doc in documents
    ]

    # Store enriched documents in Qdrant
    qdrant.add_documents(enriched_docs)

    # Test retrieval if query is provided
    if test_query:
        print("\n🔍 Testing query via ConversationalRetrievalChain...")

        retriever = qdrant.as_retriever(search_kwargs={"k": 1})

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

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
        rag_chain = ConversationalRetrievalChain.from_llm(
            llm=get_llm(model_name="llama-3.1-8b-instant", temperature=0),
            retriever=retriever,
            memory=memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=True
            
        )

        result = rag_chain.invoke({"question": test_query})
        print("\n🧠 Answer:")
        print(result["answer"])

        print("\n📚 Source Documents:")
        for doc in result["source_documents"]:
            print(f"- {doc.metadata.get('source', 'Unknown')} | {doc.page_content[:100]}...")

        return result

    print(f"Successfully stored {len(enriched_docs)} documents in Qdrant collection '{collection_name}'.")
