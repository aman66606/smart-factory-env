FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY environment.py .
COPY tasks.py .
COPY inference.py .
COPY openenv.yaml .
COPY README.md .

# Expose port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
