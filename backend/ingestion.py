# backend/langchain_app/scripts/ingestion_pipeline.py

from dotenv import load_dotenv
import os
import logging
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.langchain_app.loaders.pdf_loader import batch_process_pdfs
from backend.langchain_app.loaders.manual_loader import load_manual_json_chunks
from backend.langchain_app.loaders.transcript_loader import load_transcripts
from backend.langchain_app.loaders.website_loader import load_website_data
from backend.langchain_app.loaders.ticket_loader import load_support_tickets
from backend.langchain_app.embeddings.chunking import chunk_documents
from backend.langchain_app.embeddings.embed_utils import store_documents_in_qdrant

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_ingestion_pipeline(
    raw_pdf_dir: str = None,
    processed_dir: str = None,
    transcripts_dir: str = None,
    website_dir: str = None,
    ticket_file: str = None,
    collection_name: str = "manuals",
    embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    test_query: str = "How do I reset my Samsung convection oven?",
    chunk_size: int = 500,
    chunk_overlap: int = 100,
):
    """
    Runs the full ingestion pipeline:
    - Processes raw PDFs
    - Loads manuals, transcripts, website, and ticket data
    - Chunks and stores into Qdrant

    Args:
        raw_pdf_dir (str): Directory of raw PDF files.
        processed_dir (str): Directory to save processed manuals.
        transcripts_dir (str): Directory containing video transcripts.
        website_dir (str): Directory containing website data.
        ticket_file (str): File path for support ticket JSON.
        collection_name (str): Qdrant collection name.
        embedder_model (str): Embedding model name.
        test_query (str): Test query after ingestion.
        chunk_size (int): Chunk size for documents.
        chunk_overlap (int): Overlap between chunks.
    """

    # Load environment variables if not provided
    load_dotenv()

    raw_pdf_dir = raw_pdf_dir or os.getenv("RAW_PDF_DIR", "D:\\bigcommerce-chatbot\\data\\manuals_raw_pdfs")
    processed_dir = processed_dir or os.getenv("PROCESSED_DIR", "D:\\bigcommerce-chatbot\\data\\processed_manuals")
    transcripts_dir = transcripts_dir or os.getenv("TRANSCRIPTS_DIR", "D:\\bigcommerce-chatbot\\data\\transcripts")
    website_dir = website_dir or os.getenv("WEBSITE_DIR", "D:\\bigcommerce-chatbot\\data\\webpage")
    ticket_file = ticket_file or os.getenv("TICKET_FILE", "D:\\bigcommerce-chatbot\\data\\tickets\\resolved_support_tickets.json")

    # Step 1: Process Raw PDFs
    logger.info("Processing raw PDF manuals...")
    batch_process_pdfs(raw_pdf_dir, processed_dir)

    # Step 2: Load Processed Manuals
    logger.info("Loading processed manual chunks...")
    manual_docs = load_manual_json_chunks(processed_dir)
    logger.info(f"Loaded {len(manual_docs)} manual documents.")

    # Step 3: Load Video Transcripts
    logger.info("Loading video transcripts...")
    transcript_docs = load_transcripts(transcripts_dir)
    logger.info(f"Loaded {len(transcript_docs)} transcript chunks.")

    # Step 4: Load Website Data
    logger.info("Loading website data...")
    website_docs = load_website_data(website_dir)
    logger.info(f"Loaded {len(website_docs)} website chunks.")

    # Step 5: Load Support Ticket Data
    logger.info("Loading support tickets...")
    ticket_docs = load_support_tickets(ticket_file)
    logger.info(f"Loaded {len(ticket_docs)} support ticket documents.")

    # Combine all documents
    all_docs = manual_docs + transcript_docs + website_docs + ticket_docs
    logger.info(f"Total loaded documents for embedding: {len(all_docs)}")

    # Step 6: Chunk Documents
    chunked_docs = chunk_documents(all_docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    logger.info(f"Total chunked documents: {len(chunked_docs)}")

    # Step 7: Store in Qdrant
    store_documents_in_qdrant(
        chunked_docs,
        collection_name=collection_name,
        embedder_model=embedder_model,
        test_query=test_query,
    )

    logger.info("All documents have been processed and stored in Qdrant successfully!")


# If you want to make it runnable directly too
if __name__ == "__main__":
    run_ingestion_pipeline()
