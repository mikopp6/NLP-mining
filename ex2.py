import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Create a function to generate and display plots
def create_plots(frame, num_plots, title_prefix):
    for i in range(num_plots):
        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(f"{title_prefix} {i+1}")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 1, 6, 3]
        ax.plot(x, y, label="Data")
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

# Create a tkinter window
root = tk.Tk()
root.title("Tkinter Application with Tabs")
root.geometry("1000x600")

# Create a notebook widget to hold the tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create the first tab with 6 plots
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
create_plots(tab1, num_plots=6, title_prefix="Plot in Tab 1")

# Create the second tab with 4 plots
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")
create_plots(tab2, num_plots=4, title_prefix="Plot in Tab 2")

# Start the tkinter main loop
root.mainloop()