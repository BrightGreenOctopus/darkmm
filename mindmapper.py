import xml.etree.ElementTree as etree
import Tkinter as tk
from random import randrange
from math import cos, sin, pi, log

from Node import TkNode

WIDTH = 1000
HEIGHT = 1000
DEPTH = 3 #display depth for nodes
RADIUS = 100

class Display:
    """Container for Nodes, handles placement"""
    
    def __init__(self):
        """setup GUI etc"""

##        self.nodes = []
        
        #setup GUI
        self.root = tk.Tk()

        self.frame = tk.Frame(self.root, height=HEIGHT, width=WIDTH)
        self.frame.pack()
        
        self.import_mm_file('test.mm')
        self.draw_map()

        #run GUI          
        self.root.mainloop()

##        button = tk.Button(self.root, text = "Clear Overlaps", command = self.clear_overlaps)
##        button.pack()
#   
#   button2 = tk.Button(root, text = "Zoom in", command = zoom_in)
#   button.pack()


    def import_mm_file(self, filename):
        """parses freemind xml from file and creates Node objects"""

        #parse xml
        tree = etree.parse(filename)
        map = tree.getroot()
        
        #recursively build tree
        def parse_tree(node):
            children = []
            for child in node:
                if child.tag == 'node':
                    #add children
                    grandchildren = parse_tree(child)
                    new_node = TkNode(self.frame, child, grandchildren)
                    children.append(new_node)
            return children
        
        self.root_node = parse_tree(map)[0]


    def draw_map(self):
        """draws Nodes from root_node"""

        self.root_node.move([WIDTH/2, HEIGHT/2])
        #recurse
        def draw_children(parent, depth):
            if depth != 0:
                bredth = 0
                for child in parent.children:
                    
                    #calculate coords
                    r = (1 / float(4 ** (DEPTH - depth))) * 500
                    w = bredth * (2*pi / len(parent.children))
                    x, y = (r * cos(w)) + parent.x, (r * sin(w)) + parent.y
                    bredth += 1
#                   font_size = abs(int(20 - (depth*3)))
                    print depth, bredth, r, w, x, y
                    
                    child.move([x, y])
                    draw_children(child, depth - 1)
        
        draw_children(self.root_node, DEPTH)
        
        
        





    #event handlers
    def clear_overlaps(self):
        """moves overlapping nodes randomly away from each other"""
        while 1:
            overlap_count = 0
            for node in nodelist:
                x1, y1, x2, y2 = canvas.bbox(node.id)
                overlaps = canvas.find_overlapping(x1, y1, x2, y2)
                print overlaps
                for overlap in overlaps:
                    if overlap != node.id:
                        overlap_count += 1  
                        canvas.move(overlap, randrange(-30,40,5), randrange(-20,20,5))
            if overlap_count == 0:
                break
            canvas.update()
    
    
    def zoom_in(self):
        """TODO: makes selected node centre and moves rest up one level"""
        pass
    
        
        


Display()






        




