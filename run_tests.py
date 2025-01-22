import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

os.chdir(SCRIPT_DIR)
cmd_str = ". ./.venv/bin/activate && coverage run -m pytest ."
os.system(cmd_str)

# Viewing Coverage
os.system("coverage html")
