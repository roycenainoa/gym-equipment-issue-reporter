# Backend image — pinned to Python 3.12 for a reproducible, wheel-compatible build.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer between code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app ./app

EXPOSE 8000

# Seed the database on first start, then launch the API server.
# Use $PORT when the host provides one (e.g. cloud platforms), else default to 8000.
CMD ["sh", "-c", "python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
