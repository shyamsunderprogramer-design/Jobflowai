# Build from root to include backend/ structure
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code as backend/ folder
COPY backend ./backend

# Set PYTHONPATH so 'from backend.xxx' works
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run app
# Run app using PORT env var (default 8000)
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"