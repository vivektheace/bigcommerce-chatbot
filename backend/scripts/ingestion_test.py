from dotenv import load_dotenv
import os
import logging
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from backend.langchain_app.loaders.pdf_loader import batch_process_pdfs
from backend.langchain_app.loaders.manual_loader import load_manual_json_chunks
from backend.langchain_app.loaders.transcript_loader import load_transcripts
from backend.langchain_app.loaders.website_loader import load_website_data
from backend.langchain_app.loaders.ticket_loader import load_support_tickets

from backend.langchain_app.embeddings.chunking import chunk_documents
from backend.langchain_app.embeddings.embed_utils import store_documents_in_qdrant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Directory paths (update manually for Windows-style paths)
RAW_PDF_DIR = os.getenv("RAW_PDF_DIR", "D:\\bigcommerce-chatbot\\data\\manuals_raw_pdfs")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "D:\\bigcommerce-chatbot\\data\\processed_manuals")
TRANSCRIPTS_DIR = os.getenv("TRANSCRIPTS_DIR", "D:\\bigcommerce-chatbot\\data\\transcripts")
WEBSITE_DIR = os.getenv("WEBSITE_DIR", "D:\\bigcommerce-chatbot\\data\\webpage")
TICKET_FILE = os.getenv("TICKET_FILE", "D:\\bigcommerce-chatbot\\data\\tickets\\resolved_support_tickets.json")

# --- Step 1: Process Raw PDFs ---
logger.info("Processing raw PDF manuals...")
batch_process_pdfs(RAW_PDF_DIR, PROCESSED_DIR)

# --- Step 2: Load Processed Manual Chunks ---
logger.info("Loading processed manual chunks...")
manual_docs = load_manual_json_chunks(PROCESSED_DIR)
logger.info(f"Loaded {len(manual_docs)} manual documents.")

# --- Step 3: Load Video Transcripts ---
logger.info("Loading video transcripts...")
transcript_docs = load_transcripts(TRANSCRIPTS_DIR)
logger.info(f"Loaded {len(transcript_docs)} transcript chunks.")

# --- Step 4: Load Website Data ---
logger.info("Loading website data...")
website_docs = load_website_data(WEBSITE_DIR)
logger.info(f"Loaded {len(website_docs)} website chunks.")

# --- Step 5: Load Support Ticket Data ---
logger.info("Loading support tickets...")
ticket_docs = load_support_tickets(TICKET_FILE)
logger.info(f"Loaded {len(ticket_docs)} support ticket documents.")

# Combine all documents (optional: for embedding or search)
all_docs = manual_docs + transcript_docs + website_docs + ticket_docs
logger.info(f"Total loaded documents for embedding: {len(all_docs)}")

chunk_doc= chunk_documents(all_docs, chunk_size=500, chunk_overlap=100)
logger.info(f"Total chunked documents: {len(chunk_doc)}")

store_documents_in_qdrant(chunk_doc, collection_name="manuals", embedder_model="sentence-transformers/all-MiniLM-L6-v2", test_query="How do I reset my Samsung convection oven?")
print("All documents have been processed and stored in Qdrant.")