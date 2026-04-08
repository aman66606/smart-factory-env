#!/usr/bin/env python3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "healthy",
            "message": "Smart Factory Environment is running",
            "openenv": "ready"
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "ok", "message": "endpoint ready"}
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"Server: {format % args}")

if __name__ == '__main__':
    port = 7860
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"✅ Server running on port {port}")
    print(f"🌐 Health check: http://localhost:{port}")
    server.serve_forever()
