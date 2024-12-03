
python -m venv ./venv-windows
source ./venv-windows/Scripts/activate.bat
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "Buckshot Helper" --add-data "styles/Adwaita.qss:styles" --add-data "styles/Adwaita-Dark.qss:styles" ./BuckShotHelper.py
echo.
echo Build Done
echo.
dir ./dist/
