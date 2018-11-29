#!/usr/bin/python3
import setup
from stateMachines import *

sol = "fplfrfffrffffrffprflflffffprrfffrffflfflflfplfrfrffprflflfffprflflfffprflflfplfffrffffrffflffflflfffplfrfrffprflflfffprflflfplfffrfflfffflfflflfplfrfrfffplfrfrffprflflfffprflfflfffpllfrfplfplfrfrfP"
sol1 = "fplfrfffrffffrffprflflfffprflflfffprflflfplfffrfffrffflfflflfplfrfrffprflflfffprflflfplffffrffflffflflfffplfrfrffprflflffffprrffffrfflffflfflflfplfrfrfffplfrfrffprflflfffprflfflfffpllfrfplfplfrfrfP"

path = Path(sol1, [Forward(), Center(), Turn(), Push()])
setup.run(path)
