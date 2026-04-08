# 🏭 Smart Factory Inventory Management Environment

An **OpenEnv-compliant** reinforcement learning environment for real-world inventory optimization in smart manufacturing.

## 🌟 Overview

This environment simulates a factory managing multiple product inventories with:
- **Uncertain demand** (seasonal + random fluctuations)
- **Supplier reliability issues** (late or failed deliveries)
- **Machine degradation** (affects production capacity)
- **Financial constraints** (cash reserves, holding costs, stockout penalties)

**Perfect for:** Supply chain optimization, inventory management AI, production planning.

## 📋 Environment Specification

### Action Space (Box(3), continuous)
| Action | Range | Description |
|--------|-------|-------------|
| `reorder_multiplier` | [0, 2] | How aggressively to reorder (0=none, 2=double safety stock) |
| `supplier_premium` | [0, 1] | Extra payment for reliable delivery (0=standard, 1=premium) |
| `maintenance` | [0, 1] | Investment in machine maintenance |

### Observation Space (Dict)
```python
{
    'inventory_levels': {'electronics': int, 'mechanical': int, 'raw_materials': int},
    'pending_orders': {...},  # Backlogged demand
    'supplier_reliability': float,  # 0-1, probability of on-time delivery
    'machine_health': float,  # 0-1, current equipment condition
    'cash_reserve': float,  # Available cash in $k
    'day': int,  # Current day (0-365)
    'total_cost': float  # Accumulated costs
}