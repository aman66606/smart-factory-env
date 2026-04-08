from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle root path and health check
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "healthy",
                "openenv": "ready",
                "message": "Smart Factory Environment"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/reset":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "ok", "message": "reset"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/step":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"reward": 0.5, "done": False}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"{format % args}")

port = 7860
print(f"Server starting on port {port}")
server = HTTPServer(("0.0.0.0", port), Handler)
print("Server running! Ready for requests.")
server.serve_forever()
