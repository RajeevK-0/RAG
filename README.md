---
title: AI ML Research Assistant
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
startup_duration_timeout: 1h
pinned: false
---

# AI/ML Research Paper RAG Assistant 📚
This is a Retrieval-Augmented Generation (RAG) portfolio project built with FastAPI, Streamlit, LangChain, and FAISS.

**[🔗 Live Demo](https://huggingface.co/spaces/RajeevK-0/AI-ML-research-assistant)**

## Overview
This project is a full-stack Retrieval-Augmented Generation (RAG) application designed to help users query and interact with AI/ML research papers. It leverages a FastAPI backend for processing queries, a Streamlit frontend for a seamless chat experience, and LangChain with FAISS for efficient vector similarity search. 

Additionally, it integrates LangSmith for live background evaluation of LLM responses, ensuring high-quality answers by measuring groundedness and relevance on the fly.

## Key Features
- **Conversational Interface:** An intuitive chat UI built with Streamlit, which maintains chat history for contextual follow-up questions.
- **Streaming Responses:** Real-time typewriter-effect token streaming from the FastAPI backend to the frontend.
- **Advanced RAG Pipeline:** Utilizes LangChain and FAISS for fast and accurate document retrieval.
- **Live Evaluation Tracking:** Automatically evaluates generated answers against the retrieved context for Groundedness and Answer Relevance using LangSmith in background tasks, without blocking the user response.
- **Dockerized Deployment:** Ready to be deployed on platforms like Hugging Face Spaces or AWS with a unified startup script (`run.sh`).

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn, Pydantic
- **LLM / AI Ecosystem:** LangChain, Groq (ChatGroq), FAISS (Vector Database), Sentence-Transformers
- **Tracing & Evaluation:** LangSmith
- **Containerization:** Docker

## Prerequisites
You will need the following API keys to run this project:
- `GROQ_API_KEY`: For accessing the Groq LLM models.
- `LANGSMITH_API_KEY`: For logging and evaluating responses via LangSmith.

*Make sure to set these in your environment or a `.env` file (e.g., `llm_api_key` and `langsmith_api_key` under your `ragModule.config`).*

## Running Locally

### Option 1: Using Docker (Recommended)
1. Clone the repository.
2. Build the Docker image:
   ```bash
   docker build -t ml-rag-assistant .
   ```
3. Run the container:
   ```bash
   docker run -p 7860:7860 -p 8000:8000 \
     -e GROQ_API_KEY="your_groq_api_key" \
     -e LANGSMITH_API_KEY="your_langsmith_api_key" \
     ml-rag-assistant
   ```
4. Access the application at `http://localhost:7860`. (FastAPI backend will run on `8000`).

### Option 2: Manual Setup
1. Clone the repository and navigate into the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your environment variables are configured.
4. Start both the backend and frontend using the provided shell script:
   ```bash
   bash run.sh
   ```
5. The Streamlit interface will be available at `http://localhost:7860`.

## Project Structure
- `app.py`: Streamlit frontend application handling the UI and chat history.
- `main.py`: FastAPI application serving the `/askQuery` endpoint and LangSmith background evaluation tasks.
- `rag_main.py`: Core RAG pipeline implementation defining the LangChain logic and FAISS retrieval.
- `run.sh`: Startup script designed to launch both FastAPI and Streamlit concurrently.
- `Dockerfile`: Container configuration setting up a non-root user and executing `run.sh`.
- `requirements.txt`: Project dependencies.
- **`ragModule/`**: Contains core RAG processing and configuration scripts.
  - `config.py`: Manages environment variables and API keys (e.g., Groq, LangSmith).
  - `data_loader.py`: Handles ingestion and parsing of research papers (PDFs, text, etc.).
  - `embedding.py`: Manages the text chunking and embedding generation using Sentence-Transformers.
  - `search.py`: Orchestrates the retrieval logic and prompt generation for querying.
  - `vector_store.py`: Initializes and interacts with the FAISS vector database.