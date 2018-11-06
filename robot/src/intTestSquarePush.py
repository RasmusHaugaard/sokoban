import setup
from stateMachines import *

# infinite square push sequence
path = Path('fplfrfr', [Forward(), Center(), Turn(), Push()], repeat=True)
setup.run(path)
