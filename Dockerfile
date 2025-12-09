FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .
COPY test_env.py .

# Expose port (Railway will override with PORT env var)
EXPOSE 8000

# Debug and start the app
CMD sh -c "env | grep -E 'DATABASE_URL|ENVIRONMENT|SECRET_KEY' && python test_env.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"