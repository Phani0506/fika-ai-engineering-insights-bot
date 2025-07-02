import matplotlib.pyplot as plt
import pandas as pd
import os

def create_summary_chart(analyzed_data, output_path="data/report.png"):
    """
    Generates and saves a simple bar chart of key metrics.
    """
    print("---UTIL: Generating Chart---")
    metrics = analyzed_data.get('dora_metrics', {})
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    labels = ['Deploy Freq.', 'Lead Time (hrs)']
    values = [
        metrics.get('deployment_frequency', 0),
        metrics.get('lead_time_for_changes_hours', 0)
    ]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=['#4A90E2', '#50E3C2'])
    
    # Add labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 1), va='bottom', ha='center')

    ax.set_ylabel('Value')
    ax.set_title(f"Key Metrics: {analyzed_data.get('period', 'N/A').capitalize()} Report")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig) # Close the figure to free memory
    
    print(f"✅ Chart saved to {output_path}")
    return output_path