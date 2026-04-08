from flask import Flask, jsonify, request
import numpy as np
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from environment import SmartFactoryEnv

app = Flask(__name__)

# Global environment instance
env = SmartFactoryEnv(difficulty="medium")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "openenv": "compliant",
        "tasks": ["easy", "medium", "hard"]
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset environment"""
    global env
    try:
        data = request.get_json() or {}
        difficulty = data.get('difficulty', 'medium')
        env = SmartFactoryEnv(difficulty=difficulty)
        state = env.reset()
        
        return jsonify({
            "status": "ok",
            "state": {
                "day": state.day,
                "inventory": state.inventory_levels,
                "cash_reserve": state.cash_reserve,
                "machine_health": state.machine_health,
                "supplier_reliability": state.supplier_reliability
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/step', methods=['POST'])
def step():
    """Take an action"""
    global env
    try:
        data = request.get_json()
        action = data.get('action', [1.0, 0.5, 0.3])
        
        # Ensure action is numpy array
        action = np.array(action)
        
        # Take step
        next_state, reward, done, info = env.step(action)
        
        return jsonify({
            "reward": float(reward),
            "done": done,
            "info": info,
            "state": {
                "day": next_state.day,
                "inventory": next_state.inventory_levels,
                "cash_reserve": next_state.cash_reserve
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "name": "Smart Factory Inventory Management",
        "openenv": "compliant",
        "endpoints": ["/health", "/reset", "/step"],
        "tasks": ["easy", "medium", "hard"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    print(f"Starting Flask server on port {port}")
    print(f"Health check: http://localhost:{port}/health")
    app.run(host='0.0.0.0', port=port, debug=False)
