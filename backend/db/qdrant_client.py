from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
import socket


def get_qdrant_client() -> QdrantClient:
    """
    Tries to connect to a running Qdrant server (localhost:6333).
    Falls back to embedded Qdrant with persistent storage if not available.
    """
    try:
        socket.create_connection(("localhost", 6333), timeout=1)
        print("Connected to Qdrant server at localhost:6333")
        return QdrantClient(host="localhost", port=6333)
    except OSError:
        persistent_path = "D:\\bigcommerce-chatbot\\qdrant-path"  
        print(f"Qdrant server not found. Using embedded mode at {persistent_path}")
        return QdrantClient(path=persistent_path)

        
      


def ensure_collection_exists(
    client: QdrantClient,
    collection_name: str,
    vector_size: int = 384,
    distance: Distance = Distance.COSINE
):
    """
    Creates a new Qdrant collection if it doesn't exist.
    """
    existing_collections = [col.name for col in client.get_collections().collections]
    if collection_name not in existing_collections:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )
