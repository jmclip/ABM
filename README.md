# ABM

This is a basic overview to getting started in Agent-Based Modeling. There are slides (ABMs.rmd and ABMs.html), then two model files. Schell1 is a simplified version of Schelling's Segregation model while schell2 is a more complex version. 

## Schelling's segregation model
Schelling's segregation model begins with a simple set of premises: what if agents / individuals could live anywhere, are of two groups, and have some preference for neighbors to be members of their same group? Permitting for this, we can observe that agents segregate themselves into homogenous groups with preferences starting as low as wanting 37% of their neighbors to be members of their same group. 

## What to expect
In each step of the model, agents look to their immediate neighbors (8 squares surrounding the agent) and calculate what proportion of these agents are of the same type as the agent. If this proportion is below their threshold, the agent stays in place; otherwise, the agent moves to a new random space on the grid. 

## Files
Slides for the presentation are avaiable under ABMs_slides.
Within each of the two models (schell1 and schell2), you'll find the following files:
- model.py *this is the bulk of the model and includes the agent and model classes*
- server.py *this is how the model runs are visualized*
- run.py *run this file to run the model in the gui and exports the results to a csv*
- run_single.py *this allows for a single run, bypassing the gui, and exports the results to a csv*
- run_batch.py *(for schell2) this allows you to run multiple iterations and / or run the model with different parameter value combinations, and exports the results to a csv*

