import tkinter as tk
from tkGauge import TkGauge

# Create a tkinter root
root = tk.Tk()
root.title('My Car Dashboard')

# Create 2 frames and pack them
f1, f2 = tk.Frame(root), tk.Frame(root)

# And now create 2 gauges
g1 = TkGauge(f1, min_val=0, max_val=450, title="MPH", size=300, value=110)
g2 = TkGauge(f2, min_val=0, max_val=4500, title="RPM", size=300, value=2780)

def update_g1(val):
    g1.set_dial(float(val))

def update_g2(val):
    g2.set_dial(float(val))

# Add two scales
s1 = tk.Scale(root, from_ = 0, to = 450, orient = tk.HORIZONTAL, command=update_g1) 
s2 = tk.Scale(root, from_ = 0, to = 4500, orient = tk.HORIZONTAL, command=update_g2)
s1.set(110)
s2.set(2780)

f1.grid(row = 0, column = 0)
f2.grid(row = 0, column = 1)
s1.grid(row=1, column=0, sticky="news")
s2.grid(row=1, column=1, sticky="news")

root.mainloop()
