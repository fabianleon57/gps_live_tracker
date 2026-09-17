import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from main_functions import *

manhattan = merge_shapes_and_trips("data/MTA/gtfs_m")
print(manhattan.head())