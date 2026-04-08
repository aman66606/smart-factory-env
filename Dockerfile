FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .
COPY environment.py .
COPY tasks.py .
COPY inference.py .
COPY openenv.yaml .

# Expose port
EXPOSE 7860

# Run
CMD ["python", "-u", "app.py"]
