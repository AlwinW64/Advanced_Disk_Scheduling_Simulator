import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def add_turnaround_point(sequence, head, disk_size=200):
    modified_seq = [head]
    
    for i in range(len(sequence) - 1):
        curr = sequence[i]
        next_ = sequence[i + 1]
        modified_seq.append(curr)

        # Detect direction change
        if (next_ - curr) * (curr - modified_seq[-2]) < 0:
            if curr < next_ and (disk_size - 1) not in modified_seq:
                modified_seq.append(disk_size - 1)
            elif curr > next_ and 0 not in modified_seq:
                modified_seq.append(0)

    modified_seq.append(sequence[-1])
    
    # Additional check: if it's SCAN or C-SCAN but didn't reach end/start
    if sequence[0] > head and (0 not in sequence and 0 not in modified_seq):
        modified_seq.insert(1, 0)
    elif sequence[0] < head and ((disk_size - 1) not in sequence and (disk_size - 1) not in modified_seq):
        modified_seq.insert(1, disk_size - 1)
    
    return modified_seq
# Animation function
def animate_sequence(sequence, head, disk_size=200):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Optional: Position the animation window to the right
    manager = plt.get_current_fig_manager()
    try:
        screen_width = manager.window.winfo_screenwidth()
        screen_height = manager.window.winfo_screenheight()
        manager.window.geometry(f"{screen_width//2}x{screen_height}+{screen_width//2}+0")
    except:
        pass  # For non-GUI environments

    # Create the line plot starting from head position
    line, = ax.plot([head], [-1], 'b-o', label="Disk Head Movement")  # Start at y=-1
    current_point = ax.scatter([], [], color='r', s=100, label="Current Position")
    initial_point = ax.scatter([head], [-1], color='g', s=100, label="Initial Position")  # Position at y=-1

    # Get unique points from sequence for x-axis ticks
    unique_points = sorted(set(sequence + [head]))
    
    ax.set_title(f"Disk Head Movement Animation (Disk Size: {disk_size})")
    ax.set_xlabel("Track Position")
    ax.set_xlim(0, disk_size)
    ax.set_ylim(-1.5, len(sequence) - 0.5)  # Extend y-axis to show initial position
    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Set x-axis ticks to only show the points that are actually used
    ax.set_xticks(unique_points)
    ax.set_xticklabels(unique_points, rotation=45)  # Rotate labels for better readability
    
    # Move x-axis to top and hide y-axis
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.yaxis.set_visible(False)
    
    # Remove y-axis label
    ax.set_ylabel("")

    def update(frame):
        if frame == 0:
            # First frame: just show initial head position
            x_data = [head]
            y_data = [-1]
            current_point.set_offsets([[head, -1]])
        else:
            # Subsequent frames: show movement from head to sequence points
            x_data = [head] + sequence[:frame]
            y_data = [-1] + list(range(frame))
            if frame < len(sequence):
                current_point.set_offsets([[sequence[frame-1], frame-1]])
        
        line.set_data(x_data, y_data)
        return line, current_point

    ani = FuncAnimation(fig, update, frames=len(sequence) + 1,  # +1 to include initial position
                        interval=500, blit=True, repeat=False)

    plt.tight_layout()
    plt.show()
    return ani
