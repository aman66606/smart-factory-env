"""
Gradio web interface for Hugging Face Spaces deployment
"""

import gradio as gr
import numpy as np
from environment import SmartFactoryEnv
from tasks import get_task
from inference import HeuristicInventoryAgent
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def run_simulation(task_name: str, num_days: int, render_progress: bool = True):
    """Run simulation and return results"""
    env, grader = get_task(task_name)
    agent = HeuristicInventoryAgent(seed=42)
    
    state = env.reset()
    trajectory = []
    rewards = []
    inventory_history = {'electronics': [], 'mechanical': [], 'raw_materials': []}
    
    for day in range(min(num_days, 365)):
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        
        trajectory.append((state, reward, action, done, info))
        rewards.append(reward)
        
        # Record inventory levels
        for product in inventory_history.keys():
            inventory_history[product].append(state.inventory_levels[product])
        
        state = next_state
        if done:
            break
    
    # Grade the trajectory
    results = grader.grade(trajectory)
    
    # Create inventory plot
    fig, ax = plt.subplots(figsize=(10, 5))
    for product, history in inventory_history.items():
        ax.plot(history, label=product, linewidth=2)
    ax.set_xlabel('Day')
    ax.set_ylabel('Inventory Level (units)')
    ax.set_title(f'Inventory Levels Over Time - {task_name.upper()} Task')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode()
    buf.close()
    
    # Format results
    summary = f"""
## 📊 Simulation Results - {task_name.upper()} Task

### Performance Metrics
- **Score**: {results['score']:.3f} / 1.0
- **Passed**: {'✅ Yes' if results['passed'] else '❌ No'}
- **Average Reward**: {results['avg_reward']:.3f}
- **Total Cost**: ${results.get('total_cost', 0):.2f}

### Task-Specific Metrics
- **Stockout Rate**: {results.get('stockout_rate', 0):.3f}
- **Machine Health**: {results.get('machine_health', 0):.3f}
- **Cash Remaining**: ${results.get('cash_remaining', 0)*1000:.2f}

### Baseline Comparison
- Easy target: 0.85 | Medium: 0.70 | Hard: 0.55
"""
    
    return summary, f"data:image/png;base64,{plot_base64}"


# Create Gradio interface
with gr.Blocks(title="Smart Factory Inventory Management", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏭 Smart Factory Inventory Management Environment
    
    Train AI agents to optimize real-world factory operations! This environment simulates 
    inventory management with **supply chain uncertainty**, **machine degradation**, and 
    **demand volatility**.
    
    ### How it works:
    1. Choose a difficulty level (Easy → Medium → Hard)
    2. The AI agent controls: reorder quantity, supplier reliability investment, and maintenance
    3. Goal: Minimize costs while maintaining service levels
    4. Reward is normalized to [0, 1] based on performance
    
    ### Action Space (3 dimensions):
    - **Reorder Multiplier** [0-2]: How aggressively to restock
    - **Supplier Premium** [0-1]: Pay extra for reliable delivery
    - **Maintenance** [0-1]: Investment in machine health
    """)
    
    with gr.Row():
        with gr.Column():
            task_selector = gr.Radio(
                choices=['easy', 'medium', 'hard'],
                label="Task Difficulty",
                value='medium'
            )
            days_slider = gr.Slider(
                minimum=30, maximum=365, value=180, step=30,
                label="Simulation Days"
            )
            run_button = gr.Button("🚀 Run Simulation", variant="primary")
        
        with gr.Column():
            output_text = gr.Markdown("Results will appear here...")
    
    with gr.Row():
        output_plot = gr.Image(label="Inventory Trends", type="pil")
    
    run_button.click(
        fn=run_simulation,
        inputs=[task_selector, days_slider],
        outputs=[output_text, output_plot]
    )
    
    gr.Markdown("""
    ---
    ### 📈 Understanding the Results
    
    - **Score (0-1)**: Overall performance - higher is better
    - **Stockout Rate**: Frequency of running out of inventory
    - **Machine Health**: Equipment condition (affects production efficiency)
    - **Total Cost**: Accumulated holding, stockout, and reorder costs
    
    ### 🎯 Task Requirements
    
    | Difficulty | Target Score | Challenge |
    |------------|--------------|-----------|
    | Easy | 0.85 | Stable demand, reliable suppliers |
    | Medium | 0.70 | Variable demand, occasional issues |
    | Hard | 0.55 | High volatility, unreliable suppliers |
    
    ### 🔬 For AI Researchers
    
    This environment implements the **OpenEnv specification**:
    - `reset()` → Initial state
    - `step(action)` → (next_state, reward, done, info)
    - `state()` → Current typed state
    
    **Baseline score** (heuristic agent): ~0.72 on easy, ~0.58 on medium, ~0.45 on hard
    """)

if __name__ == "__main__":
    demo.launch()