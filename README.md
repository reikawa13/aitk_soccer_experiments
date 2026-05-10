# Evolving AITK Soccer Agent with NEAT for Robotic Simulation

In this project, we worked on training an agent to play soccer. 
## File is in: 
[aitk_soccer_experiments-master/notebooks/Advanced/EvolveSoccer.ipynb](aitk_soccer_experiments-master/notebooks/Advanced/EvolveSoccer.ipynb)

## How to run the simulation: 

Because all of the crucial code is contained in a jupyter notebook, it should be rather straight-forward to run. 

After you have established a jupyter environment: 
- Scroll down to check the config settings for NEAT. These may be changed to modify the way that the genetic algorithm behaves. You can also adjust the confic settings as well as the starting location of the objects in the world, such as the robot, the goal, and the ball. 
- Run all of the cells of the notebook. After all of the generations are done running, it will replay the individual with the highest fitness (the one that makes the goal) 
- Graphs describing the average fitness over time, the speciation, as well as a visualization of the resultant network will be generated automatically.

Note: With the current settings, checkpoints of the population will be generated every 25 generations and saved to the directory. To disable this, comment out “p.add_reporter(neat.Checkpointer(25))” in the 7th cell. 



-------------- Original README from the AITK Project ----------------------------
# aitk: Artificial Intelligence Toolkit

[![DOI](https://zenodo.org/badge/339135763.svg)](https://zenodo.org/badge/latestdoi/339135763)

This collection contains two things: an open source set of Python tools, and a set of computational essays for exploring Artificial Intelligence, Machine Learning, and Robotics. This is a collaborative effort started by the authors, building on almost a century of collective experience in education and research.

The code and essays are designed to require as few computing resources as necessary, while still allowing readers to experience first-hand the topics covered.

## Authors

* [Douglas Blank](https://github.com/dsblank/) - Emeritus Professor of Computer Science, Bryn Mawr College; Head of Research at [Comet.ml](https://comet.ml/)
* [Jim Marshall](http://science.slc.edu/~jmarshall/) - Professor in the Computer Science Department at Sarah Lawrence College
* [Lisa Meeden](https://www.cs.swarthmore.edu/~meeden/) - Professor in the Computer Science Department at Swarthmore College

## Computational Essays

Each computational essay is described at [Computational Essays](https://github.com/ArtificialIntelligenceToolkit/aitk/blob/master/ComputationalEssays.md). Our computational essays and a suggested sequencing through the notebooks can be found in the [notebooks folder](https://github.com/ArtificialIntelligenceToolkit/aitk/tree/master/notebooks) of this repo.

## Artifical Intelligence Toolkit

`aitk` is a Python package containing the following modules.

* [aitk]() - top level package
  * [aitk.robots](https://github.com/ArtificialIntelligenceToolkit/aitk/tree/master/docs/robots) - for exploring simulated mobile robots, with cameras and sensors
  * [aitk.algorithms](https://github.com/ArtificialIntelligenceToolkit/aitk/tree/master/docs/algorithms/) - for exploring algorithms
  * [aitk.networks](https://github.com/ArtificialIntelligenceToolkit/aitk/tree/master/docs/networks/) - for constructing and visualizing Keras deep learning models
  * [aitk.utils](https://github.com/ArtificialIntelligenceToolkit/aitk/tree/master/docs/utils/) - for common utilities

## AITK Community

For questions and comments, please use https://github.com/ArtificialIntelligenceToolkit/aitk/discussions/.
