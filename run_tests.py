import os
import subprocess
import sys

SCRIPT_DIR = os.getcwd()

# Define paths
venv_activate = os.path.join(SCRIPT_DIR, ".venv", "Scripts", "activate.bat")
pytest_cmd = f'"{venv_activate}" & coverage run -m pytest .'

# Print and execute the command
print(f"Running tests: {pytest_cmd}")

try:
    subprocess.run(pytest_cmd, shell=True, check=True)
    print("Generating coverage report...")
    subprocess.run("coverage html", shell=True, check=True)
    print("Coverage report generated successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Open coverage report
open_report = os.path.join(SCRIPT_DIR, "htmlcov", "index.html")
pytest_cmd = f'start "" "{open_report}"'
try:
    subprocess.run(pytest_cmd, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)
