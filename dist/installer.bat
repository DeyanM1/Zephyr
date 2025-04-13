@echo off
setlocal EnableDelayedExpansion

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

curl -o zephyr.py     https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/dist/zephyr.py
curl -o zephyrLibraryManager.py     https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/dist/zephyrLibraryManager.py
curl -o main.py       https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/main.py
curl -o functions.py  https://raw.githubusercontent.com/DeyanM1/Zephyr/refs/heads/main/functions.py


:: ------------------------------------ ::
::           BUILD EXECUTABLE           ::
:: ------------------------------------ ::

pyinstaller --onefile --add-data "main.py;." --add-data "functions.py;." zephyr.py --distpath "%OutputDir%"

:: Clean up temporary build files
del zephyr.py functions.py main.py
del zephyr.spec
rd /s /q build

mkdir lib
echo.


pyinstaller --onefile zephyrLibraryManager.py --distpath "%OutputDir%"

:: Clean up temporary build files
del zephyr.py functions.py main.py
del zephyr.spec
rd /s /q build

mkdir lib
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
echo Installation Complete! Your EXE is at:
echo %OutputDir%\main.exe

:end
endlocal
