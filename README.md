# Sokoban
This project was done as a part of the AI introduction course at TEK, Southern University of Denmark.

The problem is two-fold;
An algorithm should to be built to solve Sokoban maps, 
and a physical robot should be designed and programmed to execute the solution.

This repository contains both parts; 
An A* algorithm to find a solution to a given Sokoban map, 
and the software implementation for our robot design.

The two parts represent traditional, logic-based AI and embodied AI, respectively, and are glued together with an instruction string of basic moves like *fr* for *go forward and turn right*.

### How to run the solver
The programs are run as python modules from the project root directory.

The following command runs the 2018 competition map with the can-closest (d_closest) heuristic.
```bash
$ python3 -m solver.solve solver/maps/2018-compitition-map.txt d_closest
```

The solution can be shown graphically with this command:
```bash
$ python3 -m solver.util.exploreSolution solver/solutions/2018{...}.txt
```

The solution string for the robot can be printed by:
```bash
$ python3 -m solver.util.createPath solver/solutions/2018{...}.txt
```
