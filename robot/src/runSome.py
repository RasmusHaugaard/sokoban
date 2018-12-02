#!/usr/bin/python3
import setup
from stateMachines import Path, get_default_state_machines

sol = "fffrflflfprrfllfffprflfrffrfrfffplffrfffrffflflffprflflffffprflflffprflfflfplfffP"

path = Path(sol, get_default_state_machines())
setup.run(path)
