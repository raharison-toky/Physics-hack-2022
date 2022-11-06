## What it does

- This program simulates the chain reaction that happens when sensory neurons detect a stimuli.

<img src="demo.gif" alt="drawing" width="600"/>

## How we built the project

- The project consists of two main parts: the animations and the calculations.  
- Both parts are done by the different classes that interact with other classes to transmit the signal and to do the visuals with Pyglet
- In this model, pressing keys will trigger an action potential that will spread until the message reaches the pyramidal neurons that then become polarized
- The polarization causes a change in the Electric potential and that is what's measured

## Challenges we faced

 - The animation was slightly hard to figure out because we wanted to place the picture of the neurons at varying distances and orientations from each other while we had static images. To solve this issue, we had to split the neuron image into two parts: the head and the branch. The head of the neuron will always be the same while the branch can be elongated or compressed length-wise in order to reach the correct distance. We also used trigonometry with the neuron heads' coordinates to determine the degrees of rotation for all objects, save for the charges.

