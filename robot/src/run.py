import setup
from stateMachines import *
import sys

assert len(sys.argv) > 1, 'no argument given'

path = Path(sys.argv[1], [Forward(), Center(), Turn(), Push()])
setup.run(path)
