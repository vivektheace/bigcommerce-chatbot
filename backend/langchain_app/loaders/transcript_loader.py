import os
import json
import logging
from typing import List
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_transcripts(transcript_dir: str) -> List[Document]:
    """
    Loads transcript JSON files and converts them to LangChain Document chunks.

    Args:
        transcript_dir (str): Path to directory with video transcript JSONs.

    Returns:
        List[Document]: List of LangChain Document objects with metadata.
    """
    documents = []

    if not os.path.exists(transcript_dir):
        logger.warning(f"Transcript directory not found: {transcript_dir}")
        return documents

    for file in os.listdir(transcript_dir):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(transcript_dir, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            product_name = data.get("title", file.replace(".json", ""))
            video_id = data.get("video_id", "")
            transcript = data.get("transcript", [])

            for chunk in transcript:
                documents.append(Document(
                    page_content=chunk["content"],
                    metadata={
                        "source": file,
                        "type": "transcript",
                        "product_name": product_name,
                        "video_id": video_id,
                        "start_time": chunk.get("start", ""),
                        "chunk_id": chunk.get("chunk_id", None)
                    }
                ))

            logger.info(f" Loaded {len(transcript)} chunks from {file}")
        except Exception as e:
            logger.error(f" Failed to load transcript from {file}: {str(e)}")

    return documents

# example usage
if __name__ == "__main__":
    transcript_dir = "D:/bigcommerce-chatbot/data/transcripts"
    docs = load_transcripts(transcript_dir)
    print(f"Total documents loaded: {len(docs)}")
