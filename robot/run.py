from .src import setup
from .src.stateMachines import Path, get_default_state_machines
import sys

assert len(sys.argv) > 1, 'no argument given'

path = Path(sys.argv[1], get_default_state_machines())
setup.run(path)
