# Stage 1: Builder stage
FROM python:3.10.12 AS builder

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.10.12-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Copy project files
COPY . .

# Make sure scripts are executable
RUN chmod +x scripts/setup.sh

# Update PATH to include local Python packages
ENV PATH=/root/.local/bin:$PATH

# Expose port for Django app
EXPOSE 8000

# Run migrations and start the development server
RUN bash scripts/setup.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
