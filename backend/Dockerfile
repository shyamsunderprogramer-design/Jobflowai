# Build from the root context (docker-compose context: .)
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the backend folder
# (Assumes docker build context is the project root)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into /app/backend
COPY backend ./backend

# Set PYTHONPATH so that "from backend.xxx" imports work
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run uvicorn properly targeting the app
# Use 0.0.0.0 to bind to all interfaces
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"
