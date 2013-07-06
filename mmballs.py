import xml.etree.ElementTree as etree
import Tkinter as tk
from random import randrange

WIDTH = 500
HEIGHT = 500

#setup GUI
root = tk.Tk()

canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT)  
canvas.pack() 

nodeIds = []
for i in range(0, 1000, 10):
	nodeIds.append(canvas.create_oval(i + 20, i + 20, i + 40, i + 40, tags = 'node'))

#collision check - added to mindmapper
while 1:
	overlap_count = 0
	for node in nodeIds:
		x1, y1, x2, y2 = canvas.bbox(node)
		overlaps = canvas.find_overlapping(x1, y1, x2, y2)
		for overlap in overlaps:
			print overlaps
			if overlap != node:
				overlap_count += 1	
				canvas.move(overlap, randrange(-10,10), randrange(-10,10))
	if overlap_count == 0:
		break

#	 
		
 
#run GUI          
root.mainloop()