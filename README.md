 # PERT Planning and Visualization using Python and Pygame

This project implements project planning using the **PERT (Program Evaluation and Review Technique)** method. It models various elements of a project, such as tasks and stages, and computes important scheduling metrics like early and late start/finish dates, critical path, and project duration. Additionally, it provides a visual representation of the PERT diagram using **Pygame**.

## Features

- **PERT Diagram Representation**: Model and visualize project tasks and stages using the PERT method.
- **Task Scheduling**: Calculate early and late start/finish dates for each task and stage.
- **Critical Path Calculation**: Identify the critical path through tasks with zero float.
- **Graphical Visualization**: Display the PERT diagram using Pygame, a 2D game development library.

## Classes Overview

The project is structured using several classes to model the elements of the PERT diagram:

- **Pert**: Represents the PERT diagram, containing all the elements (tasks, stages, etc.).
- **Task**: Represents a task, with attributes such as name, predecessors, successors, earliest and latest start/finish dates, duration, start stage, and end stage.
- **Stage**: Represents a stage, containing a stage number and the earliest and latest dates.
- **Interface**: Responsible for drawing the PERT diagram using Pygame. This class handles the visualization of tasks and stages.

## How the PERT Calculation Works

To calculate the scheduling of tasks and visualize the PERT diagram, the following steps are performed:

1. **Creation of Task List**: Define all tasks involved in the project.
2. **Predecessor List Construction**: Build a list of task dependencies (which tasks must be completed before others can start).
3. **Minimal Precedence Table**: Reduce the precedence table to its minimal form.
4. **Generation of Task and Stage Levels**: Create levels of tasks and stages to organize the flow of the project.
5. **Add Task Successors**: Define which tasks follow each other.
6. **Stage Creation and Task Assignment**: Create stages and associate tasks with their corresponding stages.
7. **Earliest Dates Calculation**: Compute the earliest possible start and finish dates for each stage.
8. **Latest Dates Calculation**: Compute the latest possible start and finish dates for each stage.
9. **Slack Calculation**: Calculate total, free, and independent float (slack) for each stage.
10. **Minimum Project Duration**: Determine the minimum time required to complete the project.
11. **Critical Path Calculation**: Identify the critical path by finding tasks with zero float.
12. **PERT Diagram Visualization**: Use the `Interface` class to display the PERT diagram graphically with Pygame.

## Requirements

To run this project, you will need:

- Python 3.x
- Pygame library

You can install Pygame using pip:

pip install pygame
