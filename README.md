```Plaintext
DUE TO LARGE SIZE ,IF DATA FOLDER DOESNT OPEN ,PLEASE LET ME KNOW
SAME GOES WITH THE QDRANT-PATH FOLDER
SORRY FOR THE INCONVENIENCE ```
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

## Overview

- Retrieval-Augmented Generation (RAG) using LangChain and Qdrant
- Unified retrieval from manuals, tickets, website data, and intranet resources
- JWT-based user authentication for ticket operations
- FastAPI backend with a Streamlit user interface
- Full Docker-based deployment with Supervisord process management

---

## Tech Stack

- **Backend:** FastAPI, LangChain, LlamaIndex
- **Frontend:** Streamlit
- **Database:** Qdrant (vector search)
- **Containerization:** Docker, Supervisord
- **Authentication:** JWT Tokens

---

## Quick Start

### Clone Repository

```bash
git clone <repository-url>
cd bigcommerce-chatbot
```

### Set Up Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Configure Environment

- Create a `.env` file in the root folder with required variables.

---

## Running Locally

### Launch API Server

```bash
uvicorn routes:app --host 0.0.0.0 --port 8000 --reload
```

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### Launch Streamlit App

```bash
streamlit run streamlit_app.py
```

- Streamlit UI: [http://localhost:8501](http://localhost:8501)

> **Note:** JWT authentication is required for ticket submission.

---

## Docker Deployment

### Build Image

```bash
docker build -t bigcommerce-chatbot .
```

### Run Container

```bash
docker run -d -p 8000:8000 -p 8501:8501 bigcommerce-chatbot
```

---

## Enhancements (Planned)

- WhatsApp integration (via Twilio)
- Multilingual chatbot support
- Auto-escalation for unresolved queries
- Caching common queries for faster response

---

## RAID Analysis

| Risk                   | Assumption                            | Issue                         | Dependency                       |
|-------------------------|---------------------------------------|-------------------------------|----------------------------------|
| High chatbot load       | User preference shift to chatbot      | Latency under heavy traffic    | Qdrant retrieval performance     |
| Data security needs     | Internal hosting of infrastructure    | Unauthorized access risks      | Secure JWT and API authorization |
| Scaling challenges      | Traffic projections may fluctuate     | Resource limitations           | Container orchestration required |

---

## Best Practices

- Modularized and scalable codebase
- Centralized configuration via `.env`
- Containerized setup for reliable deployments
- Detailed API and project documentation
- Forward-compatible design for new platforms

---

## References

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)
- [Qdrant](https://qdrant.tech/documentation/)
- [LangChain](https://python.langchain.com/)

---

## Notes

This project follows industry standards for RAG pipelines, secure authentication, and containerized deployments, ensuring maintainability and ease of scaling for enterprise use.

---

