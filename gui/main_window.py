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
        
        ### Algorithms description
        self.algorithm_descriptions = {
        "FCFS": "First-Come-First-Served (FCFS):\n"
                "• Services requests in the order they arrive\n"
                "• Simple but may result in high seek times\n"
                "• No starvation, but poor performance for scattered requests",
                
        "SSTF": "Shortest Seek Time First (SSTF):\n"
                "• Services the nearest request to the current head position\n"
                "• Reduces average seek time compared to FCFS\n"
                "• May cause starvation for distant requests",
                
        "SCAN": "SCAN (Elevator Algorithm):\n"
                "• Moves the head back and forth across the disk\n"
                "• Services requests in one direction until the end, then reverses\n"
                "• Fairer than SSTF but may have longer wait times",
                
        "C-SCAN": "C-SCAN (Circular SCAN):\n"
                  "• Similar to SCAN but resets to the start after reaching the end\n"
                  "• Treats the disk as a circular list (no reversal)\n"
                  "• More uniform wait times than SCAN",
                  
        "LOOK": "LOOK Algorithm:\n"
                "• Like SCAN but reverses direction after the last request\n"
                "• More efficient than SCAN by avoiding unnecessary seeks",
                
        "C-LOOK": "C-LOOK Algorithm:\n"
                  "• Like C-SCAN but only travels to the last request\n"
                  "• Combines benefits of C-SCAN and LOOK"
        }

        self.detailed_descriptions = {
            "FCFS": {
                "title": "First-Come-First-Served (FCFS)",
                "description": """FCFS (First Come First Serve) is simplest disk scheduling algorithm. Each requests are taken/executed in the sequence of their arrival in the disk queue. As a result, there is no starvation in this algorithm. However, it isn't fast compared to other algorithms.
                \nBest for: Simple systems with uniform request distribution.""",
                "Advantages": [
                    "• Easy to implement",
                    "• There is no starvation in FCFS.",
                    "• FCFS is simple and straight forward approach which means there are no indefinite delays.",
                    "• In FCFS, fair chance given to each request."
                ],
                "Disadvantages": [
                    "• FCFS isn't considered an efficient and optimized approach.",
                    "• FCFS can be time consuming."
                ],
                "time_complexity": "O(n)",

            },
            "SSTF": {
                "title": "Shortest Seek Time First (SSTF)",

                "description": """In SSTF (Shortest Seek Time First) disk scheduling algorithm we have to calculate the seek time first. 
                That is, before serving any request, seek time is calculated for each request and then the request with least seek time will be served. 
                If we define in terms of hardware then, the request which are closure to disk head position will be served first. 
                SSTF also aims to overcome some of the limitations in FCFS.
                \nBest for: Systems where average response time is critical.""",

                "Advantages": [
                    "• Better Performance compared to FCFS.",
                    "• Response time and waiting time is less.",
                    "• Increased throughput, helps in Batch Processing System.",
                    "• Low Latency: Nearby requests get serviced quickly."
                ],
                'Disadvantages': [
                    "• Starvation Risk: Distant requests may wait indefinitely if new closer requests keep arriving.",
                    "• Non-Predictable: Worst-case seek time can be high (unlike SCAN/C-SCAN).",
                    "• Requires knowing all pending requests",
                    "• Not optimal for constantly changing workloads"
                ],
                "time_complexity": "O(n log n) - due to finding closest request",
            },

            "SCAN": {
                "title": "SCAN (Elevator Algorithm)",

                "description": """Scan is often called Elevator Scheduling Algorithm, due to the way it works. 
                In SCAN, disk arm starts from one end of the disk and executes all the requests in its way till it reaches the other end. 
                As soon as it reaches the other end, it reverses its direction, 
                hence it moves back and forth continuously (like an elevator) to access the disk""",

                "Advantages": [
                    "• Predictable Performance: Services requests in a back-and-forth pattern (like an elevator), Provides consistent average wait times.",
                    "• No Starvation: All requests are serviced as the head passes them. Fairer than SSTF for distant requests.",
                    "• Good for Heavy Loads: Efficiently handles high request volumes. Throughput remains stable under load.",
                    "• Directional Efficiency: Services all requests in one direction before reversing. Minimizes unnecessary head movement."
                ],
                'Disadvantages': [
                    "• Long Wait Times for Some: Requests at opposite end wait until full scan completes. Worst-case delay = 2 x full disk traversal time.",
                    "• Over-Servicing: Always goes to disk end even if no requests exist there. Wasted seeks (fixed in LOOK variant).",
                    "• Variable Response Time: Request service time depends on head position/direction.",
                    "• Implementation Complexity: Requires tracking head direction. Needs request sorting."
                ],

                "time_complexity": "O(n log n)"
            },

            "C-SCAN": {
                "title": "C-SCAN (Circular SCAN)",

                "description": """C-SCAN is a modified version of SCAN and deals with its inefficiency in servicing the requests. 
                It moves the head from one end to other end servicing all the requests. As soon as the head reaches the other end, 
                it returns to the beginning without servicing any requests and starts servicing again from the beginning to the other end.""",

                "Advantages": [
                    "• Uniform Wait Times: Eliminates SCAN's directional bias by always returning to track 0. Provides fairer service than SCAN for edge tracks.",
                    "• Higher Throughput: More consistent performance than SCAN under heavy loads. Services ~10-15% more requests per revolution than SCAN.",
                    "• Predictable Performance: Fixed cyclical pattern (end → 0 → requests → end). Easier to calculate worst-case latency.",
                    "• Starvation-Free: All requests get serviced within 2 full disk passes maximum."
                ],
                'Disadvantages': [
                    "• Inefficient Empty Travel: Always moves to physical disk end (even with no requests). Wastes ~20-30% more seeks than LOOK variant.",
                    "• Long Latency for Certain Requests: Requests just passed may wait nearly 2 full cycles. Worst-case delay = 2 x disk size.",
                    "• Implementation Complexity: Requires tracking virtual 'wrap-around' point. Harder to debug than FCFS/SSTF.",
                    "• Poor Light-Load Performance: Overhead of full sweeps isn't justified with few requests."
                ],

                "time_complexity": "O(n log n) - due to sorting"
            },

            "LOOK": {
                "title": "LOOK",

                "description": """Look disk scheduling is another type of disk scheduling algorithm. 
                Look scheduling is an enhanced version of SCAN disk scheduling. 
                Look disk scheduling is the same as SCAN disk scheduling, but in this scheduling, instead of going till the last track, 
                we go till the last request and then change the direction.""",

                "Advantages": [
                    "• Efficient Seek Utilization: Only travels as far as the last request in each direction (unlike SCAN/C-SCAN). Eliminates empty end-to-end seeks (30-40%% less movement than SCAN)",
                    "• Improved Average Performance: 15-25%% faster average seek time than SCAN. Better throughput than C-SCAN for asymmetric workloads.",
                    "• Starvation-Free: Guarantees service within 1 full sweep. More consistent latency than SSTF",
                    "• Adaptive Direction Handling: Dynamically reverses at last request (not physical disk end). Intelligent for bursty request patterns."
                ],
                'Disadvantages': [
                    "• Variable Worst-Case Latency: New edge requests may wait nearly full sweep time. Less predictable than C-SCAN.",
                    "• Implementation Complexity: Requires tracking both direction and request boundaries. More edge cases than FCFS.",
                    "• Moderate Sorting Overhead: Still requires O(n log n) sorting like SCAN. Not as lightweight as FCFS."
                ],

                "time_complexity": "O(n log n) - due to sorting"
            },

            "C-LOOK": {
                "title": "C-LOOK (Circular LOOK) Algorithm",

                "description": """C-LOOK takes the advantages of both the disk scheduling C-SCAN, and Look disk scheduling. 
                In C-look scheduling, the disk arm moves and service each request till the head reaches its highest request, 
                and after that, the disk arm jumps to the lowest cylinder without servicing any request, 
                and the disk arm moves further and service those requests which are remaining.""",

                "Advantages": [
                    "• Optimized Seek Pattern: Only services requests in one direction (like C-SCAN). Jumps from last to first request without traveling unused areas (unlike C-SCAN). 40-50%% less head movement than SCAN.",
                    "• High Throughput: Services 15-20% more requests per revolution than LOOK. Ideal for high-density request clusters.",
                    "• Starvation-Free: All requests serviced within 1.5 disk cycles maximum.",
                    "• Predictable Performance: More consistent latency than LOOK. Clear worst-case bound = 2 x (last_request - first_request)."
                ],
                'Disadvantages': [
                    "• Directional Bias: Favors requests in the current scan direction. New opposite-direction requests wait longer.",
                    "• Implementation Complexity: Requires tracking both ends of active request zone. Edge cases when requests span disk boundaries.",
                    "• Moderate Sorting Overhead: Still requires O(n log n) sorting. Not as lightweight as FCFS."
                ],

                "time_complexity": "O(n log n) - due to sorting"
            }

        }

        self.create_widgets()

    def show_algorithm_details(self):
        """Create a detailed algorithm information window"""
        details_win = tk.Toplevel(self.root)
        details_win.title("Detailed ")
        details_win.geometry("600x500+100+100")
        
        # Main container
        container = ttk.Frame(details_win)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Algorithm selection
        ttk.Label(container, text="Select Algorithm:").pack(pady=5)
        algo_var = tk.StringVar(value="FCFS")
        ttk.OptionMenu(container, algo_var, "FCFS", *self.detailed_descriptions.keys()).pack()
        
        # Create text widget with scrollbars
        text_frame = ttk.Frame(container)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        text = tk.Text(text_frame, wrap=tk.WORD, state='disabled', 
                    font=('Arial', 11), padx=10, pady=10)
        vsb = ttk.Scrollbar(text_frame, orient="vertical", command=text.yview)
        hsb = ttk.Scrollbar(text_frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        text.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        def update_details(*args):
            """Update the displayed details when algorithm changes"""
            algo = algo_var.get()
            details = self.detailed_descriptions.get(algo, {})
            
            text.config(state='normal')
            text.delete(1.0, tk.END)
            
            # Add title
            text.insert(tk.END, f"{details.get('title', '')}\n\n", "title")
            text.tag_configure("title", font=('Arial', 14, 'bold'))
            
            # Add description
            text.insert(tk.END, f"{details.get('description', '')}\n\n", "desc")
            text.tag_configure("desc", font=('Arial', 11, 'italic'))
            
            # Add Advantages
            text.insert(tk.END, "Advantages:\n", "subtitle")
            text.tag_configure("subtitle", font=('Arial', 12, 'underline'))

            for char in details.get('Advantages', []):
                text.insert(tk.END, f"{char}\n")

            # Add Disadvantages
            text.insert(tk.END, "\nDisadvantages:\n", "subtitle")
            text.tag_configure("subtitle", font=('Arial', 12, 'underline'))
            
            for char in details.get('Disadvantages', []):
                text.insert(tk.END, f"{char}\n")
            
            # Add technical details
            text.insert(tk.END, "\nTechnical Details:\n", "subtitle")
            text.insert(tk.END, f"Time Complexity: {details.get('time_complexity', '')}\n")
            
            text.config(state='disabled')
        
        # Initial update and trace
        algo_var.trace_add('write', update_details)
        update_details()
        
        # Close button
        ttk.Button(container, text="Close", command=details_win.destroy).pack(pady=10)


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


    def update_description(self, *args):
        """Update the description text when algorithm changes"""
        algo = self.algorithm_var.get()
        description = self.algorithm_descriptions.get(algo, "No description available")
        
        self.desc_text.config(state='normal')
        self.desc_text.delete('1.0', tk.END)
        self.desc_text.insert(tk.END, description)
        self.desc_text.config(state='disabled')

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
        
        ttk.Label(input_frame, text="Algorithm Description:").grid(row=5, column=0, sticky=tk.W, pady=5)
    
        ### Create a text widget for the description
        self.desc_text = tk.Text(input_frame, height=6, width=50, wrap=tk.WORD, 
                                state='disabled', bg='#f5f5f5', relief='solid')
        self.desc_text.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # With this:
        # Create a frame to hold both text widget and scrollbar
        desc_frame = ttk.Frame(input_frame)
        input_frame.grid_columnconfigure(1, weight=1)  # Makes column 1 expandable
        desc_frame.grid(row=5, column=1, padx=5, pady=5, sticky='nsew')

        # Text widget
        self.desc_text = tk.Text(desc_frame, height=6, width=50, wrap=tk.WORD,
                                state='disabled', bg='#f5f5f5', relief='solid')
        self.desc_text.pack(side='left', fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(desc_frame, orient='vertical', command=self.desc_text.yview)
        scrollbar.pack(side='right', fill='y')

        # Link text widget to scrollbar
        self.desc_text.config(yscrollcommand=scrollbar.set)
        
        # Add trace to update description when algorithm changes
        self.algorithm_var.trace_add('write', self.update_description)
        
        # Initial description update
        self.update_description()

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

        self.details_button = ttk.Button(button_frame, 
                                text="Detailed Description",
                                command=self.show_algorithm_details)
        self.details_button.pack(side=tk.LEFT, padx=10)


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

#v4