---
title: Smart Factory Inventory Management
emoji: 🏭
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
license: mit
---

# 🏭 Smart Factory Inventory Management Environment

An OpenEnv-compliant reinforcement learning environment for real-world inventory optimization in smart manufacturing.

## Features

- **Real-world simulation** with supply chain uncertainty
- **3 difficulty levels** (Easy → Medium → Hard)
- **Automatic grading** with task-specific metrics
- **Partial progress rewards** (0.0-1.0 normalized)
- **Baseline agent** with reproducible scores
- **Live interactive demo**

## Quick Start

The environment implements the OpenEnv API:
- `reset()` - Initialize factory state
- `step(action)` - Execute action, get reward
- `state()` - Current typed state

## Action Space
- **Reorder Multiplier** [0-2]: How aggressively to restock
- **Supplier Premium** [0-1]: Pay extra for reliable delivery  
- **Maintenance** [0-1]: Investment in machine health

## Try It Live
Use the interface above to simulate different scenarios and see how the AI agent performs!

## Technical Details
- Built with Python 3.9
- Gradio web interface
- Docker containerized
- OpenEnv compliant
