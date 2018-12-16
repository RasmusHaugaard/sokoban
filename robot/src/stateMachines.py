from .linefollowing import LineFollowing
from .homing import Homing
from .forward import Forward
from .center import Center
from .turn import Turn
from .push import Push
from .path import Path


def get_default_state_machines():
    return [LineFollowing(), Homing(), Forward(), Center(), Turn(), Push()]
