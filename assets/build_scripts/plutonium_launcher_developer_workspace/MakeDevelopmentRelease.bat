@echo off

set "PlutoniumLauncherDir=%~dp0plutonium_launcher"
set "DevelopmentDirToZip=%PlutoniumLauncherDir%\assets\build_scripts\plutonium_launcher_developer_workspace"
set "FinalZipLocation=%~dp0Development.zip"

if not exist  "%~dp0/plutonium_launcher" (
     "%~dp0/VirtualEnvironmentSetup.bat"
)

cd /d "%PlutoniumLauncherDir%"

echo Creating zip file from %DevelopmentDirToZip% to %FinalZipLocation%
powershell -Command "Compress-Archive -Path '%DevelopmentDirToZip%' -DestinationPath '%FinalZipLocation%' -Force"
