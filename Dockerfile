# Combined image for single-service cloud deployment: build the React frontend,
# then serve it together with the FastAPI backend from one process.
# (Local development still uses docker-compose with two separate services.)

# --- Stage 1: build the frontend ---
FROM node:22-alpine AS frontend
WORKDIR /fe
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
# The backend serves this build, so the API is same-origin (no host needed).
ENV VITE_API_URL=""
RUN npm run build

# --- Stage 2: backend + bundled frontend ---
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY --from=frontend /fe/dist ./static
EXPOSE 8000
# Seed the database, then serve API + frontend on the host-provided port.
CMD ["sh", "-c", "python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
