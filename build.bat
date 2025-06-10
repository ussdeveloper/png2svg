@echo off
echo Building png2svg.exe...
echo.

REM Sprawdz czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nie jest zainstalowany lub nie jest w PATH
    pause
    exit /b 1
)

REM Sprawdz czy PyInstaller jest zainstalowany
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo Instaluję PyInstaller...
    python -m pip install PyInstaller
    if errorlevel 1 (
        echo ERROR: Nie można zainstalować PyInstaller
        pause
        exit /b 1
    )
)

REM Sprawdz czy opencv-python jest zainstalowany
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo Instaluję opencv-python...
    python -m pip install opencv-python
    if errorlevel 1 (
        echo ERROR: Nie można zainstalować opencv-python
        pause
        exit /b 1
    )
)

REM Sprawdz czy svgwrite jest zainstalowany
python -c "import svgwrite" >nul 2>&1
if errorlevel 1 (
    echo Instaluję svgwrite...
    python -m pip install svgwrite
    if errorlevel 1 (
        echo ERROR: Nie można zainstalować svgwrite
        pause
        exit /b 1
    )
)

REM Sprawdz czy numpy jest zainstalowany
python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo Instaluję numpy...
    python -m pip install numpy
    if errorlevel 1 (
        echo ERROR: Nie można zainstalować numpy
        pause
        exit /b 1
    )
)

echo Wszystkie zależności zainstalowane pomyślnie!
echo.

REM Usun poprzednie build foldery
if exist "build" (
    echo Usuwam folder build...
    rmdir /s /q "build"
)

if exist "dist" (
    echo Usuwam folder dist...
    rmdir /s /q "dist"
)

if exist "png2svg.spec" (
    echo Usuwam png2svg.spec...
    del "png2svg.spec"
)

echo.
echo Budowanie exe...
python -m PyInstaller --onefile --strip --clean --name png2svg png2svg.py

if errorlevel 1 (
    echo.
    echo ERROR: Budowanie nie powiodło się!
    pause
    exit /b 1
)

echo.
echo SUCCESS: png2svg.exe zbudowany pomyślnie!
echo Lokalizacja: %CD%\dist\png2svg.exe
echo.

REM Test czy exe działa
echo Testowanie exe...
dist\png2svg.exe --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: Exe może nie działać poprawnie
) else (
    echo Test pomyślny - exe działa!
)

echo.
pause
