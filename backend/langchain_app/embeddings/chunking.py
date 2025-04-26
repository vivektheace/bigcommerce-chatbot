# backend/langchain_app/embeddings/chunking.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List

def chunk_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Document]:
    """
    Splits raw documents into smaller chunks using recursive splitting.
    
    Args:
        documents (List[Document]): Raw LangChain documents.
        chunk_size (int): Max token size per chunk.
        chunk_overlap (int): Overlap between chunks for better context.

    Returns:
        List[Document]: Chunked documents with metadata preserved.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " "]
    )
    return splitter.split_documents(documents)
