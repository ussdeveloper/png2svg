#!/bin/bash

echo "Building png2svg executable..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using: $PYTHON_CMD"

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "ERROR: pip is not available"
    exit 1
fi

# Package installation function
install_package() {
    echo "Installing $1..."
    $PYTHON_CMD -m pip install $1
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot install $1"
        exit 1
    fi
}

# Check and install dependencies
$PYTHON_CMD -c "import cv2" 2>/dev/null || install_package "opencv-python"
$PYTHON_CMD -c "import svgwrite" 2>/dev/null || install_package "svgwrite"
$PYTHON_CMD -c "import numpy" 2>/dev/null || install_package "numpy"
$PYTHON_CMD -m PyInstaller --version &>/dev/null || install_package "PyInstaller"

echo "All dependencies installed successfully!"
echo ""

# Remove previous build folders
[ -d "build" ] && rm -rf "build"
[ -d "dist" ] && rm -rf "dist"
[ -f "png2svg.spec" ] && rm "png2svg.spec"

echo "Building executable..."
$PYTHON_CMD -m PyInstaller --onefile --strip --clean --name png2svg png2svg.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Build failed!"
    exit 1
fi

echo ""
echo "SUCCESS: png2svg executable built successfully!"
echo "Location: $(pwd)/dist/png2svg"
echo ""

# Test if executable works
echo "Testing executable..."
if ./dist/png2svg --help &>/dev/null; then
    echo "Test successful - executable works!"
else
    echo "WARNING: Executable may not work correctly"
fi

echo ""
