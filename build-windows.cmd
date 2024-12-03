
python -m venv ./venv-windows
source ./venv-windows/Scripts/activate.bat
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "Buckshot Helper" ./BuckShotHelper.py
echo.
echo Build Done
echo.
dir ./dist/
