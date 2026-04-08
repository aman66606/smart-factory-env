import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from environment import SmartFactoryEnv

print("Starting Smart Factory Environment...", flush=True)
print("Python version:", sys.version, flush=True)

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
            import numpy as np
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
        print(f"[{self.path}] {format % args}", flush=True)

if __name__ == "__main__":
    port = 7860
    print(f"Starting server on port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"✅ Server running on port {port}", flush=True)
    print(f"🌐 Health check: http://localhost:{port}/health", flush=True)
    server.serve_forever()
