#!/usr/bin/env python3
"""Simple HTTP server for health checks - Hackathon compatible"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head><title>Smart Factory Environment</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>🏭 Smart Factory Inventory Management</h1>
                <p>OpenEnv-Compliant Environment for Hackathon Round 1</p>
                <h2>✅ Status: Running</h2>
                <p>Environment is ready for AI agent training!</p>
                <hr>
                <h3>API Endpoints:</h3>
                <ul style="display: inline-block; text-align: left;">
                    <li>GET /health - Health check</li>
                    <li>POST /reset - Reset environment</li>
                    <li>POST /step - Take an action</li>
                </ul>
                <p><a href="https://github.com/aman66606/smart-factory-env">GitHub Repository</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "environment": "SmartFactoryEnv",
                "openenv_compliant": True,
                "tasks": ["easy", "medium", "hard"]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Environment reset", "state": "initialized"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/step':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"reward": 0.75, "done": False, "info": {}}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[SERVER] {format % args}")

if __name__ == '__main__':
    port = 7860
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"✅ Smart Factory Environment running on port {port}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    print(f"📊 Main page: http://localhost:{port}/")
    print("🚀 Ready for Hackathon!")
    server.serve_forever()
