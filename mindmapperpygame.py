import xml.etree.ElementTree as etree
import sys, pygame
import Tkinter as tk

size = WIDTH, HEIGHT = 1000, 1000

#setup GUI
pygame.init()
screen = pygame.display.set_mode(size)

#setup tk
root = tk.Tk()
frame = tk.Frame(root, height=300, width=WIDTH)
frame.pack()

class Node:
	"""Mindmap node"""
	
	def __init__(self, coords, text):
		
		self.x = coords[0]
		self.y = coords[1]
		self.text = text
		
		text = canvas.create_text(self.x, self.y, text = self.text)
#testnode = Node((50,50), "testnode")

tree = etree.parse('test.mm')
map = tree.getroot()

nodelist = []

def parse_tree(node, depth = 1, coords = (WIDTH/2, HEIGHT/2)):
	bredth = 0
	for child in node:
		if child.tag == 'node':
			
			#calculate coords
			from math import cos, sin, pi, log
			r = depth * (HEIGHT/6.0)
			w = bredth * pi/4
#			w = pi * w / 180.0 #dont like thinking in radians
			x, y = r * cos(w) + coords[0], r * sin(w) + coords[1]
			
#			nodelist.append(Node((x, y), child.attrib['TEXT'])) 
			nodelist.append(Node((x, y), '.')) 

			#add children
			bredth += 1
			parse_tree(child, depth + log(depth, 2), (x,y))
		
parse_tree(map)
	
#attribs are in dict
#rootnode.attrib['TEXT']

#run eventloop          
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
