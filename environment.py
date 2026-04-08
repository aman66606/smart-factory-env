import numpy as np
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class FactoryState:
    inventory_levels: Dict[str, int]
    pending_orders: Dict[str, int]
    supplier_reliability: float
    machine_health: float
    cash_reserve: float
    day: int
    total_cost: float
    stockout_penalties: float
    holding_costs: float

class SmartFactoryEnv:
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.reset()
    
    def reset(self):
        self.state = FactoryState(
            inventory_levels={'electronics': 500, 'mechanical': 500, 'raw_materials': 500},
            pending_orders={'electronics': 0, 'mechanical': 0, 'raw_materials': 0},
            supplier_reliability=0.85,
            machine_health=1.0,
            cash_reserve=1000.0,
            day=0,
            total_cost=0.0,
            stockout_penalties=0.0,
            holding_costs=0.0
        )
        return self.state
    
    def step(self, action):
        reorder_mult = np.clip(action[0], 0, 2)
        supplier_premium = np.clip(action[1], 0, 1)
        maintenance = np.clip(action[2], 0, 1)
        
        # Simple reward calculation
        reward = 0.5 + (supplier_premium * 0.3) + (maintenance * 0.2)
        reward = np.clip(reward, 0, 1)
        
        self.state.day += 1
        done = self.state.day >= 365
        
        info = {'day': self.state.day, 'reward': reward}
        
        return self.state, reward, done, info
    
    def state(self):
        return self.state
