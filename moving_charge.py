import pyglet
from pyglet import shapes
import math

window = pyglet.window.Window(750, 750)
batch = pyglet.graphics.Batch()

# def GUIreceptor():

class Point:
    def __init__(self,x,y) -> None:
          self.x = x
          self.y = y

class Neuron:
    neurons = []

    def __init__(self,start,end) -> None:
          width = 16
          self.start = start
          self.end = end
          self.synapse = shapes.Rectangle(self.start.x, self.start.y, width, width, color=(55, 55, 255), batch=batch)
          self.synapse.anchor_x = width/2
          self.synapse.anchor_y = width/2
          dx = self.end.x - self.end.y
          dy = self.end.y - self.end.x

          self.rotation = math.acos(dy/math.sqrt(dx**2+dy**2))
          self.synapse.rotation = 45

          self.radius = 10
          self.head = shapes.Circle(self.end.x, self.end.y, self.radius, color=(50, 225, 30), batch=batch)
        #   self.head.anchor_x = width/2
        #   self.head.anchor_y = width/2

          self.line = shapes.Line(self.start.x, self.start.y, self.end.x, self.end.y, width=5, color=(200, 20, 20), batch=batch)

          self.shapes = [self.line,self.synapse,self.head,]

          self.neurons.append(self)

    def draw(self):

        for i in self.shapes:
            i.draw()



# def GUI_create_receptor(x, y):
# 	width = 16
# 	shape = shapes.Rectangle(x, y, width, width, color=(55, 55, 255), batch=batch)
# 	shape.anchor_x = width/2
# 	shape.anchor_y = width/2
# 	shape.rotation = 45
# 	return shape

# def GUI_create_neuron(x, y):
# 	radius = 10
# 	shape = shapes.Circle(x, y, radius, color=(50, 225, 30), batch=batch)
# 	return shape




# # line = shapes.Line(150, 0, 150, 200, width=4, color=(200, 20, 20), batch=batch)

# line2 = shapes.Line(20, 20, 161, 136, width=3, color=(200, 20, 20), batch=batch)

# receptor = GUI_create_receptor(20,20)
# neuron = GUI_create_neuron(161,136)

start = Point(20,20)
end = Point(161,136)

start1 = Point(70,40)
end1 = Point(261,136)

neuron1 = Neuron(start,end)


neuron1 = Neuron(start1,end1)
@window.event
def on_draw():
    window.clear()
    for i in Neuron.neurons:
        i.draw()

pyglet.app.run()