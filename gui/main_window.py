import tkinter as tk
from tkinter import messagebox, ttk
from core.fcfs import fcfs
from core.sstf import sstf
from core.scan import scan
from core.cscan import cscan
from core.look import look
from core.clook import clook
from visualization.plot import animate_sequence

class DiskSchedulingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = screen_width // 2
        window_height = screen_height

        self.root.geometry(f"{window_width}x{window_height}+0+0")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        
        self.create_widgets()

    def open_new_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Compare Disk Scheduling Algorithms")
        new_window.geometry("600x600+600+200")

        # Input Fields
        tk.Label(new_window, text="Enter Requests (comma separated):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.request_entry = tk.Entry(new_window, width=40)
        self.request_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(new_window, text="Initial Head Position:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.head_entry = tk.Entry(new_window)
        self.head_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(new_window, text="Disk Size:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.disk_size_entry = tk.Entry(new_window)
        self.disk_size_entry.insert(0, "200")
        self.disk_size_entry.grid(row=2, column=1, padx=10, pady=5)

        # Algorithm Checkboxes
        self.algorithm_vars = {}
        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        tk.Label(new_window, text="Select Algorithms for Comparison:").grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        for i, algo in enumerate(algorithms):
            var = tk.BooleanVar()
            self.algorithm_vars[algo] = var
            tk.Checkbutton(new_window, text=algo, variable=var).grid(row=4+i, column=0, columnspan=2, sticky='w', padx=20)

        # Compare Button
        tk.Button(new_window, text="Compare Algorithms", command=self.compare_algorithms).grid(row=10, column=0, columnspan=2, pady=20)

        # Text Box for Results
        self.result_text = tk.Text(new_window, height=15, width=70, wrap='word', state='disabled', bg="#f5f5f5", relief="solid", borderwidth=1)
        self.result_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        # Close Button
        tk.Button(new_window, text="Close", command=new_window.destroy).grid(row=12, column=0, columnspan=2, pady=10)


    # Perform Algorithm Comparison
    def compare_algorithms(self):
        try:
            requests = list(map(int, self.request_entry.get().split(',')))
            head = int(self.head_entry.get())
            disk_size = int(self.disk_size_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        selected_algorithms = [algo for algo, var in self.algorithm_vars.items() if var.get()]
        if not selected_algorithms:
            messagebox.showwarning("No Algorithm Selected", "Please select at least one algorithm.")
            return

        results = {}
        output_text = "Comparison Results:\n\n"
        
        for algo in selected_algorithms:
            if algo == "FCFS":
                sequence, total_seek_time = fcfs(requests.copy(), head)
            elif algo == "SSTF":
                sequence, total_seek_time = sstf(requests.copy(), head)
            elif algo == "SCAN":
                sequence, total_seek_time = scan(requests.copy(), head, "right", disk_size)
            elif algo == "C-SCAN":
                sequence, total_seek_time = cscan(requests.copy(), head, "right", disk_size)
            elif algo == "LOOK":
                sequence, total_seek_time = look(requests.copy(), head, "right", disk_size)
            elif algo == "C-LOOK":
                sequence, total_seek_time = clook(requests.copy(), head, "right", disk_size)

            average_seek_time = total_seek_time / len(requests) if requests else 0
            throughput = len(requests) / total_seek_time if total_seek_time != 0 else 0

            results[algo] = (sequence, total_seek_time, average_seek_time, throughput)

            output_text += (
                f"Algorithm: {algo}\n"
                f"Sequence: {sequence}\n"
                f"Total Seek Time: {total_seek_time}\n"
                f"Average Seek Time: {average_seek_time:.2f}\n"
                f"Throughput: {throughput:.2f} requests per unit time\n"
                f"{'-'*60}\n"
            )

        self.display_results(output_text)

    # Display results in the Text widget
    def display_results(self, text):
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state='disabled')

    
    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        label = ttk.Label(main_frame, 
                           text="Advanced Disk Scheduling Simulator", 
                           font=("Arial", 16, "bold"),
                           foreground="black")
        label.pack(pady=20)

        label = tk.Label(main_frame, 
                          text="What is Disk Scheduling?\nDisk scheduling is done by operating systems to schedule I/O requests arriving for the disk.\nDisk scheduling is also known as I/O scheduling.", 
                          font=("Arial", 14),
                          anchor="center",
                          borderwidth=1, 
                          relief="solid",
                          pady=20)
        label.pack(pady=10)

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
        self.entry_disk_size.insert(0, "200")  # Default value
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
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=10)


        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(10,0))

        

        # Result Label to display results
        self.result_label = ttk.Label(main_frame, text="", justify=tk.LEFT, anchor="w", background="#f0f0f0", font=("Arial", 10))
        self.result_label.pack(fill=tk.BOTH, padx=10, pady=10)

        
        self.new_window_button = ttk.Button(button_frame, text="Compare Algorithms", command=self.open_new_window)
        self.new_window_button.pack(side=tk.BOTTOM, padx=10)
    
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

            # Display results on window
            self.result_label.config(text=result_text)
            self.status_var.set("Running animation...")
            self.root.update()
            animate_sequence(sequence, head, disk_size)
            self.status_var.set("Simulation completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error in simulation")
    
    def clear_fields(self):
        self.entry_requests.delete(0, tk.END)
        self.entry_head.delete(0, tk.END)
        self.entry_disk_size.delete(0, tk.END)
        self.entry_disk_size.insert(0, "200")
        self.algorithm_var.set("FCFS")
        self.direction_var.set("right")
        self.status_var.set("Fields cleared")
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingSimulator(root)
    root.mainloop()

#v2