# backend/langchain_app/api/app.py

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from backend.ingestion import run_ingestion_pipeline
from backend.retriever import run_retrieval_pipeline
from auth import verify_token
from backend.db.mock_customer_db import customers
from backend.db.models import TicketRequest



import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Swagger Auth scheme
bearer_scheme = HTTPBearer()

# FastAPI app setup
app = FastAPI(
    title="BigCommerce Chatbot API",
    description="API for running document ingestion and retrieval",
    version="1.0.0"
)

# Pydantic model for request
class RetrievalRequest(BaseModel):
    query: str
    collection_name: str = "manuals"

# --- Endpoints ---

@app.post("/ingest")
async def ingest_documents(token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    user_data = verify_token(authorization=f"{token.scheme} {token.credentials}")
    logger.info(f"Token verified for ingest: {user_data}")
    
    try:
        run_ingestion_pipeline()
        return {"message": "Ingestion completed successfully."}
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/retrieve")
async def retrieve_documents(
    request: RetrievalRequest,
    token: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    user_data = verify_token(authorization=f"{token.scheme} {token.credentials}")
    logger.info(f"Token verified for retrieve: {user_data}")
    logger.info(f"Retrieval request: {request.dict()}")

    try:
        response = run_retrieval_pipeline(
            collection_name=request.collection_name,
            user_query=request.query
        )
        return {
            "query": request.query,
            "collection": request.collection_name,
            "response": response
        }
    except Exception as e:
        logger.error(f"Retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@app.post("/ticket")
async def create_ticket(
    request: TicketRequest,
    token: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    user_data = verify_token(authorization=f"{token.scheme} {token.credentials}")
    logger.info(f"Token verified for ticket creation: {user_data}")
    logger.info(f"Ticket creation request: {request.dict()}")

    try:
        # Extract customer_id from the request
        customer_id = request.customer_id  # Adjust this if your TicketRequest field has a different name

        # Validate if customer exists in the database
        if not any(customer["id"] == customer_id for customer in customers):
            logger.error(f"Customer with ID {customer_id} not found.")
            raise HTTPException(status_code=404, detail="Customer not found")

        # If customer exists, proceed to create ticket
        return {
            "message": "Ticket created successfully!",
            "ticket_details": request.dict()
        }
    except Exception as e:
        logger.error(f"Ticket creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ticket creation failed: {str(e)}")
@app.get("/")
def root():
    return {"message": "Welcome to the BigCommerce Chatbot API!"}
