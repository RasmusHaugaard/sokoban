#!/usr/bin/python3
from .src import setup
from .src.stateMachines import Path, get_default_state_machines

sol = "fplfrfffrffffrffprflflfffprflflfffprflflfplfffrfffrffflfflflfplfrfrffprflflfffprflflfplffffrffflffflflfffplfrfrffprflflffffprrffffrfflffflfflflfplfrfrfffplfrfrffprflflfffprflfflfffpllfrfplfplfrfrfP"

path = Path(sol, get_default_state_machines())
setup.run(path)
