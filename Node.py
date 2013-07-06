import Tkinter as tk

class TkNode:
    """Mindmap Node, contains xml and child Nodes"""
    
    def __init__(self, tkmaster, xml, children):
        
        self.children = children
        self.x = 50 
        self.y = 50

        self.text = tk.Text(tkmaster, width= 1, height= 1)
        self.text.insert(tk.END, xml.attrib['TEXT'][:30])
        

        self.text.place(x= self.x, y= self.y)
    

    def move(self, pos):
        """moves center of node to pos"""
        #TODO: ajust for node height
        self.x = pos[0]
        self.y = pos[1]

        self.text.place(x= self.x, y= self.y, anchor= tk.N)




    



