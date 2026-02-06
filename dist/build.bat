@echo off

uv run nuitka src/zcli.py --onefile --output-dir=dist/windows --output-filename=zcli.exe --assume-yes-for-downloads

REM uv run nuitka src/zcli.py --onefile --output-dir=dist/linux --output-filename=zlm

uv run nuitka src/zlm.py --onefile --output-dir=dist/windows --output-filename=zlm.exe --assume-yes-for-downloads

REM uv run nuitka src/zlm.py --onefile --output-dir=dist/linux --output-filename=zlm 


cd .\dist\windows
rmdir /s /q zcli.build
rmdir /s /q zcli.dist
rmdir /s /q zcli.onefile-build
rmdir /s /q zlm.build
rmdir /s /q zlm.dist
rmdir /s /q zlm.onefile-build

cd ..\linux
rmdir /s /q zcli.build
rmdir /s /q zcli.dist
rmdir /s /q zcli.onefile-build
rmdir /s /q zlm.build
rmdir /s /q zlm.dist
rmdir /s /q zlm.onefile-build