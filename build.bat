@echo off
echo Building png2svg.exe...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install PyInstaller
    if errorlevel 1 (
        echo ERROR: Cannot install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if opencv-python is installed
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo Installing opencv-python...
    python -m pip install opencv-python
    if errorlevel 1 (
        echo ERROR: Cannot install opencv-python
        pause
        exit /b 1
    )
)

REM Check if svgwrite is installed
python -c "import svgwrite" >nul 2>&1
if errorlevel 1 (
    echo Installing svgwrite...
    python -m pip install svgwrite
    if errorlevel 1 (
        echo ERROR: Cannot install svgwrite
        pause
        exit /b 1
    )
)

REM Check if numpy is installed
python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing numpy...
    python -m pip install numpy
    if errorlevel 1 (
        echo ERROR: Cannot install numpy
        pause
        exit /b 1
    )
)

echo All dependencies installed successfully!
echo.

REM Remove previous build folders
if exist "build" (
    echo Removing build folder...
    rmdir /s /q "build"
)

if exist "dist" (
    echo Removing dist folder...
    rmdir /s /q "dist"
)

if exist "png2svg.spec" (
    echo Removing png2svg.spec...
    del "png2svg.spec"
)

echo.
echo Building executable...
python -m PyInstaller --onefile --strip --clean --name png2svg png2svg.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo SUCCESS: png2svg.exe built successfully!
echo Location: %CD%\dist\png2svg.exe
echo.

REM Test if exe works
echo Testing executable...
dist\png2svg.exe --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: Executable may not work correctly
) else (
    echo Test successful - executable works!
)

echo.
pause
