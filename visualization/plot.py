import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_sequence(sequence, head, disk_size=200):
    fig, ax = plt.subplots(figsize=(12, 6))  # Unified figure size
    
    # Initialize plot elements
    line, = ax.plot([], [], 'b-o', label="Disk Head Movement", alpha=0.7)
    current_point = ax.scatter([], [], color='red', s=100, label="Current Position")
    initial_point = ax.scatter([head], [0], color='green', s=100, label="Initial Position")
    
    # Configure axes
    ax.set_title(f"Disk Head Movement (Disk Size: {disk_size})", fontsize=14)
    ax.set_xlabel("Track Position", fontsize=12)
    ax.set_ylabel("Request Step", fontsize=12)
    ax.set_xlim(0, disk_size)
    ax.set_ylim(-0.5, len(sequence) - 0.5)
    ax.invert_yaxis()  # Top-to-bottom request order
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    
    # Animation update function
    def update(frame):
        x_data = sequence[:frame + 1]
        y_data = range(frame + 1)
        line.set_data(x_data, y_data)
        if frame < len(sequence):
            current_point.set_offsets([[sequence[frame], frame]])
        return line, current_point
    
    # Create and return animation
    ani = FuncAnimation(
        fig, update, frames=len(sequence),
        interval=500, blit=True, repeat=False
    )
    plt.tight_layout()
    return ani  # Critical: Return to prevent garbage collection

def plot_comparison(results, head, disk_size):
    fig, ax = plt.subplots(figsize=(12, 6))  # Unified figure size
    colors = plt.cm.tab10.colors  # Consistent color scheme
    
    # Plot each algorithm's path
    for i, (algo, seq, seek) in enumerate(results):
        ax.plot(seq, range(len(seq)), 'o-', 
                color=colors[i], 
                label=f"{algo} (Seek: {seek})", 
                alpha=0.7)
        ax.scatter([head], [-1], color=colors[i], marker='s', s=100)
    
    # Customize plot
    ax.set_title(f"Algorithm Comparison (Disk Size: {disk_size})", fontsize=14)
    ax.set_xlabel("Track Position", fontsize=12)
    ax.set_ylabel("Request Order", fontsize=12)
    ax.set_xlim(0, disk_size)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')
    
    # Annotate initial head position
    ax.annotate(
        f"Initial Head: {head}", 
        xy=(head, -1), 
        xytext=(head, -2), 
        ha='center', 
        arrowprops=dict(facecolor='black', shrink=0.05)
    )
    plt.tight_layout()
    plt.show()