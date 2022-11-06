import math
from typing import Type, Union, Optional
import pyglet
from pyglet import shapes
from pyglet.window import key
import numpy as np
import random
# Main File
# K_e * q / r
# Constants
K_e = 8.9875517923E9  # Coulomb's constant

triangular_tail = pyglet.image.load("triangular_tail.png")
triangular_tail.anchor_x = triangular_tail.width//2
triangular_tail.anchor_y = triangular_tail.height//2
axon = pyglet.image.load("axon.png")
axon.anchor_x = axon.width // 2
axon.anchor_y = axon.height // 2
print(axon.width, axon.height)
head = pyglet.image.load("head_circleless.png")
head.anchor_x = 126
head.anchor_y = 140
print(head.width, head.height)

triangular_neurons = pyglet.image.load("triangular_circleless.png")
triangular_neurons.anchor_x = 80
triangular_neurons.anchor_y = 159


charge = pyglet.image.load("charge.png")
####################################
charge.anchor_x = charge.width // 2
charge.anchor_y = charge.height // 2
##################################


# Objects and Classes

window = pyglet.window.Window(1920, 1080)
pyglet.gl.glClearColor(159/255,197/255,232/255,1.000)
batch = pyglet.graphics.Batch()


class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def dist_from_point(self, point2: Type["Point"]):
    return math.sqrt(((self.x - point2.x)**2 + (self.y - point2.y)**2))


class CompleteDiagram():

  def __init__(self):
    self.receptors = []
    self.electrodes = []
    self.neurons = []

  def check_grid(self):
    for neuron in self.neurons:
      if neuron.transmitted:
        for child in neuron.children:
          child.activate()

  def get_shapes(self):
    pass

  def draw(self):
    # create batch
    #batch = pyglet.graphics.Batch()
    # add all lines to batch
    # for root_node in receptors:
    #   pass
    for electrode in self.electrodes:
      electrode.potential = 0.0

    for neuron in self.neurons:
      neuron.draw()

    for electrode in self.electrodes:
      electrode.draw()
    # add points


class Electrode:

    """
    class for checking the electric potential as it would be measured at the position on the screen and plotting it.
    It plots the time domain for the previous 50 values and computes the FFT with the previous 200 values.
    """

    def __init__(self, point: Point, diagram: CompleteDiagram):
        self.point = point
        self.diagram = diagram
        self.diagram.electrodes.append(self)
        self.potential = 0
        self.graph_x = 150
        self.graph_y = 1080//2
        self.graph_width = 750
        self.graph_height = 200
        self.radius = 7
        self.values = [pyglet.shapes.Circle(self.graph_x+i,self.graph_y+self.graph_height//2,self.radius,color=(255, 255, 255),batch=batch) for i in range(0,self.graph_width,self.graph_width//50)]
        self.previous_vals = np.zeros(len(self.values))
        self.previous_200 = np.zeros(200)

        self.fft_graph_x = self.graph_x + self.graph_width + 100
        self.fft_graph_y = self.graph_y
        fourier_domain= np.fft.fft(self.previous_200)
        self.fft_values = [pyglet.shapes.Circle(self.fft_graph_x+i,self.graph_y+self.graph_height//2,self.radius,color=(255, 255, 255),batch=batch) for i in range(0,self.graph_width,self.graph_width//25)]
        self.lines = [shapes.Line(self.fft_values[i].x, self.fft_values[i].y, self.fft_values[i+1].x, self.fft_values[i+1].y, width=5, color=(255, 255, 255), batch=batch) for i in range(len(self.fft_values)-1)]

        self.time_text = pyglet.text.Label("Time domain",
	                       color=(255, 255, 255, 255),
	                       font_name='Arial',
	                       font_size=30,
	                       x=self.graph_x,
	                       y=self.graph_y - 60)

        self.freq_text = pyglet.text.Label("Frequency domain",
	                       color=(255, 255, 255, 255),
	                       font_name='Arial',
	                       font_size=30,
	                       x=self.fft_graph_x,
	                       y=self.graph_y - 60)


    def draw(self):
        # square = pyglet.shapes.Rectangle(500,350,400,200,color=(255, 255, 255),batch=batch)
        # fl = pyglet.text.Label(f'{np.average(self.previous_200):.0f} V',
	    #                    color=(255, 255, 255, 255),
	    #                    font_name='Arial',
	    #                    font_size=20,
	    #                    x=500,
	    #                    y=300)
        self.previous_vals[:-1] = self.previous_vals[1:]
        self.previous_vals[-1] = self.potential
        self.previous_200[:-1] = self.previous_200[1:]
        self.previous_200[-1] = self.potential
        fourier_domain = np.fft.fft(self.previous_200)
        # w = np.fft.fftfreq(50)*256
        # print(w)
        # fl.draw()
        for i in range(len(self.previous_vals)):
            self.values[i].y = self.previous_vals[i]/40 + self.graph_y
            self.values[i].draw()

        for i in range(len(self.fft_values)):
            self.fft_values[i].y = self.graph_y + abs(fourier_domain[i+1]/300)
            self.fft_values[i].draw()

        # Drawing full lines instead of dots
        # self.lines = [shapes.Line(self.fft_values[i].x, self.fft_values[i].y, self.fft_values[i+1].x, self.fft_values[i+1].y, width=5, color=(255, 255, 255), batch=batch) for i in range(len(self.fft_values)-1)]

        # for i in self.lines:
        #     i.draw()

        #print(len(self.fft_values))

        self.time_text.draw()
        self.freq_text.draw()

        # square.draw()


class Receptor:

  def __init__(self, point: Point, diagram: CompleteDiagram):
    self.point = point
    self.children = []
    self.diagram = diagram
    self.diagram.receptors.append(self)

  def activation(self):
    for i in self.children:
      i.transmitting = True


class Charge:

    def __init__(self, neuron):
        self.neuron = neuron
        self.start = neuron.start
        self.end = neuron.end
        self.offset = random.random()
        radius = 5
        self.vector_length = 12
        self.shape = shapes.Circle(x=self.start.x, y=self.start.y, radius=radius, color=(255, 0, 0), batch=batch)
        self.vector = np.array([self.end.x - self.start.x, self.end.y - self.start.y])
        self.vector = self.vector /np.linalg.norm(self.vector)
        self.remaining_d = math.sqrt((self.start.x - self.end.x)**2 + (self.start.y - self.end.y)**2)


    def move_charge(self):
        if self.remaining_d > self.vector_length:
            self.shape.opacity = 255
            self.shape.x += self.vector[0]*(self.vector_length - self.offset)
            self.shape.y += self.vector[1]*(self.vector_length - self.offset)
            self.remaining_d = math.sqrt((self.shape.x - self.end.x)**2 + (self.shape.y - self.end.y)**2)
        
        else:
            self.shape.opacity = 0
            # if self.shape.opacity != 0:
            #     self.shape.opacity -= 3
            #     self.neuron.transmitting = False
            self.neuron.transmitting = False
            self.neuron.done_transmitting = True
            self.shape.x = self.neuron.start.x
            self.shape.y = self.neuron.start.y
            self.offset = random.random()
            self.remaining_d = math.sqrt((self.shape.x - self.end.x)**2 + (self.shape.y - self.end.y)**2)
            self.neuron.done_transmition()

    def draw(self):
        if self.neuron.transmitting:
            self.move_charge()
            self.shape.draw()


class Neuron:
  """
    Important note: point is the TAIL of the neuron
    """

  def __init__(self, point: Point, parent: Union[Receptor, Type["Neuron"]]):
    self.point = point
    self.parent = parent
    self.diagram = parent.diagram
    self.children = []
    self.transmitting = False
    self.done_transmitting = False

    width = 16

    self.start = self.parent.point
    self.end = self.point

    self.synapse = pyglet.sprite.Sprite(head, x=self.start.x, y=self.start.y, batch=batch)
    self.synapse.scale = 0.25

    ratio = (self.end.y - self.start.y) / (self.end.x - self.start.x)
    degrees = math.atan(ratio) * 180 / math.pi

    dx = self.end.x - self.end.y
    dy = self.end.y - self.end.x

    self.rotation = math.acos(dy / math.sqrt(dx**2 + dy**2))
    self.synapse.rotation = -degrees - 5

    self.radius = 11

    # self.head = pyglet.sprite.Sprite(triangular, x=self.end.x-10, y=self.end.y-10, batch=batch)
    # self.head.anchor_x = self.head.width / 2
    # self.head.anchor_y = self.head.height / 2
    # self.head.scale = 0.05

    self.line = pyglet.sprite.Sprite(axon, x=(self.end.x + self.start.x)//2, y=(self.end.y + self.start.y)//2,
                                     batch=batch)

    lenght = math.sqrt((self.end.x - self.start.x) ** 2 + (self.start.y - self.end.y) ** 2)
    self.line.scale_y = 0.4
    self.line.rotation = -degrees
    self.line.scale_x = lenght / 386

    self.shapes = [
      self.line,
      self.synapse,
    ]

    # append itself as a child to the parent
    self.parent.children.append(self)
    self.diagram.neurons.append(self)

  def activate(self):
    self.transmitting = True

  def done_transmition(self):
    for i in self.children:
      i.transmitting = True
      i.activate()
    self.transmitting = False
    self.transmitting = False

  def draw(self):
    for i in self.shapes:
      i.draw()


class TriangularNeuron(Neuron):

  DIPOLE_DIST = 5

  def __init__(self, point: Point, parent: Union[Receptor, Type["Neuron"]]):
    super().__init__(point, parent)

    self.head = pyglet.sprite.Sprite(triangular_neurons, x=self.end.x + 5, y=self.end.y, batch=batch)

    self.head.scale = 0.25
    self.head.rotation = self.line.rotation

    self.line = pyglet.sprite.Sprite(triangular_tail, x=(self.end.x + self.start.x)/2 + 5, y=(self.end.y + self.start.y)/2 - 5, batch=batch)
    self.line.rotation = self.head.rotation
    lenght = math.sqrt((self.start.x - self.end.x)**2 + (self.start.y - self.end.y)**2)
    self.line.scale_y = 0.35
    self.line.scale_x = lenght / 230

    self.charge = Charge(self)
    # self.shapes.append(self.charge)

    self.synapse = pyglet.sprite.Sprite(head, x=self.start.x, y=self.start.y, batch=batch)
    self.synapse.scale = 0.25

    
  # def activation(self):
  #     self.activate()

  # def activate(self):
  #     self.charge = 1
  #     self.activated = True
  #     print(self.charge)
  #     print("activated")

    self.shapes = [
      self.head,
      self.line,
      self.synapse,
      self.charge
    ]

    self.activated = False
    self.charge = 0.005
    self.max_charge = 0.005

    self.charging = False


  def activate(self):
    self.activated = True

  def done_transmition(self):
        #self.charge = 0.005
        # print(self.charge)
        # print("activated")
        self.charging = True


  def get_potential(self):
        # if (self.activated) and (self.charge <= 0.5):
        #     self.charge += 0.1
        #     print("It ran")
        #     return self.charge 

        electrode = self.diagram.electrodes[0]
        positive_pole_point = self.point
        length_neuron = math.sqrt((self.parent.point.x - self.point.x)**2 + (self.parent.point.y - self.point.y)**2)
        negative_x = self.point.x + (self.point.x - self.parent.point.x) * self.DIPOLE_DIST / length_neuron
        negative_y = self.point.y + (self.point.y - self.parent.point.y) * self.DIPOLE_DIST / length_neuron
        positive_pole_distance = self.point.dist_from_point(electrode.point)
        negative_pole_distance = Point(negative_x, negative_y).dist_from_point(electrode.point)
        electrode.potential += K_e * self.charge * (1 / positive_pole_distance - 1 / negative_pole_distance)
        #print(K_e * self.charge * (1 / positive_pole_distance - 1 / negative_pole_distance))

  def draw(self):

    self.shapes[0].color = (np.array([255,0,0]) + np.array([0,255,255])*(self.max_charge-self.charge)/self.max_charge).astype(int)
    super().draw()

    # draw charge intensity (aura)
    impulse_shape = shapes.Circle(self.end.x,
                                  self.end.y,
                                  self.radius,
                                  color=(255, 0, 0),
                                  batch=batch)
    #print(self.charge)
    # impulse_shape.opacity = 100

    self.get_potential()

    #if self.transmitting:

        #if self.transmitting:

    if self.charge < self.max_charge and self.charging:
        self.charge += self.max_charge/5

    elif self.charge > self.max_charge and self.charging:
        self.charging = False

    else:
        DECAY = 0.07
        self.charge *= 1-DECAY # decrease the charge
        float_opacity = 1.0
        float_opacity *= 1- DECAY
        impulse_shape.opacity = int(float_opacity)

class SimpleNeuron(Neuron):

  def __init__(self, point: Point, parent: Union[Receptor, Type["Neuron"]]):
    super().__init__(point, parent)

    self.transmitting = False
    self.charge = Charge(self)
    self.shapes.append(self.charge)
    print("Hello world")
    self.transmitting = False

  def activate(self):
    pass

@window.event
def on_draw():
	window.clear()
	#batch.draw()
	diag1.draw()

diag1 = CompleteDiagram()

TREE_WIDTH_OFFSET = 480
NUM_RECEPTORS = 4
for i in range(NUM_RECEPTORS):
	if i % 2:
		Receptor(Point(200 + i * TREE_WIDTH_OFFSET, 40), diag1)
	else:
		Receptor(Point(50 + i * TREE_WIDTH_OFFSET, 30), diag1)

corner = Electrode(Point(0, 0), diag1)


@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.LEFT:
		for i, rec in enumerate(diag1.receptors):
			if i % 2 == 0:
				rec.activation()
	if symbol == key.RIGHT:
		for i, rec in enumerate(diag1.receptors):
			if i % 2 == 1:
				rec.activation()



if __name__ == "__main__":

    for i, rec in enumerate(diag1.receptors):
        if i % 2:
            n1 = SimpleNeuron(Point(330 + i * TREE_WIDTH_OFFSET, 90), rec)
            n2 = SimpleNeuron(Point(340 + i * TREE_WIDTH_OFFSET, 300), n1)
            t1 = TriangularNeuron(Point(400 + i * TREE_WIDTH_OFFSET, 370), n2)
            n3 = SimpleNeuron(Point(120 + i * TREE_WIDTH_OFFSET, 180), rec)
            n4 = SimpleNeuron(Point(200 + i * TREE_WIDTH_OFFSET, 290), n3)
            t2 = TriangularNeuron(Point(250 + i * TREE_WIDTH_OFFSET, 385), n4)
            n5 = SimpleNeuron(Point(50 + i * TREE_WIDTH_OFFSET, 365), n3)
            t3 = TriangularNeuron(Point(100 + i * TREE_WIDTH_OFFSET, 400), n5)
        else:
            t1 = TriangularNeuron(Point(55 + i * TREE_WIDTH_OFFSET, 190), rec)
            n1 = SimpleNeuron(Point(200 + i * TREE_WIDTH_OFFSET, 120), rec)
            t2 = TriangularNeuron(Point(380 + i * TREE_WIDTH_OFFSET, 110), n1)
            n2 = SimpleNeuron(Point(180 + i * TREE_WIDTH_OFFSET, 310), n1)
            t3 = TriangularNeuron(Point(40 + i * TREE_WIDTH_OFFSET, 400), n2)
            n3 = SimpleNeuron(Point(270 + i * TREE_WIDTH_OFFSET, 290), n2)
            t4 = TriangularNeuron(Point(400 + i * TREE_WIDTH_OFFSET, 380), n3)

    window.set_fullscreen(True)
    pyglet.app.run()


# @window.event
# def on_draw():
#   window.clear()
#   #batch.draw()
#   diag1.draw()
#   d = pyglet.clock.tick()
#   fl = pyglet.text.Label(f'{1/d:.0f} FPS',
#                          color=(255, 255, 255, 255),
#                          font_name='Arial',
#                          font_size=20,
#                          x=10,
#                          y=570)
#   fl.draw()


# diag1 = CompleteDiagram()
# r1 = Receptor(Point(50, 60), diag1)
# r2 = Receptor(Point(150, 60), diag1)
# corner = Electrode(Point(1000, 600), diag1)


# @window.event
# def on_key_press(symbol, modifiers):

#   if symbol == key.SPACE:
#     r1.activation()
#     r2.activation()


# if __name__ == "__main__":

#   n1 = SimpleNeuron(Point(150, 100), r1)
#   #n1.transmitting = True
#   t1 = TriangularNeuron(Point(90, 140), n1)
#   n2 = SimpleNeuron(Point(190, 200), n1)

#   t2 = TriangularNeuron(Point(160, 250), n2)
#   n3 = SimpleNeuron(Point(220, 240), n2)

#   nn1 = SimpleNeuron(Point(250, 100), r2)
#   #n1.transmitting = True
#   tt1 = TriangularNeuron(Point(190, 140), nn1)
#   nn2 = SimpleNeuron(Point(290, 200), nn1)
#   tt2 = TriangularNeuron(Point(260, 250), nn2)
#   #r1.activation()
#   pyglet.app.run()
