@echo off
setlocal

:: Set the working directory
set OUTPUT_DIR=%USERPROFILE%\Zephyr

:: Create output directory if it doesn't exist
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Change to the output directory
cd /d "%OUTPUT_DIR%"

:: Download main and dependency scripts from GitHub
curl -o zephyr.py https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/zephyr.py
curl -o main.py https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/main.py
curl -o functions.py https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/functions.py

:: Compile the main Python script (PyInstaller will detect the imported files)

pyinstaller --onefile --add-data "main.py;." --add-data "functions.py;." zephyr.py --distpath %OUTPUT_DIR%


:: Clean up unnecessary files
del zephyr.py functions.py main.py
rd /s /q __pycache__
rd /s /q build
del zephyr.spec
rd dist

echo %OUTPUT_DIR%
setx PATH "%PATH%;%OUTPUT_DIR%"

echo "Compilation Complete! Your EXE is at %OUTPUT_DIR%\main.exe"
echo "You can now run 'zephyr' from anywhere in the command prompt!"
endlocal
