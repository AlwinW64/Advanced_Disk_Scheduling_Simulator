import tkinter as tk
from tkinter import messagebox, ttk
from core.fcfs import fcfs
from core.sstf import sstf
from core.scan import scan
from core.cscan import cscan
from core.look import look
from core.clook import clook
from visualization.plot import animate_sequence
import matplotlib.pyplot as plt

class DiskSchedulingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input fields frame
        input_frame = ttk.LabelFrame(main_frame, text="Simulation Parameters", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Disk Requests
        ttk.Label(input_frame, text="Disk Requests (comma-separated):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_requests = ttk.Entry(input_frame, width=50)
        self.entry_requests.grid(row=0, column=1, padx=5, pady=5)
        
        # Initial Head Position
        ttk.Label(input_frame, text="Initial Head Position:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_head = ttk.Entry(input_frame, width=10)
        self.entry_head.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Disk Size
        ttk.Label(input_frame, text="Disk Size:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_disk_size = ttk.Entry(input_frame, width=10)
        self.entry_disk_size.insert(0, "200")
        self.entry_disk_size.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Algorithm Selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.algorithm_var = tk.StringVar(value="FCFS")
        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        self.algorithm_menu = ttk.OptionMenu(input_frame, self.algorithm_var, *algorithms)
        self.algorithm_menu.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Direction Selection
        ttk.Label(input_frame, text="Direction:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.direction_var = tk.StringVar(value="right")
        directions = ["right", "left"]
        self.direction_menu = ttk.OptionMenu(input_frame, self.direction_var, *directions)
        self.direction_menu.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Buttons
        self.run_button = ttk.Button(button_frame, text="Run Simulation", command=self.start_simulation)
        self.run_button.pack(side=tk.LEFT, padx=10)
        
        self.compare_button = ttk.Button(button_frame, text="Compare Algorithms", command=self.open_compare_window)
        self.compare_button.pack(side=tk.LEFT, padx=10)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(10,0))
    
    def start_simulation(self):
        try:
            requests = list(map(int, self.entry_requests.get().split(',')))
            head = int(self.entry_head.get())
            algorithm = self.algorithm_var.get()
            disk_size = int(self.entry_disk_size.get() or 200)
            
            if disk_size <= 0:
                raise ValueError("Disk size must be positive")
            
            if any(r < 0 or r >= disk_size for r in requests):
                raise ValueError(f"All requests must be between 0 and {disk_size-1}")

            if algorithm == "FCFS":
                sequence, total_seek_time = fcfs(requests.copy(), head)
            elif algorithm == "SSTF":
                sequence, total_seek_time = sstf(requests.copy(), head)
            elif algorithm == "SCAN":
                sequence, total_seek_time = scan(requests.copy(), head, self.direction_var.get(), disk_size)
            elif algorithm == "C-SCAN":
                sequence, total_seek_time = cscan(requests.copy(), head, self.direction_var.get(), disk_size)
            elif algorithm == "LOOK":
                sequence, total_seek_time = look(requests.copy(), head, self.direction_var.get(), disk_size)
            elif algorithm == "C-LOOK":
                sequence, total_seek_time = clook(requests.copy(), head, self.direction_var.get(), disk_size)
            else:
                raise ValueError("Invalid algorithm selected")

            average_seek_time = total_seek_time / len(requests)
            throughput = len(requests) / total_seek_time if total_seek_time != 0 else 0

            result_text = (
                f"Algorithm: {algorithm}\n"
                f"Sequence: {sequence}\n"
                f"Total Seek Time: {total_seek_time}\n"
                f"Average Seek Time: {average_seek_time:.2f}\n"
                f"Throughput: {throughput:.2f} requests per unit time\n"
                f"Disk Size: {disk_size}"
            )
            messagebox.showinfo("Simulation Result", result_text)
            
            self.status_var.set("Running animation...")
            self.root.update()
            animate_sequence(sequence, head, disk_size)
            self.status_var.set("Simulation completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error in simulation")
    
    def open_compare_window(self):
        # Create a new top-level window
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Compare Algorithms")
        compare_window.geometry("400x300")
        
        # Frame for inputs
        input_frame = ttk.Frame(compare_window, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Number of algorithms to compare
        ttk.Label(input_frame, text="Number of Algorithms:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_algorithms = tk.IntVar(value=2)
        spinbox = ttk.Spinbox(input_frame, from_=2, to=6, textvariable=self.num_algorithms, width=5, command=lambda: self.update_algorithm_dropdowns(input_frame))
        spinbox.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Algorithm selection labels
        ttk.Label(input_frame, text="Select Algorithms:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Placeholder for algorithm dropdowns
        self.algorithm_vars = []
        self.algorithm_menus = []
        for i in range(6):
            var = tk.StringVar(value="FCFS")
            self.algorithm_vars.append(var)
            menu = ttk.OptionMenu(input_frame, var, "FCFS", *["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"])
            menu.grid(row=i+2, column=1, sticky=tk.W, pady=5)
            self.algorithm_menus.append(menu)
            if i >= 2:
                menu.grid_remove()
        
        # Button to confirm selection
        ttk.Button(input_frame, text="Run Comparison", command=lambda: self.run_comparison(compare_window)).grid(row=8, columnspan=2, pady=20)
    
    def update_algorithm_dropdowns(self, frame):
        num = self.num_algorithms.get()
        for i, menu in enumerate(self.algorithm_menus):
            if i < num:
                menu.grid()
            else:
                menu.grid_remove()
    
    def run_comparison(self, window):
        try:
            # Get user inputs
            requests_str = self.entry_requests.get()
            head_str = self.entry_head.get()
            disk_size_str = self.entry_disk_size.get()
            
            if not requests_str or not head_str:
                raise ValueError("Please fill in all fields (requests and head position)")
            
            requests = list(map(int, requests_str.split(',')))
            head = int(head_str)
            disk_size = int(disk_size_str or 200)
            num_algorithms = self.num_algorithms.get()
            
            # Validate inputs
            if any(r < 0 or r >= disk_size for r in requests):
                raise ValueError(f"Requests must be between 0 and {disk_size-1}")
            
            # Collect selected algorithms
            algorithms = [self.algorithm_vars[i].get() for i in range(num_algorithms)]
            
            # Run simulations
            results = []
            for algo in algorithms:
                if algo == "FCFS":
                    seq, seek = fcfs(requests.copy(), head)
                elif algo == "SSTF":
                    seq, seek = sstf(requests.copy(), head)
                elif algo == "SCAN":
                    seq, seek = scan(requests.copy(), head, self.direction_var.get(), disk_size)
                elif algo == "C-SCAN":
                    seq, seek = cscan(requests.copy(), head, self.direction_var.get(), disk_size)
                elif algo == "LOOK":
                    seq, seek = look(requests.copy(), head, self.direction_var.get(), disk_size)
                elif algo == "C-LOOK":
                    seq, seek = clook(requests.copy(), head, self.direction_var.get(), disk_size)
                results.append((algo, seq, seek))
            
            # Close the comparison window
            window.destroy()
            
            # Plot combined results
            self.plot_comparison(results, head, disk_size)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def plot_comparison(self, results, head, disk_size):
        plt.figure(figsize=(12, 6))
        colors = ['b', 'g', 'r', 'c', 'm', 'y']
        
        for i, (algo, seq, seek) in enumerate(results):
            plt.plot(seq, range(len(seq)), 'o-', color=colors[i], label=f"{algo} (Seek: {seek})")
        
        plt.scatter([head], [-1], color='k', marker='s', s=100, label="Initial Head")
        plt.title(f"Algorithm Comparison (Disk Size: {disk_size})")
        plt.xlabel("Track Position")
        plt.ylabel("Request Order")
        plt.xlim(0, disk_size)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.show()
    
    def clear_fields(self):
        self.entry_requests.delete(0, tk.END)
        self.entry_head.delete(0, tk.END)
        self.entry_disk_size.delete(0, tk.END)
        self.entry_disk_size.insert(0, "200")
        self.algorithm_var.set("FCFS")
        self.direction_var.set("right")
        self.status_var.set("Fields cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingSimulator(root)
    root.mainloop()