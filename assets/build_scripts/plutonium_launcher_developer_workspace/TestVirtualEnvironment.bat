@echo off

if not exist  "%~dp0/plutonium_launcher" (
     "%~dp0/VirtualEnvironmentSetup.bat"
)

cd /d "%~dp0/plutonium_launcher"

.venv\Scripts\activate && uv run "%CD%/src/plutonium_launcher/__main__.py"

exit /b 0
