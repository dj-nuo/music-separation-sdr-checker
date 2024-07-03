# Usage
See example in `main.py`
Results will be written to `results.csv` (averaged) and `results_audit.csv` (per track)

# Tests
Run `pytest`

# Dev Container & Host home folder
Ideally, lauch virtual environment in Docker container using VSCode "Dev Container". 

`Ctrl/Cmd + Shift + P` -> `Dev Containers: Reopen in container`

`.devcontainer/devcontainer.json` has configuration to expose your user home folder on the root `/` in the container

# Credits
Inspired by `https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/utils.py`