FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables (override at runtime)
ENV API_BASE_URL="https://api.openai.com/v1"
ENV MODEL_NAME="gpt-3.5-turbo"
ENV HF_TOKEN=""

# Expose port for Spaces
EXPOSE 7860

# Run the inference script (for testing) or app (for demo)
CMD ["python", "app.py"]