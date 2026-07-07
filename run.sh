#!/bin/bash

# Start FastAPI on port 8000 in the background (the '&' is critical)
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on port 7860 in the foreground
python -m streamlit run app.py --server.port 7860 --server.address 0.0.0.0