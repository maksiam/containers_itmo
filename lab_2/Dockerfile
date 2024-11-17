FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python packages
# RUN pip install --no-cache-dir \
#     faiss-cpu \
#     numpy \
#     python-telegram-bot \
#     mistralai \
#     langchain \
#     sentence-transformers \
#     PyPDF2 \
#     python-dotenv

# Copy the application code
COPY . .

# Set environment variables (if needed)
# ENV TELEGRAM_BOT_TOKEN=your_token_here
# ENV MISTRAL_API_KEY=your_key_here
# ENV FAISS_DB_PATH=/app/faiss_index

# Run the application
CMD ["python", "main.py"]