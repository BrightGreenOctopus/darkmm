import pygame
import random, math
import form
import xml.etree.ElementTree as etree
from math import cos, sin, pi, log



background_colour = (0, 0, 0)
(WIDTH, HEIGHT) = (1000, 800)
drag = 0.7
elasticity = 0.75
gravity = (0.5*math.pi, 0.00)
DEPTH = 10 #display depth for nodes
FULL_HEIGHT = 900

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)

class Particle():
    def __init__(self, (x, y), xml, children, parent):
        self.x = x
        self.y = y
        self.size = 100 #Radius WARN: hardcoded
        self.colour = (220, 220, 220)
        self.thickness = 3
        self.speed = 0
        self.angle = 0
        #
        self.children = children
        self.parent = parent
        self.text = xml.attrib['TEXT']
        self.is_distant = False

    def display(self):
        if self.is_distant:
            #pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
            #
            self.font = pygame.font.Font(None, self.size / 2)
            label = self.font.render(self.text, 1, (0,255,0))
            screen.blit(label, (self.x - self.size, self.y))

        else:
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)
            #
            self.font = pygame.font.Font(None, self.size / 2)
            label = self.font.render(self.text[:10], 1, (0,255,0))
            screen.blit(label, (self.x - self.size, self.y))

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag


    def bounce(self):
        if self.x > WIDTH - self.size:
            self.x = 2*(WIDTH - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > HEIGHT - self.size:
            self.y = 2*(HEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

screen = pygame.display.set_mode((WIDTH, FULL_HEIGHT))
pygame.display.set_caption('FreeMM')
pygame.font.init()



number_of_particles = 5
my_particles = []

def import_mm_file(filename):
    """
    parses freemind xml from file and creates Particle objects
    returns root node
    """

    #parse xml
    tree = etree.parse(filename)
    map = tree.getroot()

    #recursively build tree
    def parse_tree(node, parent):
        """takes xml node and returns children as particles"""
        children = []
        for xml in node:
            if xml.tag == 'node':
                #add children
                new_particle = Particle((10,10), xml, [], parent)
                new_particle.children = parse_tree(xml, new_particle)
                children.append(new_particle)
        return children

    return parse_tree(map, None)[0]

root_node = import_mm_file('test.mm')

def draw_map():
    """draws Nodes from root_node"""

    root_node.x, root_node.y = WIDTH/2, HEIGHT/2
    root_node.size = 100
    my_particles.append(root_node)

    #recurse
    def draw_children(parent, depth):
        if depth != 0:
            bredth = 0
            for child in parent.children:
                child.size = int((1 / float(2 ** (DEPTH - depth))) * 50)
                cv = int((1 / float(2 ** (DEPTH - depth))) *200)
                child.colour = (cv,cv,cv)
                #calculate coords
                #r = (1 / float(4 ** (DEPTH - depth))) * 300
                r = parent.size + child.size + (parent.size/(2 ** (DEPTH - depth)))
                w = bredth * (2*pi / len(parent.children))
                x, y = (r * cos(w)) + parent.x, (r * sin(w)) + parent.y
                bredth += 1
#                   font_size = abs(int(20 - (depth*3)))
                print depth, bredth, r, w, x, y
                child.x, child.y = x, y

                if (DEPTH - depth) > 0:
                    child.is_distant = True
                else:
                    child.is_distant = False

                my_particles.append(child)
                draw_children(child, depth - 1)

    draw_children(root_node, DEPTH)

draw_map()

txt = form.Form((0, 800), 1000, fontsize=15, height=100)
txt.OUTPUT = unicode("""This new version is simpler to use and faster with the great texts,
the constraint being that it only supports monospaced fonts.

There is still plenty of improvement to do.
You can modify this text ...""","utf8")
txt.show()

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
            last_selected = selected_particle
            if event.button == 4:
                if last_selected:
                    root_node = last_selected
                    my_particles = []
                    draw_map()
            if event.button == 5:
                if last_selected and last_selected.parent:
                    root_node = last_selected.parent
                    my_particles = []
                    draw_map()

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        txt.update(event)

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1
        txt.OUTPUT = selected_particle.text

    screen.fill(background_colour)
    txt.show()

    for i, particle in enumerate(my_particles):
        particle.move()
        #particle.bounce()
        #for particle2 in my_particles[i+1:]:
        #    collide(particle, particle2)
        particle.display()

    pygame.display.flip()
