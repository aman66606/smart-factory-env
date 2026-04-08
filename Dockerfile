FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir numpy pyyaml

# Copy all files
COPY app.py .
COPY environment.py .
COPY tasks.py .
COPY inference.py .
COPY openenv.yaml .

# Expose the port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
