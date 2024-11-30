#!/bin/bash

#pyinstaller --name "buckshothelper_out" ./BuckShotHelper.py
#cp -r ./dist/buckshothelper_out/_internal/PyQt5 ./lib/

if [[ "$1" != "--use-system-packages" ]]; then
    python -m venv ./venv-linux
    source ./venv-linux/bin/activate
    pip install -r requirements.txt
else
    echo "Using system packages"
fi

#pyinstaller --name "buckshothelper" --add-data "lib/plugins:PyQt5/Qt5/plugins" ./BuckShotHelper.py
pyinstaller --onefile --name "buckshothelper" --add-data "lib/plugins:PyQt5/Qt5/plugins" ./BuckShotHelper.py

echo " "
echo "Packaging Complete"
echo " "

ls -lh ./dist/
