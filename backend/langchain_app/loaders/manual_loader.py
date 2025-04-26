import os
import json
import logging
from typing import List
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_manual_json_chunks(manuals_dir: str) -> List[Document]:
    """
    Loads pre-processed manual chunks (JSON) and returns LangChain Documents.

    Args:
        manuals_dir (str): Path to folder with parsed manual chunks as JSON files.

    Returns:
        List[Document]: List of LangChain-compatible Document objects.
    """
    documents = []

    if not os.path.exists(manuals_dir):
        logger.warning(f"Manuals directory does not exist: {manuals_dir}")
        return documents

    for product_folder in os.listdir(manuals_dir):
        product_path = os.path.join(manuals_dir, product_folder)
        chunks_path = os.path.join(product_path, "chunks.json")

        if not os.path.isfile(chunks_path):
            logger.warning(f"No chunks.json found in: {product_path}")
            continue

        try:
            with open(chunks_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            for chunk in chunks:
                content = chunk.get("content", "")
                metadata = chunk.get("metadata", {})
                metadata.update({
                    "chunk_id": chunk.get("chunk_id"),
                    "chunk_type": chunk.get("chunk_type"),
                    "source": metadata.get("source", product_folder),
                    "page_number": chunk.get("page_number", None)
                })

                documents.append(Document(page_content=content, metadata=metadata))

            logger.info(f"Loaded {len(chunks)} chunks from {product_folder}")
        except Exception as e:
            logger.error(f"Failed to load {chunks_path}: {str(e)}")

    return documents


if __name__ == "__main__":
    manuals_dir = "D:/bigcommerce-chatbot/data/processed_manuals"
    docs = load_manual_json_chunks(manuals_dir)
    print(f"Total documents loaded: {len(docs)}")
