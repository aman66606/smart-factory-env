from flask import Flask, jsonify, request
import numpy as np
from environment import SmartFactoryEnv

app = Flask(__name__)
env = SmartFactoryEnv()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/reset', methods=['POST'])
def reset():
    global env
    data = request.get_json() or {}
    env = SmartFactoryEnv(difficulty=data.get('difficulty', 'medium'))
    state = env.reset()
    return jsonify({"day": state.day, "inventory": state.inventory_levels})

@app.route('/step', methods=['POST'])
def step():
    data = request.get_json()
    action = data.get('action', [1.0, 0.5, 0.3])
    next_state, reward, done, info = env.step(np.array(action))
    return jsonify({"reward": reward, "done": done})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
