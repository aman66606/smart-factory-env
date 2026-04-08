"""
OpenEnv Hackathon Round 1 - Inference Script
Structured logging format required for evaluation
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from openai import OpenAI
from environment import SmartFactoryEnv
from tasks import get_task

# Environment variables (required for hackathon)
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

class LLMAgent:
    """Agent that uses LLM for decision making"""
    
    def __init__(self, task_name: str):
        self.client = OpenAI(
            base_url=API_BASE_URL,
            api_key=HF_TOKEN  # Using HF_TOKEN as API key
        )
        self.task_name = task_name
        self.conversation_history = []
        
    def get_action(self, state) -> np.ndarray:
        """Get action from LLM based on current state"""
        
        # Prepare state description for LLM
        state_desc = f"""
        Current Factory State:
        - Inventory: Electronics={state.inventory_levels['electronics']}, 
                     Mechanical={state.inventory_levels['mechanical']},
                     Raw Materials={state.inventory_levels['raw_materials']}
        - Supplier Reliability: {state.supplier_reliability:.2f}
        - Machine Health: {state.machine_health:.2f}
        - Cash Reserve: ${state.cash_reserve:.2f}k
        - Day: {state.day}
        - Task Difficulty: {self.task_name}
        
        Action Space (values 0-1, except reorder which is 0-2):
        1. Reorder Multiplier: How much to reorder (0=none, 1=normal, 2=double)
        2. Supplier Premium: Pay extra for reliability (0=no, 1=maximum)
        3. Maintenance: Invest in machine health (0=no, 1=maximum)
        
        Return ONLY three numbers separated by commas, like: 1.0,0.5,0.3
        """
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an inventory management expert. Return actions as three numbers: reorder_multiplier (0-2), supplier_premium (0-1), maintenance (0-1)."},
                    {"role": "user", "content": state_desc}
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            # Parse LLM response
            action_text = response.choices[0].message.content
            action_values = [float(x.strip()) for x in action_text.split(',')[:3]]
            
            # Ensure correct ranges
            action = np.array([
                np.clip(action_values[0], 0, 2),
                np.clip(action_values[1], 0, 1),
                np.clip(action_values[2], 0, 1)
            ])
            
        except Exception as e:
            # Fallback to heuristic if LLM fails
            print(f"LLM error: {e}, using fallback")
            action = self._heuristic_fallback(state)
        
        return action
    
    def _heuristic_fallback(self, state) -> np.ndarray:
        """Simple heuristic fallback policy"""
        inv_levels = list(state.inventory_levels.values())
        min_inventory = min(inv_levels)
        
        if min_inventory < 100:
            reorder = 1.5
        elif min_inventory < 250:
            reorder = 1.0
        else:
            reorder = 0.5
        
        supplier = 0.8 if state.supplier_reliability < 0.7 else 0.3
        maintenance = 0.8 if state.machine_health < 0.5 else 0.2
        
        return np.array([reorder, supplier, maintenance])


def run_episode(task_name: str, seed: int = 42):
    """
    Run a single episode with structured logging
    Required format: [START], [STEP], [END]
    """
    
    # [START] log - Required format
    print(json.dumps({
        "event": "START",
        "timestamp": datetime.now().isoformat(),
        "task": task_name,
        "seed": seed
    }))
    
    # Initialize environment and agent
    env, grader = get_task(task_name)
    agent = LLMAgent(task_name)
    
    state = env.reset()
    done = False
    step_count = 0
    total_reward = 0
    trajectory = []
    
    while not done and step_count < 365:
        # Get action from agent
        action = agent.get_action(state)
        
        # [STEP] log - Required format before each step
        print(json.dumps({
            "event": "STEP",
            "step": step_count,
            "action": action.tolist(),
            "timestamp": datetime.now().isoformat()
        }))
        
        # Take step
        next_state, reward, done, info = env.step(action)
        
        # [STEP] log - Required format after step
        print(json.dumps({
            "event": "STEP_RESULT",
            "step": step_count,
            "reward": float(reward),
            "done": done,
            "timestamp": datetime.now().isoformat()
        }))
        
        trajectory.append((state, reward, action, done, info))
        total_reward += reward
        state = next_state
        step_count += 1
    
    # Grade the trajectory
    results = grader.grade(trajectory)
    
    # [END] log - Required format
    print(json.dumps({
        "event": "END",
        "timestamp": datetime.now().isoformat(),
        "total_steps": step_count,
        "total_reward": float(total_reward),
        "score": float(results['score']),
        "passed": results['passed'],
        "metrics": {
            "avg_reward": results.get('avg_reward', 0),
            "stockout_rate": results.get('stockout_rate', 0),
            "machine_health": results.get('machine_health', 0)
        }
    }))
    
    return results


def main():
    """Main execution - runs all three tasks"""
    
    print(json.dumps({
        "event": "INFERENCE_START",
        "timestamp": datetime.now().isoformat(),
        "api_base_url": API_BASE_URL,
        "model_name": MODEL_NAME
    }))
    
    tasks = ['easy', 'medium', 'hard']
    all_results = []
    
    for task in tasks:
        print(json.dumps({
            "event": "TASK_START",
            "task": task,
            "timestamp": datetime.now().isoformat()
        }))
        
        results = run_episode(task)
        all_results.append(results)
        
        print(json.dumps({
            "event": "TASK_END",
            "task": task,
            "score": results['score'],
            "passed": results['passed']
        }))
    
    # Final summary
    avg_score = np.mean([r['score'] for r in all_results])
    print(json.dumps({
        "event": "INFERENCE_END",
        "timestamp": datetime.now().isoformat(),
        "average_score": float(avg_score),
        "task_results": all_results
    }))


if __name__ == "__main__":
    main()