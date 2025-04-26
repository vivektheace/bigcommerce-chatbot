import os
import json
import logging
from typing import List
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_website_data(website_dir: str) -> List[Document]:
    """
    Loads product website data from JSON files and converts to LangChain Documents.

    Args:
        website_dir (str): Path to folder containing website JSON files.

    Returns:
        List[Document]: List of Document objects with metadata.
    """
    documents = []

    if not os.path.exists(website_dir):
        logger.warning(f"Website directory does not exist: {website_dir}")
        return documents

    for file in os.listdir(website_dir):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(website_dir, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            product_name = data.get("product_name", file.replace(".json", ""))

            highlights = data.get("overview", {}).get("highlights", [])
            features = data.get("product_details", {}).get("features", [])

            # Combine both highlight bullets and detailed features
            all_content = highlights + features

            for i, content in enumerate(all_content):
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source": file,
                        "product_name": product_name,
                        "type": "website",
                        "feature_index": i
                    }
                ))

            logger.info(f"Loaded {len(all_content)} website chunks from {file}")
        except Exception as e:
            logger.error(f"Failed to load website data from {file}: {str(e)}")

    return documents


# example usage
if __name__ == "__main__":
    website_dir = "D:/bigcommerce-chatbot/data/website_data"
    docs = load_website_data(website_dir)
    print(f"Total documents loaded: {len(docs)}")