#!/bin/bash


#uv run nuitka src/zcli.py --onefile --output-dir=dist/windows --output-filename=zcli.exe --assume-yes-for-downloads

#uv run nuitka src/zlm.py --onefile --output-dir=dist/windows --output-filename=zlm.exe --assume-yes-for-downloads

uv run nuitka src/zcli.py --onefile --output-dir=dist/linux --output-filename=zcli

uv run nuitka src/zlm.py --onefile --output-dir=dist/linux --output-filename=zlm 

./dist/buildDocs.sh


cd ./dist/windows
rm -rf zcli.build zcli.dist zcli.onefile-build zlm.build zlm.dist zlm.onefile-build

cd ../linux/
rm -rf zcli.build zcli.dist zcli.onefile-build zlm.build zlm.dist zlm.onefile-build