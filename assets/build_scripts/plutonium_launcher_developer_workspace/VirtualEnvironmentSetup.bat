@echo off

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Define the base directory
set "base_dir=%~dp0plutonium_launcher"

:: Install uv if not already installed
pip install uv

:: Remove the existing directory if it exists
if not exist "%base_dir%" (
    git clone -b dev https://github.com/Mythical-Github/plutonium_launcher.git "%base_dir%"
)

:: Change to the base directory
cd "%base_dir%"

:: Set the run application command
set command=uv run "%base_dir%/src/plutonium_launcher/__main__.py"

:: Create and activate the virtual environment, then install requirements, then run the application, then pause
uv venv --python 3.10.0
.venv\Scripts\activate && uv pip install -r requirements.txt && %command%