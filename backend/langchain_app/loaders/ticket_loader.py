import os
import json
import logging
from typing import List
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_support_tickets(ticket_file: str) -> List[Document]:
    """
    Loads resolved support tickets from a JSON file and converts them to LangChain Q&A documents.

    Args:
        ticket_file (str): Path to a JSON file containing support ticket entries.

    Returns:
        List[Document]: List of Q&A-style LangChain Document objects.
    """
    documents = []

    if not os.path.exists(ticket_file):
        logger.warning(f"Ticket file not found: {ticket_file}")
        return documents

    try:
        with open(ticket_file, "r", encoding="utf-8") as f:
            tickets = json.load(f)

        for ticket in tickets:
            issue = ticket.get("issue", "").strip()
            resolution = ticket.get("resolution_summary", "").strip()
            product = ticket.get("product", "Unknown")
            ticket_id = ticket.get("ticket_id", "")
            customer = ticket.get("customer_name", "Unknown")

            if not issue or not resolution:
                continue

            documents.append(Document(
                page_content=f"Customer Issue: {issue}\nResolution: {resolution}",
                metadata={
                    "ticket_id": ticket_id,
                    "customer_name": customer,
                    "product": product,
                    "type": "support_ticket"
                }
            ))

        logger.info(f"Loaded {len(documents)} ticket documents from {ticket_file}")
    except Exception as e:
        logger.error(f"Failed to load tickets from {ticket_file}: {str(e)}")

    return documents
