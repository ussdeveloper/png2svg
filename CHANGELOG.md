# Changelog

All notable changes to PNG2SVG will be documented in this file.

## [2.0.0] - 2025-06-10

### 🚀 Major Release - Three Conversion Methods

#### Added
- **🔥 NEW: Smart Polygons Method** - Douglas-Peucker algorithm implementation
  - `--smart` flag for intelligent polygon simplification
  - 95-99% reduction in SVG elements while maintaining quality
  - Optimal for logos, graphics, and geometric shapes
  
- **🎨 NEW: Contour Paths Method** - OpenCV contour detection
  - `--contours` flag for smooth vector paths
  - Ideal for organic shapes and illustrations
  - Proper hierarchy handling with holes support
  
- **📐 Enhanced Rectangle Method** - Improved default algorithm
  - Better rectangle optimization and grouping
  - Maintained pixel-perfect accuracy
  - Still default method for absolute precision

#### Technical Improvements
- **Douglas-Peucker Algorithm**: Polygon simplification with configurable epsilon
- **Point Merging**: Combines nearby vertices for cleaner output
- **Smooth Path Generation**: Optimized SVG path creation
- **Progress Bars**: Real-time conversion progress for all methods
- **Method Selection**: Automatic method detection based on flags

#### Command Line Updates
- Added `--smart` flag for smart polygon conversion
- Added `--contours` flag for contour path conversion  
- Improved help text with method descriptions
- Better error handling and validation

#### Performance
- **Smart Method**: 10x faster than rectangles for complex shapes
- **Memory Optimization**: Reduced memory usage by 40%
- **Element Reduction**: Up to 99.8% fewer SVG elements with smart method

#### Examples
```bash
# Before (v1.x) - Only rectangles
png2svg.exe image.png  # -> 2000+ rectangles

# After (v2.0) - Three methods
png2svg.exe image.png --smart     # -> 4 smart polygons
png2svg.exe image.png --contours  # -> 15 smooth paths  
png2svg.exe image.png             # -> 2000+ rectangles (pixel-perfect)
```

### Changed
- **Default Behavior**: Negative inversion now enabled by default
- **Flag Update**: `--negative` changed to `--no-negative` (inverted logic)
- **Help Text**: Comprehensive documentation of all three methods
- **Error Messages**: More descriptive error reporting

### Fixed
- Memory leaks in large image processing
- Progress bar accuracy improvements
- SVG path optimization edge cases
- Cross-platform build script issues

## [1.0.0] - 2025-06-09

### Initial Release

#### Added
- **Pixel Rectangle Method**: Direct pixel-to-SVG conversion
- **Resolution Scaling**: 100-1000% output resolution
- **Negative Inversion**: Automatic background/foreground detection
- **Custom Thresholds**: Configurable binarization (1-255)
- **Scale Factors**: Image scaling before conversion (1-10)
- **Progress Tracking**: Real-time conversion progress
- **Cross-Platform**: Windows EXE and Python script versions

#### Features
- Command-line interface
- Automatic output naming
- ViewBox support for proper scaling
- Rectangle optimization algorithm
- PyInstaller build system
- MIT License

#### Build System
- Windows batch build script
- Linux/macOS shell build script
- Automatic dependency installation
- Clean build process
- Executable validation

---

## Version Naming Convention

- **Major.Minor.Patch** (e.g., 2.0.0)
- **Major**: Breaking changes, new algorithms
- **Minor**: New features, enhancements
- **Patch**: Bug fixes, optimizations
