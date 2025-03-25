import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_sequence(sequence, head, disk_size=200):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Initialize empty line and point
    line, = ax.plot([], [], 'b-o', label="Disk Head Movement")
    current_point = ax.scatter([], [], color='r', s=100, label="Current Position")
    initial_point = ax.scatter([head], [0], color='g', s=100, label="Initial Position")
    
    # Set up axes
    ax.set_title(f"Disk Head Movement Animation (Disk Size: {disk_size})")
    ax.set_xlabel("Track Position")
    ax.set_ylabel("Request Step")
    ax.set_xlim(0, disk_size)
    ax.set_ylim(-0.5, len(sequence)-0.5)
    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Animation function
    def update(frame):
        x_data = sequence[:frame+1]
        y_data = list(range(frame+1))
        line.set_data(x_data, y_data)
        if frame < len(sequence):
            current_point.set_offsets([[sequence[frame], frame]])
        return line, current_point
    
    # Create animation
    ani = FuncAnimation(fig, update, frames=len(sequence), 
                        interval=500, blit=True, repeat=False)
    
    plt.tight_layout()
    plt.show()
    return ani