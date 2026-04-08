FROM python:3.9-slim

WORKDIR /app

# Copy only the essential file
COPY app.py .

# Expose port
EXPOSE 7860

# Run the app
CMD ["python", "-u", "app.py"]
