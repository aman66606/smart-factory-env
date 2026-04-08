#!/usr/bin/env python3
import json
import sys
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import your environment
from environment import SmartFactoryEnv

# Global environment instance
env = SmartFactoryEnv(difficulty="medium")

class OpenEnvHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <html>
            <head><title>Smart Factory Environment</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>🏭 Smart Factory Inventory Management</h1>
                <p>✅ OpenEnv-Compliant Environment</p>
                <p>Status: <span style="color: green;">RUNNING</span></p>
                <hr>
                <h3>API Endpoints:</h3>
                <ul>
                    <li>POST /reset - Reset environment</li>
                    <li>POST /step - Take action [reorder, supplier, maintenance]</li>
                    <li>GET /health - Health check</li>
                </ul>
                <p><a href="https://github.com/aman66606/smart-factory-env">GitHub Repository</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "healthy", "openenv": "ready"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if self.path == "/reset":
            global env
            env = SmartFactoryEnv(difficulty=data.get("difficulty", "medium"))
            state = env.reset()
            
            # Convert state to serializable format
            response = {
                "status": "ok",
                "state": {
                    "day": state.day,
                    "cash_reserve": state.cash_reserve,
                    "inventory": state.inventory_levels,
                    "machine_health": state.machine_health
                }
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == "/step":
            action = data.get("action", [1.0, 0.5, 0.3])
            next_state, reward, done, info = env.step(np.array(action))
            
            response = {
                "status": "ok",
                "reward": float(reward),
                "done": done,
                "info": info,
                "state": {
                    "day": next_state.day,
                    "cash_reserve": next_state.cash_reserve,
                    "inventory": next_state.inventory_levels
                }
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[API] {format % args}")

if __name__ == "__main__":
    port = 7860
    server = HTTPServer(("0.0.0.0", port), OpenEnvHandler)
    print(f"✅ Smart Factory Environment running on port {port}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    print(f"📊 Reset endpoint: POST http://localhost:{port}/reset")
    print(f"🎯 Step endpoint: POST http://localhost:{port}/step")
    print("🚀 Ready for Hackathon validation!")
    server.serve_forever()
