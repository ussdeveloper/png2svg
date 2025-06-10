# PNG2SVG Converter

🚀 **Revolutionary PNG/JPG to SVG converter with THREE advanced algorithms** - pixel rectangles, contour paths, and smart polygon simplification using Douglas-Peucker algorithm.

## ✨ Features

- **🎯 Three Conversion Methods**: Choose the best algorithm for your needs
- **🔥 Smart Polygons**: Douglas-Peucker algorithm for optimal shape simplification  
- **📐 Pixel-Perfect Accuracy**: Every black pixel preserved as SVG rectangles
- **🎨 Smooth Contours**: Vector paths following original image shapes
- **⚡ High Performance**: Optimized algorithms with progress bars
- **🎛️ Flexible Options**: Resolution scaling, negative inversion, custom thresholds
- **💻 Cross-Platform**: Windows EXE and Python script versions

## 🚀 Quick Start

### Method 1: Download EXE (Windows)
```bash
# Download png2svg.exe from releases
png2svg.exe image.png --smart              # Smart polygons (recommended)
png2svg.exe image.png --contours           # Smooth contours  
png2svg.exe image.png                      # Pixel rectangles (default)
```

### Method 2: Python Script
```bash
git clone https://github.com/ussdeveloper/png2svg.git
cd png2svg
pip install -r requirements.txt
python png2svg.py image.png --smart
```

## 🧠 Conversion Methods

### 🔥 1. SMART POLYGONS (Recommended)
**Best for**: Logos, graphics, geometric shapes
```bash
png2svg.exe image.png output.svg --smart --resolution 300
```
- **Algorithm**: Douglas-Peucker polygon simplification
- **Process**: Find contours → Simplify vertices → Merge close points → Smooth curves
- **Result**: Minimal SVG elements with maximum quality
- **Example**: 2000+ rectangles → 4 smart polygons (99.8% reduction!)

### 🎨 2. CONTOUR PATHS  
**Best for**: Organic shapes, illustrations
```bash
png2svg.exe image.png output.svg --contours --resolution 300
```
- **Algorithm**: OpenCV contour detection
- **Process**: Edge detection → Path tracing → SVG conversion
- **Result**: Vector paths following image boundaries
- **Example**: Complex shape → 5-15 smooth SVG paths

### 📐 3. PIXEL RECTANGLES (Default)
**Best for**: Pixel art, absolute precision needed
```bash
png2svg.exe image.png output.svg --resolution 400
```
- **Algorithm**: Pixel grouping and rectangle optimization
- **Process**: Scan pixels → Group adjacent → Create rectangles → Optimize
- **Result**: 100% accurate pixel reproduction
- **Example**: Every black pixel becomes SVG rectangle

## 📊 Performance Comparison

| Method | Elements | File Size | Quality | Speed | Best For |
|--------|----------|-----------|---------|-------|----------|
| **Smart Polygons** | **4-10** | **Smallest** | **Excellent** | **Fastest** | **Logos, Graphics** |
| **Contour Paths** | **5-50** | **Small** | **Very Good** | **Fast** | **Illustrations** |  
| **Pixel Rectangles** | **100-5000+** | **Large** | **Perfect** | **Slower** | **Pixel Art** |

## 🎛️ Command Line Options

```bash
png2svg.exe input.png [output.svg] [options]

Positional Arguments:
  input                 Input PNG/JPG file
  output                Output SVG file (optional)

Conversion Methods:
  --smart               Smart polygons (Douglas-Peucker + smoothing)
  --contours            Contour paths (original shapes)
  (default)             Pixel rectangles (absolute precision)

Quality Options:
  --resolution [100-1000]    SVG resolution % (default: 100%)
  --scale [1-10]             Image scale factor (default: 5)
  --threshold [1-255]        Binarization threshold (default: 128)

Image Processing:
  --no-negative              Disable negative inversion (enabled by default)
```

## 💡 Usage Examples

### Basic Conversion
```bash
# Smart polygons (recommended for most cases)
png2svg.exe logo.png logo.svg --smart

# High resolution with smart polygons
png2svg.exe image.png output.svg --smart --resolution 500

# Contour paths for illustrations
png2svg.exe drawing.png vector.svg --contours --resolution 300

# Pixel-perfect conversion
png2svg.exe pixelart.png precise.svg --resolution 200
```

### Advanced Options
```bash
# Disable negative inversion (for black backgrounds)
png2svg.exe image.png --smart --no-negative

# Custom threshold for fine-tuning
png2svg.exe image.png --contours --threshold 100 --resolution 400

# Maximum quality with smart polygons
png2svg.exe logo.png --smart --resolution 1000 --scale 8
```

## 🔬 Technical Details

### Douglas-Peucker Algorithm (Smart Polygons)
The smart polygon method implements the Douglas-Peucker line simplification algorithm:

1. **Contour Detection**: Find shape boundaries using OpenCV
2. **Polygon Simplification**: Reduce vertices while preserving shape accuracy
3. **Point Merging**: Combine nearby vertices for cleaner output
4. **Smooth Path Generation**: Create optimized SVG paths with curves

**Benefits**:
- 95-99% reduction in SVG elements
- Maintains visual fidelity
- Creates scalable vector graphics
- Optimized for geometric shapes

### Pixel Rectangle Method
Advanced rectangle packing algorithm:
1. **Horizontal Scanning**: Find maximum width rectangles
2. **Vertical Extension**: Extend rectangles downward when possible  
3. **Optimization**: Minimize total rectangle count
4. **Pixel Accuracy**: Every source pixel represented

### Contour Path Method
OpenCV-based vector tracing:
1. **Edge Detection**: Identify shape boundaries
2. **Hierarchy Processing**: Handle nested shapes correctly
3. **Path Conversion**: Transform contours to SVG paths
4. **Hole Support**: Proper handling of complex shapes with holes

## 🛠️ Installation

### Prerequisites
- Python 3.8+ (for script version)
- Windows 10+ (for EXE version)

### Install Dependencies
```bash
pip install opencv-python numpy svgwrite
```

### Build from Source
```bash
git clone https://github.com/ussdeveloper/png2svg.git
cd png2svg
pip install -r requirements.txt

# Run directly
python png2svg.py image.png output.svg --smart

# Build EXE (Windows)
./build.bat

# Build on Linux/macOS  
./build.sh
```

## 📈 Build System

### Windows Build
```bash
build.bat                    # Automatic build with dependency check
```

### Linux/macOS Build  
```bash
chmod +x build.sh
./build.sh                   # Cross-platform build script
```

**Build Features**:
- ✅ Automatic dependency installation
- ✅ Clean build process (removes old artifacts)
- ✅ Executable testing and validation
- ✅ PyInstaller optimization for smaller file size

## 📝 Examples and Results

### Logo Conversion (Smart Polygons)
```
Input:  company_logo.png (complex logo)
Method: --smart --resolution 300
Result: 6 SVG polygons instead of 3,247 rectangles
Size:   89% smaller file, vector scalable
```

### Illustration (Contour Paths)
```
Input:  drawing.png (hand-drawn illustration)  
Method: --contours --resolution 200
Result: 23 smooth SVG paths
Size:   Vector-perfect curves, artistic quality preserved
```

### Pixel Art (Rectangle Method)
```
Input:  sprite.png (16x16 pixel character)
Method: default --resolution 800  
Result: 94 optimized rectangles
Size:   100% pixel accuracy, 8x scale factor
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and test thoroughly
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

### Development Setup
```bash
git clone https://github.com/ussdeveloper/png2svg.git
cd png2svg
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python png2svg.py --help
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/ussdeveloper/png2svg
- **Issues**: https://github.com/ussdeveloper/png2svg/issues  
- **Releases**: https://github.com/ussdeveloper/png2svg/releases

## 🏆 Algorithm Comparison

| Feature | Smart Polygons | Contour Paths | Pixel Rectangles |
|---------|---------------|---------------|------------------|
| **Element Count** | ⭐⭐⭐⭐⭐ (Minimal) | ⭐⭐⭐⭐ (Low) | ⭐⭐ (High) |
| **File Size** | ⭐⭐⭐⭐⭐ (Smallest) | ⭐⭐⭐⭐ (Small) | ⭐⭐ (Large) |  
| **Accuracy** | ⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐⭐ (Very Good) | ⭐⭐⭐⭐⭐ (Perfect) |
| **Speed** | ⭐⭐⭐⭐⭐ (Fastest) | ⭐⭐⭐⭐ (Fast) | ⭐⭐⭐ (Moderate) |
| **Scalability** | ⭐⭐⭐⭐⭐ (Infinite) | ⭐⭐⭐⭐⭐ (Infinite) | ⭐⭐⭐⭐⭐ (Infinite) |

---

**🚀 Transform your images into perfect vectors with PNG2SVG!**
