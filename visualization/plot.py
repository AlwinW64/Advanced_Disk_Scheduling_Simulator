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

    line, = ax.plot([], [], 'b-o', label="Disk Head Movement")
    current_point = ax.scatter([], [], color='r', s=100, label="Current Position")
    initial_point = ax.scatter([head], [0], color='g', s=100, label="Initial Position")

    ax.set_title(f"Disk Head Movement Animation (Disk Size: {disk_size})")
    ax.set_xlabel("Track Position")
    ax.set_ylabel("Request Step")
    ax.set_xlim(0, disk_size)
    ax.set_ylim(-0.5, len(sequence) - 0.5)
    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    def update(frame):
        x_data = sequence[:frame + 1]
        y_data = list(range(frame + 1))
        line.set_data(x_data, y_data)
        if frame < len(sequence):
            current_point.set_offsets([[sequence[frame], frame]])
        return line, current_point

    ani = FuncAnimation(fig, update, frames=len(sequence),
                        interval=500, blit=True, repeat=False)

    plt.tight_layout()
    plt.show()
    return ani
