#!/usr/bin/env python3
import json
import os
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler
from environment import SmartFactoryEnv

# Get port from environment variable (HF Spaces sets this)
PORT = int(os.environ.get("PORT", 7860))

# Global environment
env = SmartFactoryEnv(difficulty="medium")

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "healthy",
                "openenv": "ready",
                "endpoints": ["/reset", "/step", "/health"]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        global env
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if self.path == "/reset":
            difficulty = data.get("difficulty", "medium")
            env = SmartFactoryEnv(difficulty=difficulty)
            state = env.reset()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "state": {
                    "day": state.day,
                    "inventory": state.inventory_levels,
                    "cash": state.cash_reserve
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == "/step":
            action = data.get("action", [1.0, 0.5, 0.3])
            next_state, reward, done, info = env.step(np.array(action))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "reward": float(reward),
                "done": done,
                "state": {
                    "day": next_state.day,
                    "inventory": next_state.inventory_levels
                }
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.path}] {format % args}")

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"✅ Server running on port {PORT}")
    server.serve_forever()
