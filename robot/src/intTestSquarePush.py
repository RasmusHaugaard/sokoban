import setup
from path import Path
from forward import Forward
from center import Center
from turnSafe import Turn
from push import Push

# infinite square push sequence
path = Path('fplfrfr', [Forward(), Center(), Turn(), Push()], repeat=True)
setup.run(path)
