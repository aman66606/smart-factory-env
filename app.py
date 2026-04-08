import sys
print("Starting...", flush=True)

# Simple HTTP server - NO external dependencies needed
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "message": "Smart Factory Ready"}).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"reward": 0.5, "done": False}).encode())
    
    def log_message(self, format, *args):
        print(f"Server: {format % args}", flush=True)

port = 7860
print(f"Starting on port {port}", flush=True)
HTTPServer(('0.0.0.0', port), Handler).serve_forever()
