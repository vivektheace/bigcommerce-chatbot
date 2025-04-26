## BigCommerce Chatbot
A chatbot system developed for BigCommerce to assist customers by retrieving information from product manuals, support tickets, website content, and intranet videos.

## Project Structure

```plaintext
├── .env
├── Dockerfile
├── README.md
├── auth.py
├── backend
│   ├── __init__.py
│   ├── db
│   │   ├── mock_customer_db.py
│   │   ├── models.py
│   │   ├── qdrant_client.py
│   ├── ingestion.py
│   ├── langchain_app
│   │   ├── __init__.py
│   │   ├── chains
│   │   │   ├── __init__.py
│   │   │   ├── retriever_chain.py
│   │   │   ├── test_retriever.py
│   │   │   ├── ticket_escalation.py
│   │   ├── embeddings
│   │   │   ├── chunking.py
│   │   │   ├── embed_utils.py
│   │   ├── loaders
│   │   │   ├── __init__.py
│   │   │   ├── manual_loader.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── ticket_loader.py
│   │   │   ├── transcript_loader.py
│   │   │   ├── website_loader.py
│   ├── retriever.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── ingestion_test.py
├── data
│   ├── manuals/
│   ├── mock_customers/
│   ├── processed_manuals/
│   ├── tickets/
│   ├── transcripts/
│   ├── webpage/
├── generate_tree.py
├── qdrant-path/
├── requirements.txt
├── routes.py
├── streamlit_app.py
├── supervisord.conf
```
## Features
Retrieval of information from manuals, support tickets, website, and intranet resources.

User authentication using JWT before ticket creation.

Retrieval-Augmented Generation (RAG) powered by LangChain and Qdrant.

API backend developed using FastAPI with a Streamlit-based user interface.

Full containerization with Docker for consistent deployment.

## Technology Stack
Backend: FastAPI, LangChain, LlamaIndex

Frontend: Streamlit

Vector Database: Qdrant

Containerization: Docker, Supervisord

Authentication: JWT Tokens

## Installation and Setup
# Clone the repository:
git clone <repository-url>
cd bigcommerce-chatbot

# Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate     # Windows

## Install project dependencies:
pip install -r requirements.txt
Set up environment variables:
Create a .env file and define the necessary variables.

## Start the FastAPI server:
uvicorn routes:app --host 0.0.0.0 --port 8000 --reload

## Start the Streamlit application:
streamlit run streamlit_app.py

## Usage
Access the API documentation via Swagger UI:
http://localhost:8000/docs

Access the Streamlit chatbot interface:
http://localhost:8501

## Users must authenticate before raising support tickets.

## Docker Deployment
Build the Docker image:
docker build -t bigcommerce-chatbot .

Run the Docker container:
docker run -d -p 8000:8000 -p 8501:8501 bigcommerce-chatbot

## Future Enhancements
WhatsApp integration via Twilio.

Multilingual support for chatbot interactions.

Auto-escalation mechanism for unresolved queries.

Caching frequently asked questions for faster responses.

## RAID Matrix

Risk	Assumption	Issue	Dependency
High chatbot traffic	Users prefer chatbot support over traditional channels	Response latency under high load	Qdrant indexing and retrieval efficiency
Data security requirements	Infrastructure remains internal to BigCommerce	Unauthorized access incidents	Secure JWT and API management
Scalability challenges	Initial traffic estimations	Increased concurrent user demand	Container orchestration for scaling

## Acknowledgements
This project demonstrates the use of modern Retrieval-Augmented Generation (RAG) techniques, semantic search, and containerized deployment practices for enterprise-grade chatbot solutions.

## Best Practices Followed
Modular codebase with clear separation of concerns.

Centralized configuration using environment variables.

Containerized architecture for consistent environment setup and deployment.

Comprehensive documentation of API and project usage.

Designed for future extensibility to new platforms and channels.

## References
FastAPI Documentation

Streamlit Documentation

Qdrant Documentation

LangChain Documentation

## Notes
This documentation is prepared following professional software development and deployment standards to ensure clarity, maintainability, and ease of onboarding for new developers or stakeholders.