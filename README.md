## What it does

- This program simulates the chain reaction induced by a stimulus when detected by sensory neurons.

<img src="demo.gif" alt="drawing" width="600"/>

## How we built the project

- The project consists of two main parts: the animations and the calculations.  
- Both parts are done by the different classes that interact with other classes to transmit the signal and to do the visuals with Pyglet
- In this model, pressing keys will trigger an action potential that will spread until the message reaches the pyramidal neurons that, then become polarized
- The polarization causes a change in the Electric potential, and that is what's measured

## Challenges we faced

 - The first challenge we faced was to comprehend the functioning of a neuron network and to simplify it to be able to transpose it in code. For example, we neglected the charge exchanges between the neurons and the fluid around them to only focus on the travelling signal modelized as a moving charge in the code. 

- The animation was slightly hard to figure out because we wanted to place the picture of the neurons at varying distances and orientations from each other while we had static images. To solve this issue, we had to split the neuron image into two parts: the head and the branch. The head of the neuron will always be the same, while the branch can be elongated or compressed length-wise to reach the correct distance. We also used trigonometry with the neuron heads' coordinates to determine the degrees of rotation for all objects, save for the charges.

- The charge propagation inside the neuron branches was also quite challenging. Indeed, the charge had to follow the neuron's tail and activate the following ones. Depending on whether the next neuron is a triangular neuron or a simple neuron, it does not have the same impact. For example, if it is a simple neuron, the charge continues traveling, and if it is a triangular one, it activates it. 

- It was also hard to figure out how to make each neuron interact with each other in the code. After all, all simple neurons have a charged object ready to depart. Still, it had to move only after a stimulus or receiving an electrical signal from a parent neuron. Writing the code such that the information from a previous neuron passed on to the other required much time and testing until all the neurons were synchronized correctly.

- The main challenge, in the end, was combining the animation and the main algorithm such that the changes in the code behind the screen were reflected in the animations. Some worries were that the weight of the code itself may cause lags on screen or that combining one section with the other does not yield the visuals we wanted.
