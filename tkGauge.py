import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from scipy.interpolate import interp1d


class TkGauge:
	"""
	A gauge chart widget for tkinter projects. Gauge charts represent data visually by utilizing a dial or indicator gauge.

	Args:
		master (tk.Frame): The parent tkinter widget where the gauge will be placed.
		min_val (float, optional): The minimum value displayed on the gauge chart. Defaults to 0.
		max_val (float, optional): The maximum value displayed on the gauge chart. Defaults to 10.
		title (str, optional): The title or label for the gauge chart. Defaults to an empty string.
		size (int, optional): The size (width and height) of the gauge widget in pixels. Defaults to 100.
		value (float, optional): The initial value of the gauge dial. Defaults to 5.7.

	Attributes:
		canvas (tk.Canvas): The canvas where the gauge components are drawn.
		line (int): The identifier of the line representing the dial on the canvas.
		value_lbl (int): The identifier of the text label displaying the current value on the canvas.
		x1 (float): The x-coordinate of the center of the gauge.
		y1 (float): The y-coordinate of the center of the gauge.
		img (ImageTk.PhotoImage): The image object representing the background of the gauge.
		dial_length (int): The length of the dial indicator on the gauge.

	Methods:
		get_coords(theta): Convert an angle to x-y coordinates on the gauge dial.
		set_dial(value): Set the value of the gauge dial and update its position on the canvas.
	"""

	def __init__(self, master: tk.Frame, min_val: float = 0, max_val: float = 10, title: str = '', size: int = 300, value: float = 5.7):
		"""
		Initialize the GaugeWidget.

		Parameters:
			master (tk.Frame): The parent tkinter widget where the gauge will be placed.
			min_val (float, optional): The minimum value displayed on the gauge chart. Defaults to 0.
			max_val (float, optional): The maximum value displayed on the gauge chart. Defaults to 10.
			title (str, optional): The title or label for the gauge chart. Defaults to an empty string.
			size (int, optional): The size (width and height) of the gauge widget in pixels. Defaults to 300.
			value (float, optional): The initial value of the gauge dial. Defaults to 5.7.
		"""

		# Load the image for the background
		image = Image.open('Images/template.png').resize((size, size), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(image)

		# Get the centre position of the background image
		self.x1, self.y1 = x1, y1 = size/2, size/2

		# Define the dial length
		self.dial_length = int(0.3*size)

		# Create an interpolation object. Could also use numpy.interp(x, [x1,y1], [x2,y2])
		self.map = interp1d([min_val, max_val], [0.75*np.pi, 2.25*np.pi])

		# Create the canvas, for the gauge and pack it
		self.canvas = tk.Canvas(master, width=size, height=size)
		self.canvas.pack()

		# Make up the gauge components
		self.canvas.create_image(x1, y1, image=self.img) # Load the image on the canvas
		self.canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill='red', width=3) # Circle at the centre of the gauge
		self.canvas.create_text(x1, y1+30, fill="white", font=("Purisa", 12), text=title) # Title for the gauge
		self.canvas.create_rectangle(x1-20, y1+40, x1+20, y1+60, fill='black') # Background for the value text box
		self.value_lbl = self.canvas.create_text(x1, y1+50, fill="white", font=("Purisa", 12), text=value) # Value of the dial

		# Numbers circling the chart
		for i in np.linspace(min_val, max_val, num=10): 	
			x2, y2 = self.get_coords(self.map(i))
			self.canvas.create_text(x2, y2, fill="white", font=("Purisa", 12), text=int(i))

		# Make the line for the dial
		x2, y2 = self.get_coords(self.map( value ))
		self.line = self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

		return None

	def get_coords(self, theta) -> tuple:
		"""
		Convert a given angle to x-y coordinates of the tip of the dial.

		Parameters:
			theta (float): The angle in radians.

		Returns:
			tuple: A tuple containing the x-y coordinates of the tip of the dial.
		"""
		x2 = self.x1 + self.dial_length*np.cos(theta)
		y2 = self.y1 + self.dial_length*np.sin(theta)
		return x2, y2

	def set_dial(self, value) -> None:
		"""
		Set the value of the gauge dial and update its position on the canvas.

		Parameters:
			value (float): The value to set on the gauge dial.
		"""
		x2,y2 = self.get_coords( self.map(value) )
		self.canvas.coords(self.line, self.x1, self.y1, x2,y2)
		self.canvas.itemconfigure(self.value_lbl, text=value)

		return None


if __name__ == '__main__':
	root = tk.Tk()
	mygauge1 = TkGauge(root, title="Speed", min_val=20, max_val=200, value=50, size=300)
	root.mainloop()
