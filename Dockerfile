# ===== Stage 1: Build the Svelte frontend =====
FROM node:18.12.1-buster-slim AS frontend-builder

WORKDIR /frontend

# Copy package files first for better layer caching
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy remaining frontend files and build
COPY frontend .
RUN npm run build

# ===== Final Stage =====
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/backend \
    APP_ENV=production

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /backend

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend .

# Copy built frontend from builder
COPY --from=frontend-builder /frontend/dist /frontend/dist

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]