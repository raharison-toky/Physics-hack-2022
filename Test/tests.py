import pyglet
from pyglet import shapes

window = pyglet.window.Window(720,720)
# label = pyglet.text.Label("Big Brain",
#     font_name="Times New Roman",
#     font_size=25,
#     x=window.width//2, y = window.height//2,
#     anchor_x="center", anchor_y="center")

batch = pyglet.graphics.Batch()

class Neuron:
    neurons = []
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.radius = 10
        self.height = 100
        self.charge = shapes.Circle(x,y,self.radius,color=(50,255,30),batch=batch)
        self.body = shapes.Rectangle(self.x - self.radius//4,self.y,3,self.height,color=(50,255,30),batch=batch)
        self.shapes = [self.charge,self.body]
        self.neurons.append(self)
        self.transmitting = False

    def activate(self):
        self.transmitting = True

    def draw(self):
        for i in self.shapes:
            i.draw()
        self.move()

    def move(self):
        # self.x += 5
        # self.y += 5
        if self.transmitting:
            self.charge.x +=0
            self.charge.y +=5
            if self.charge.y == self.body.y + self.height:
                self.charge.x = self.x
                self.charge.y = self.y
                self.transmitting = False

neuron1 = Neuron(200,50)
for i in Neuron.neurons:
    i.activate()

@window.event 
def on_draw():
    window.clear()
    for i in Neuron.neurons:
        #i.activate()
        i.draw()
        # i.draw()
        # i.move()
    # label.draw()

pyglet.app.run()
