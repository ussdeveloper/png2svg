#!/bin/bash

echo "Building png2svg.exe..."
echo ""

# Sprawdź czy Python jest zainstalowany
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python nie jest zainstalowany"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Używam: $PYTHON_CMD"

# Sprawdź czy pip jest dostępny
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "ERROR: pip nie jest dostępny"
    exit 1
fi

# Funkcja instalacji pakietu
install_package() {
    echo "Instaluję $1..."
    $PYTHON_CMD -m pip install $1
    if [ $? -ne 0 ]; then
        echo "ERROR: Nie można zainstalować $1"
        exit 1
    fi
}

# Sprawdź i zainstaluj zależności
$PYTHON_CMD -c "import cv2" 2>/dev/null || install_package "opencv-python"
$PYTHON_CMD -c "import svgwrite" 2>/dev/null || install_package "svgwrite"
$PYTHON_CMD -c "import numpy" 2>/dev/null || install_package "numpy"
$PYTHON_CMD -m PyInstaller --version &>/dev/null || install_package "PyInstaller"

echo "Wszystkie zależności zainstalowane pomyślnie!"
echo ""

# Usuń poprzednie build foldery
[ -d "build" ] && rm -rf "build"
[ -d "dist" ] && rm -rf "dist"
[ -f "png2svg.spec" ] && rm "png2svg.spec"

echo "Budowanie exe..."
$PYTHON_CMD -m PyInstaller --onefile --strip --clean --name png2svg png2svg.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Budowanie nie powiodło się!"
    exit 1
fi

echo ""
echo "SUCCESS: png2svg.exe zbudowany pomyślnie!"
echo "Lokalizacja: $(pwd)/dist/png2svg"
echo ""

# Test czy exe działa
echo "Testowanie exe..."
if ./dist/png2svg --help &>/dev/null; then
    echo "Test pomyślny - exe działa!"
else
    echo "WARNING: Exe może nie działać poprawnie"
fi

echo ""
