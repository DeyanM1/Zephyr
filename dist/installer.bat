@echo off
setlocal EnableDelayedExpansion



:: ------------------------------------ ::
::       CHECK PYTHON INSTALLATION      ::
:: ------------------------------------ ::

:: Check if Python 3.11 or higher is installed
for /f "delims=" %%P in ('python --version 2^>nul') do set "PythonVersion=%%P"
if not defined PythonVersion (
    echo Python 3.11 or higher is required but not found.
    echo Please install Python 3.11 or higher and try again.
    exit /b 1
)

:: Extract major and minor version
for /f "tokens=2 delims=." %%A in ("%PythonVersion:~7%") do (
    set "MajorVersion=%%A"
    set "MinorVersion=%%B"
)



if !MajorVersion! LSS 3 (
    echo Python 3.11 or higher is required but found version !PythonVersion!.
    exit /b 1
) else if !MajorVersion! EQU 3 if !MinorVersion! LSS 11 (
    echo Python 3.11 or higher is required but found version !PythonVersion!.
    exit /b 1
)

echo Python version !PythonVersion! detected.

:: Check if pyinstaller is installed using pip list
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is not installed. Installing it now...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller. Please install it manually and try again.
        exit /b 1
    )
)

echo PyInstaller is installed.






:: ------------------------------------ ::
::         SETUP: OUTPUT DIRECTORY      ::
:: ------------------------------------ ::

set "OutputDir=%USERPROFILE%\Zephyr"

:: Create the output directory if it doesn't exist
if not exist "%OutputDir%" (
    mkdir "%OutputDir%"
)

:: Change to the output directory
cd /d "%OutputDir%"


:: ------------------------------------ ::
::           DOWNLOAD SCRIPTS           ::
:: ------------------------------------ ::

curl -o zephyr.py                   https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/dist/zephyr.py
curl -o zephyrLibraryManager.py     https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/dist/zephyrLibraryManager.py
curl -o main.py                     https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/main.py
curl -o functions.py                https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/functions.py


:: ------------------------------------ ::
::           BUILD EXECUTABLE           ::
:: ------------------------------------ ::

python -m pyinstaller --onefile --add-data "main.py;." --add-data "functions.py;." zephyr.py --distpath "%OutputDir%" --name zephyr

:: Clean up temporary build files
del zephyr.py functions.py main.py
del zephyr.spec
rd /s /q build

mkdir lib
echo.
echo Installed runner
echo.


:: BUILD 2nd executable for zephyrLibraryManager.py
python -m pyinstaller --onefile zephyrLibraryManager.py --distpath "%OutputDir%" --name zlm

:: Clean up temporary build files
del zephyrLibraryManager.py zlm.spec
rd /s /q build

echo.
echo Installed library Manager


echo.
echo.


:: ------------------------------------ ::
::        ADD TO SYSTEM USER PATH       ::
:: ------------------------------------ ::

set "NewPath=%OutputDir%"
set "RegKey=HKCU\Environment"

:: Get current PATH
for /f "tokens=2*" %%A in ('reg query "%RegKey%" /v Path 2^>nul') do set "CurrentPath=%%B"

:: Check if NewPath is already in PATH
echo !CurrentPath! | findstr /I /C:"%NewPath%" >nul
if !errorlevel! == 0 (
    echo Path already exists in user PATH.
    goto :end
)

:: Append the new path
set "UpdatedPath=!CurrentPath!;%NewPath%"
reg add "%RegKey%" /v Path /t REG_EXPAND_SZ /d "!UpdatedPath!" /f
echo Path added successfully.


:: ------------------------------------ ::
::           FINAL CONFIG VARS          ::
:: ------------------------------------ ::

setx ZEPHYR_PATH "%OutputDir%"
echo ZEPHYR_PATH set to %OutputDir%

echo.
echo.
echo Installation Complete! Your EXE is at:
echo %OutputDir%\main.exe

:end
endlocal
