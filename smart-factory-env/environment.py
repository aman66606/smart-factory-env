"""
Smart Factory Inventory Management Environment
OpenEnv-compliant for Hackathon Round 1
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
import random


@dataclass
class FactoryState:
    """Typed state representation - Required for OpenEnv"""
    inventory_levels: Dict[str, int]
    pending_orders: Dict[str, int]
    supplier_reliability: float
    machine_health: float
    cash_reserve: float
    day: int
    total_cost: float
    stockout_penalties: float
    holding_costs: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SmartFactoryEnv:
    """
    Real-world inventory management environment
    Actions: [reorder_quantity, supplier_choice, maintenance_investment]
    """
    
    def __init__(self, difficulty: str = "medium", config: Optional[Dict] = None):
        self.difficulty = difficulty
        self.config = config or self._default_config()
        self._setup_difficulty()
        self.reset()
    
    def _default_config(self) -> Dict:
        return {
            'max_days': 365,
            'demand_mean': {'electronics': 100, 'mechanical': 150, 'raw_materials': 200},
            'demand_std': {'electronics': 30, 'mechanical': 40, 'raw_materials': 50},
            'lead_time': {'electronics': 5, 'mechanical': 3, 'raw_materials': 2},
            'holding_cost_rate': 0.02,
            'stockout_penalty': 50.0,
            'max_inventory': 1000,
            'reorder_point': {'electronics': 200, 'mechanical': 250, 'raw_materials': 300}
        }
    
    def _setup_difficulty(self):
        """Adjust parameters based on difficulty"""
        if self.difficulty == 'easy':
            self.config['demand_std'] = {k: v*0.5 for k, v in self.config['demand_std'].items()}
            self.config['supplier_reliability'] = 0.95
        elif self.difficulty == 'medium':
            self.config['demand_std'] = {k: v*1.0 for k, v in self.config['demand_std'].items()}
            self.config['supplier_reliability'] = 0.85
        else:  # hard
            self.config['demand_std'] = {k: v*1.5 for k, v in self.config['demand_std'].items()}
            self.config['supplier_reliability'] = 0.70
    
    def reset(self) -> FactoryState:
        """Reset environment to initial state"""
        self.state = FactoryState(
            inventory_levels={'electronics': 500, 'mechanical': 500, 'raw_materials': 500},
            pending_orders={'electronics': 0, 'mechanical': 0, 'raw_materials': 0},
            supplier_reliability=self.config.get('supplier_reliability', 0.85),
            machine_health=1.0,
            cash_reserve=1000.0,
            day=0,
            total_cost=0.0,
            stockout_penalties=0.0,
            holding_costs=0.0
        )
        return self.state
    
    def step(self, action: np.ndarray) -> Tuple[FactoryState, float, bool, Dict]:
        """Execute one time step"""
        reorder_mult = np.clip(action[0], 0, 2)
        supplier_premium = np.clip(action[1], 0, 1)
        maintenance = np.clip(action[2], 0, 1)
        
        # Generate demand
        daily_demand = self._generate_demand()
        
        # Process inventory and calculate costs
        stockout_cost = 0
        holding_cost = 0
        
        for product in ['electronics', 'mechanical', 'raw_materials']:
            demand = daily_demand[product]
            inventory = self.state.inventory_levels[product]
            
            if inventory >= demand:
                self.state.inventory_levels[product] -= demand
            else:
                shortage = demand - inventory
                self.state.inventory_levels[product] = 0
                stockout_cost += shortage * self.config['stockout_penalty']
            
            holding_cost += self.state.inventory_levels[product] * self.config['holding_cost_rate']
        
        # Calculate reward (normalized to [0, 1])
        reward = self._calculate_reward(stockout_cost, holding_cost, maintenance)
        
        # Update state
        self.state.day += 1
        self.state.total_cost += stockout_cost + holding_cost
        self.state.stockout_penalties += stockout_cost
        self.state.holding_costs += holding_cost
        
        done = self.state.day >= self.config['max_days']
        
        info = {
            'day': self.state.day,
            'stockout_cost': stockout_cost,
            'holding_cost': holding_cost,
            'action': action.tolist()
        }
        
        return self.state, reward, done, info
    
    def _generate_demand(self) -> Dict[str, int]:
        """Generate daily demand"""
        demand = {}
        for product in ['electronics', 'mechanical', 'raw_materials']:
            mean = self.config['demand_mean'][product]
            std = self.config['demand_std'][product]
            base_demand = np.random.normal(mean, std)
            demand[product] = max(0, int(base_demand))
        return demand
    
    def _calculate_reward(self, stockout_cost: float, holding_cost: float, maintenance: float) -> float:
        """Calculate normalized reward [0, 1]"""
        max_stockout = 5000
        max_holding = 2000
        
        cost_score = 1.0 - (stockout_cost / max_stockout + holding_cost / max_holding) / 2
        cost_score = np.clip(cost_score, 0, 1)
        
        maintenance_bonus = maintenance * 0.2
        reward = cost_score * 0.8 + maintenance_bonus
        
        return np.clip(reward, 0, 1)
    
    def state(self) -> FactoryState:
        """Return current state"""
        return self.state