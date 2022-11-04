@REM Compiles python scripts as executables
@REM python -m py_compile zsi_conversion.py zsi_cleanup.py cmb_cleanup.py

pyinstaller --onefile src\zsi_conversion.py
pyinstaller --onefile src\zsi_cleanup.py
pyinstaller --onefile src\cmb_cleanup.py