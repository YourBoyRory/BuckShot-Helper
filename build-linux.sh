#!/bin/bash

python -m venv ./venv-linux
source ./venv-linux/bin/activate
pip install -r requirements.txt
pyinstaller --onefile --name "buckshothelper" --add-data "styles:PyQt5/Qt5/plugins/styles" ./BuckShotHelper.py

echo " "
echo "Packaging Complete"
echo " "

ls -lh ./dist/
