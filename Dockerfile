# Stage 1: Build Stage
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app /app

# Stage 2: Test Stage (Optional)
FROM python:3.9-slim AS tester

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the application code
COPY ./app /app

# Run tests
# Assuming you have test scripts in /app/tests
RUN python -m unittest discover -s app/tests

# Stage 3: Production Stage
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the application code
COPY ./app /app

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
