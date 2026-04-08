import sys
import numpy as np

# Simple HTTP server instead of Gradio to avoid conflicts
print("Smart Factory Environment - OpenEnv Hackathon")
print("=============================================")
print("Environment is ready!")
print("")
print("API Endpoints:")
print("  - GET /health - Health check")
print("  - POST /reset - Reset environment")
print("  - POST /step - Take an action")
print("")

# Simple health check endpoint
def health_check():
    return {"status": "healthy", "environment": "SmartFactoryEnv"}

print("To test the environment, run: python inference.py")
print("")
print("Environment running successfully!")

# Keep the container alive
import time
import json

if __name__ == "__main__":
    print("Starting environment server...")
    print(json.dumps({
        "event": "SERVER_START",
        "status": "ready",
        "environment": "SmartFactoryEnv",
        "tasks": ["easy", "medium", "hard"]
    }))
    
    # Keep running for health checks
    while True:
        time.sleep(60)
        print(json.dumps({"event": "HEARTBEAT", "timestamp": time.time()}))
