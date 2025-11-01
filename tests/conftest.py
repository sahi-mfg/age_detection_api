import os
import sys

# Get the directory of the 'tests' folder
tests_dir = os.path.dirname(__file__)

# Get the directory of the project root (one level up from 'tests')
project_root = os.path.abspath(os.path.join(tests_dir, os.pardir))

# Add the project root to the Python path
sys.path.insert(0, project_root)
