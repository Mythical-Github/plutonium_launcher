@echo off

cd /d "%~dp0"

set "base_dir=%~dp0plutonium_launcher"

if not exist  "%~dp0/plutonium_launcher" (
     "%~dp0/VirtualEnvironmentSetup.bat"
)

cd "%base_dir%"

set "c_one=uv pip install wxPython"
set "c_two=uv pip install wxPython"
set "c_three=uv pip install wxPython"
set "c_four=uv pip install wxPython"
set "c_five=uv pip install wxPython"
set "c_new=uv pip install wxPython"
set "c_six=uv pip install wxPython"
set "c_seven=uv pip install wxPython"
set "c_eight=uv pip freeze | uv pip compile - -o requirements.txt"

uv venv
.venv\Scripts\activate && %c_one% && %c_two% && %c_three% && %c_four% && %c_five% && %c_new% && %c_six% && %c_seven% && %c_eight%

pause

exit /b 0
