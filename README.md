 # PERT Planning and Visualization using Python and Pygame

This project demonstrates the application of the PERT (Program Evaluation and Review Technique) method for project scheduling and task planning. Using Python and Pygame, it simulates the calculation of task schedules and visualizes the result in a PERT diagram.

The program models various project components such as tasks, their dependencies (predecessors and successors), and calculates key scheduling information like earliest and latest start dates, task durations, and slack (free time). The final output includes both the task scheduling data and a visual representation of the PERT diagram.

<img width="1287" alt="Capture d’écran 2025-01-06 à 17 27 01" src="https://github.com/user-attachments/assets/bc38226c-d2bc-4d50-8599-c3604580b834" />


## Features
- **Task Scheduling**: Create tasks with names, durations, dependencies, and calculate earliest and latest start dates.
- **Critical Path Calculation**: Identify the critical path — the sequence of tasks with zero slack that directly impacts the project timeline.
- **Slack Calculation**: Calculate total, free, and certain slack for each task.
- **PERT Diagram Visualization**: Display the PERT diagram using the Pygame library.

## Classes Overview

The project is structured using several classes to model the elements of the PERT diagram:
The project uses several key classes to model the PERT diagram and task scheduling:

- **Pert**: Represents a PERT diagram, containing all the tasks and associated elements.
- **Task**: Models a task with key properties such as name, predecessors, successors, earliest and latest start dates, duration, start and end steps, etc.
- **Step**: Represents a project step with attributes like step number, earliest and latest dates.
- **Interface**: Visualizes the PERT diagram using Pygame, a Python library for creating 2D games and visualizations.

## How the PERT Calculation Works

To calculate the scheduling of tasks and visualize the PERT diagram, the following steps are performed:
Steps to Calculate and Visualize the PERT Diagram

The following steps are taken to calculate the task schedule and visualize the PERT diagram:

- **:Construct a List of Tasks**:: Create tasks with specified durations and dependencies.
- **:Identify Predecessors**:: Determine task dependencies.
- **:Reduce the Minimal Precedence Table**:: Simplify the list of dependencies.
- **:Generate Task Levels**:: Group tasks into steps based on dependencies.
- **:Add Task Successors**:: Link tasks to their successors.
- **:Create Steps**:: Define project steps and associate them with tasks.
- **:Calculate Earliest Dates**:: Compute the earliest possible start date for each step.
- **:Calculate Latest Dates**:: Compute the latest permissible start date for each step.
- **:Calculate Total, Free, and Certain Slack**:: Determine how much flexibility is available in task scheduling.
- **:Determine Minimum Project Duration**:: Calculate the shortest time required to complete the project.
- **:Identify the Critical Path**:: Highlight the sequence of tasks with zero free slack.
- **:Visualize the PERT Diagram**:: Use the Interface class to display the task schedule and critical path.

## Requirements

Dependencies : 

- Python 3.x
- Pygame library (pip install pygame)

## How to run :
python main.py

# Known Issues

The game window size is fixed.

# License

This game is open-source and available under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.


