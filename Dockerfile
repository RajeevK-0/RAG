FROM python:3.12-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install them first to cache the layer
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files, including your code and faiss_index folder
COPY --chown=user . .

# Hugging Face forwards public traffic to this port
EXPOSE 7860

# Launch the startup script
CMD ["bash", "run.sh"]