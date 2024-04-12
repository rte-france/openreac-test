import pathlib

# local imports
from utils import *
from networks import *

# common paths
ROOT_PROJECT = pathlib.Path(__file__).parent.parent.parent.parent
OUTPUT_PATH = ROOT_PROJECT / "output" / "tempo"
AMPL_CODE_PATH = ROOT_PROJECT / "ampl"
RESOURCES_PATH = ROOT_PROJECT / "python" / "resources" / "ampl_divided"