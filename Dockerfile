# Use official Python slim image for a lightweight production container
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir keeps the image small by discarding pip's cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project source into the container
COPY . .

# Create the vector store directory (persisted FAISS index)
# The .gitignore excludes data/vector_store/ so it must be created explicitly
RUN mkdir -p data/vector_store

# Expose port 7860 — required by Hugging Face Spaces,
# also compatible with Render, Railway, and local Docker
EXPOSE 7860

# Start the FastAPI application with Uvicorn
# Host 0.0.0.0 makes it accessible outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
