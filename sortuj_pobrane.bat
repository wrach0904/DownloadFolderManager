@echo off
:: 1. Zabijamy stare procesy, żeby nie dublować
taskkill /f /im pythonw.exe >nul 2>&1

:: 2. Uruchamiamy pythonw.exe z PEŁNĄ ścieżką do skryptu main.pyw
:: WAŻNE: Sprawdź czy main.pyw ma 'w' na końcu w nazwie pliku na dysku!
start "" "C:\Program Files\Python311\pythonw.exe" "C:\Users\damne\OneDrive\Documents\PyCharm\PythonPROGRAMS\download_folder_manager\main.pyw"

:: 3. Koniec
exit