"""
Task definitions with automatic grading for each difficulty level
"""

import numpy as np
from typing import Dict, Any, Tuple
from environment import SmartFactoryEnv


class TaskGrader:
    """Base grader class"""
    
    def grade(self, trajectory: list) -> Dict[str, Any]:
        """Grade a full episode trajectory"""
        raise NotImplementedError


class EasyTaskGrader(TaskGrader):
    """Easy: Focus on basic inventory management"""
    
    def grade(self, trajectory: list) -> Dict[str, Any]:
        total_reward = sum(step[1] for step in trajectory)
        avg_reward = total_reward / len(trajectory)
        
        # Check specific metrics
        final_state = trajectory[-1][0]
        stockout_rate = final_state.stockout_penalties / 5000  # Normalized
        
        score = avg_reward * 0.6 + (1 - min(1, stockout_rate)) * 0.4
        
        return {
            'score': min(1.0, max(0.0, score)),
            'avg_reward': avg_reward,
            'stockout_rate': stockout_rate,
            'total_cost': final_state.total_cost,
            'passed': score >= 0.85
        }


class MediumTaskGrader(TaskGrader):
    """Medium: Balance costs with supplier reliability"""
    
    def grade(self, trajectory: list) -> Dict[str, Any]:
        total_reward = sum(step[1] for step in trajectory)
        avg_reward = total_reward / len(trajectory)
        
        final_state = trajectory[-1][0]
        stockout_rate = final_state.stockout_penalties / 10000
        machine_health = final_state.machine_health
        
        # Bonus for maintaining machine health
        machine_bonus = machine_health * 0.2
        
        score = avg_reward * 0.5 + (1 - min(1, stockout_rate)) * 0.3 + machine_bonus
        
        return {
            'score': min(1.0, max(0.0, score)),
            'avg_reward': avg_reward,
            'stockout_rate': stockout_rate,
            'machine_health': machine_health,
            'total_cost': final_state.total_cost,
            'passed': score >= 0.70
        }


class HardTaskGrader(TaskGrader):
    """Hard: Optimize all aspects under high uncertainty"""
    
    def grade(self, trajectory: list) -> Dict[str, Any]:
        total_reward = sum(step[1] for step in trajectory)
        avg_reward = total_reward / len(trajectory)
        
        final_state = trajectory[-1][0]
        stockout_rate = final_state.stockout_penalties / 15000
        holding_efficiency = 1 - (final_state.holding_costs / 10000)
        cash_remaining = final_state.cash_reserve / 1000  # Normalized
        
        # Complex scoring with multiple factors
        score = (avg_reward * 0.4 + 
                (1 - min(1, stockout_rate)) * 0.2 +
                max(0, holding_efficiency) * 0.2 +
                max(0, cash_remaining) * 0.2)
        
        return {
            'score': min(1.0, max(0.0, score)),
            'avg_reward': avg_reward,
            'stockout_rate': stockout_rate,
            'holding_efficiency': holding_efficiency,
            'cash_remaining': cash_remaining,
            'machine_health': final_state.machine_health,
            'total_cost': final_state.total_cost,
            'passed': score >= 0.55
        }


def get_task(task_name: str) -> Tuple[SmartFactoryEnv, TaskGrader]:
    """Get environment and grader for a specific task"""
    
    if task_name == 'easy':
        env = SmartFactoryEnv(difficulty='easy')
        grader = EasyTaskGrader()
    elif task_name == 'medium':
        env = SmartFactoryEnv(difficulty='medium')
        grader = MediumTaskGrader()
    elif task_name == 'hard':
        env = SmartFactoryEnv(difficulty='hard')
        grader = HardTaskGrader()
    else:
        raise ValueError(f"Unknown task: {task_name}")
    
    return env, grader