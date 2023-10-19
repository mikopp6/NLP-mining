import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Create a Tkinter window
root = tk.Tk()
root.title("Tkinter Plot Example")
root.geometry("1000x600")

# Create a Frame for the first column of plots
frame1 = ttk.Frame(root)
frame1.grid(row=0, column=0)

# Create a Frame for the second column of plots
frame2 = ttk.Frame(root)
frame2.grid(row=0, column=1)

# Create Matplotlib Figures and Axes for the first column
fig1 = Figure(figsize=(2,2), dpi=100)
ax1 = fig1.add_subplot(111)
ax1.set_title("Plot 1")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")
x = [1, 2, 3, 4, 5]
y1 = [2, 4, 1, 6, 3]
ax1.plot(x, y1, label="Data 1")
ax1.legend()

fig2 = Figure(figsize=(2,2), dpi=100)
ax2 = fig2.add_subplot(111)
ax2.set_title("Plot 2")
ax2.set_xlabel("X-axis")
ax2.set_ylabel("Y-axis")
y2 = [1, 3, 5, 2, 4]
ax2.plot(x, y2, label="Data 2")
ax2.legend()

fig3 = Figure(figsize=(2,2), dpi=100)
ax3 = fig3.add_subplot(111)
ax3.set_title("Plot 3")
ax3.set_xlabel("X-axis")
ax3.set_ylabel("Y-axis")
y3 = [4, 2, 3, 1, 5]
ax3.plot(x, y3, label="Data 3")
ax3.legend()

# Create Matplotlib Figures and Axes for the second column
fig4 = Figure(figsize=(2,2), dpi=100)
ax4 = fig4.add_subplot(111)
ax4.set_title("Plot 4")
ax4.set_xlabel("X-axis")
ax4.set_ylabel("Y-axis")
y4 = [5, 3, 2, 4, 1]
ax4.plot(x, y4, label="Data 4")
ax4.legend()

fig5 = Figure(figsize=(2,2), dpi=100)
ax5 = fig5.add_subplot(111)
ax5.set_title("Plot 5")
ax5.set_xlabel("X-axis")
ax5.set_ylabel("Y-axis")
y5 = [3, 2, 4, 1, 5]
ax5.plot(x, y5, label="Data 5")
ax5.legend()

fig6 = Figure(figsize=(2,2), dpi=100)
ax6 = fig6.add_subplot(111)
ax6.set_title("Plot 6")
ax6.set_xlabel("X-axis")
ax6.set_ylabel("Y-axis")
y6 = [2, 5, 4, 1, 3]
ax6.plot(x, y6, label="Data 6")
ax6.legend()

# Embed the Matplotlib Figures in the Tkinter window
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.pack(fill=tk.BOTH, expand=True)

canvas2 = FigureCanvasTkAgg(fig2, master=frame1)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.pack(fill=tk.BOTH, expand=True)

canvas3 = FigureCanvasTkAgg(fig3, master=frame1)
canvas_widget3 = canvas3.get_tk_widget()
canvas_widget3.pack(fill=tk.BOTH, expand=True)

canvas4 = FigureCanvasTkAgg(fig4, master=frame2)
canvas_widget4 = canvas4.get_tk_widget()
canvas_widget4.pack(fill=tk.BOTH, expand=True)

canvas5 = FigureCanvasTkAgg(fig5, master=frame2)
canvas_widget5 = canvas5.get_tk_widget()
canvas_widget5.pack(fill=tk.BOTH, expand=True)

canvas6 = FigureCanvasTkAgg(fig6, master=frame2)
canvas_widget6 = canvas6.get_tk_widget()
canvas_widget6.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter main loop
root.mainloop()
