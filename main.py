from gui.main_window import DiskSchedulingSimulator
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingSimulator(root)
    root.mainloop()