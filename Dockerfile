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
# FROM python:3.12-slim

# # 1. Install system build tools for ML packages (FAISS, Scikit-Learn, etc.)
# RUN apt-get update && apt-get install -y gcc g++ build-essential

# # 2. Set up the working directory BEFORE switching users
# WORKDIR /home/user/app

# # 3. Create user and assign explicit ownership to the working directory
# RUN useradd -m -u 1000 user
# RUN chown -R user:user /home/user/app

# # 4. Now switch to the non-root user
# USER user
# ENV PATH="/home/user/.local/bin:$PATH"

# # 5. Copy requirements and install
# COPY --chown=user requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 6. Copy the rest of the app (including FAISS index)
# COPY --chown=user . .

# EXPOSE 7860

# CMD ["bash", "run.sh"]