# Contributing to PNG2SVG

Thank you for your interest in contributing to PNG2SVG! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/yourusername/png2svg.git
   cd png2svg
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Test the installation**
   ```bash
   python png2svg.py --help
   python png2svg.py example.png test.svg --smart
   ```

## 🛠️ Development Workflow

### Branch Strategy
- **main**: Stable releases only
- **develop**: Integration branch for features
- **feature/**: New features (`feature/add-bezier-curves`)
- **bugfix/**: Bug fixes (`bugfix/fix-memory-leak`)
- **hotfix/**: Critical fixes for production

### Creating a Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes
1. Write code following the style guidelines below
2. Add tests for new functionality
3. Update documentation if needed
4. Test thoroughly across different image types

### Committing Changes
```bash
git add .
git commit -m "feat: add new polygon smoothing algorithm

- Implement Catmull-Rom spline smoothing
- Add --smooth-factor parameter
- Improve curve quality for logos
- Add unit tests for smoothing functions"
```

### Commit Message Convention
- **feat**: New features
- **fix**: Bug fixes  
- **docs**: Documentation changes
- **style**: Code style/formatting
- **refactor**: Code refactoring
- **test**: Adding/updating tests
- **chore**: Build/tooling changes

## 🎯 Types of Contributions

### 🔥 Algorithm Improvements
- **New conversion methods**: Implement new vectorization algorithms
- **Performance optimizations**: Improve speed/memory usage
- **Quality enhancements**: Better shape approximation, smoother curves

**Example areas**:
- Bezier curve fitting
- Spline interpolation
- Advanced polygon simplification
- Edge detection improvements

### 🐛 Bug Fixes
- Memory leaks
- Incorrect SVG output
- Cross-platform compatibility
- Edge cases in image processing

### 📚 Documentation
- README improvements
- Code comments
- Usage examples
- API documentation

### 🧪 Testing
- Unit tests for algorithms
- Integration tests for CLI
- Performance benchmarks
- Cross-platform testing

## 📋 Code Style Guidelines

### Python Style
- Follow **PEP 8** style guide
- Use **type hints** for function parameters and returns
- Maximum line length: **88 characters** (Black formatter)
- Use **docstrings** for all functions and classes

### Function Documentation
```python
def simplify_polygon_douglas_peucker(points: np.ndarray, epsilon: float = 2.0) -> np.ndarray:
    """Simplify polygon using Douglas-Peucker algorithm.
    
    Args:
        points: Array of polygon vertices as [x, y] coordinates
        epsilon: Maximum distance threshold for point elimination
        
    Returns:
        Simplified polygon with reduced vertex count
        
    Example:
        >>> points = np.array([[0, 0], [1, 1], [2, 0]])
        >>> simplified = simplify_polygon_douglas_peucker(points, 0.5)
    """
```

### Code Organization
```
png2svg/
├── png2svg.py              # Main CLI script
├── algorithms/             # Algorithm implementations
│   ├── __init__.py
│   ├── rectangles.py       # Rectangle method
│   ├── contours.py         # Contour method
│   ├── smart_polygons.py   # Smart polygon method
│   └── utils.py            # Shared utilities
├── tests/                  # Test suite
│   ├── test_algorithms.py
│   ├── test_cli.py
│   └── test_data/          # Test images
└── docs/                   # Documentation
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_algorithms.py

# Run with coverage
python -m pytest --cov=png2svg tests/
```

### Writing Tests
```python
import pytest
import numpy as np
from algorithms.smart_polygons import simplify_polygon_douglas_peucker

def test_douglas_peucker_simple():
    """Test Douglas-Peucker with simple triangle."""
    points = np.array([[0, 0], [1, 1], [2, 0]])
    result = simplify_polygon_douglas_peucker(points, epsilon=0.5)
    assert len(result) <= len(points)
    assert result.shape[1] == 2  # [x, y] coordinates

def test_douglas_peucker_edge_cases():
    """Test edge cases for Douglas-Peucker."""
    # Empty array
    empty = np.array([]).reshape(0, 2)
    assert len(simplify_polygon_douglas_peucker(empty)) == 0
    
    # Single point
    single = np.array([[1, 1]])
    result = simplify_polygon_douglas_peucker(single)
    assert np.array_equal(result, single)
```

### Test Data
Add test images to `tests/test_data/`:
- **simple_shapes.png**: Basic geometric shapes
- **complex_logo.png**: Detailed logo for performance testing
- **pixel_art.png**: Pixel art for rectangle method
- **organic_shape.png**: Natural shapes for contour method

## 📊 Performance Considerations

### Benchmarking
```python
import time
import cProfile

def benchmark_conversion_method(image_path: str, method: str):
    """Benchmark conversion method performance."""
    start_time = time.time()
    
    # Run conversion
    result = convert_image(image_path, method=method)
    
    end_time = time.time()
    print(f"{method}: {end_time - start_time:.2f}s")
    return result

# Profile memory usage
def profile_memory():
    import tracemalloc
    tracemalloc.start()
    # ... run conversion ...
    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory: {current / 1024/1024:.1f}MB (peak: {peak / 1024/1024:.1f}MB)")
```

### Optimization Guidelines
- **Memory**: Use generators for large datasets, avoid copying arrays
- **Speed**: Vectorize operations with NumPy, minimize Python loops
- **I/O**: Batch file operations, use efficient image libraries

## 🔍 Code Review Process

### Pull Request Requirements
- [ ] **Tests pass**: All existing and new tests must pass
- [ ] **Documentation updated**: README, docstrings, comments
- [ ] **Performance tested**: No significant performance regression
- [ ] **Cross-platform**: Works on Windows, Linux, macOS
- [ ] **Code style**: Follows project conventions

### Review Checklist
- **Functionality**: Does it work as intended?
- **Performance**: Is it efficient? Any bottlenecks?
- **Readability**: Clear variable names, good structure?
- **Testing**: Adequate test coverage?
- **Documentation**: Clear docstrings and comments?

## 🏷️ Issue Guidelines

### Bug Reports
Use the bug report template:
```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**
1. Run command: `png2svg.exe image.png --smart`
2. Expected: 4 polygons
3. Actual: Error message

**Environment**
- OS: Windows 11
- Python: 3.12.6
- PNG2SVG: 2.0.0

**Test Image**
[Attach or link to problematic image]
```

### Feature Requests
```markdown
**Feature Description**
Add support for Bezier curve fitting in smart polygon method.

**Use Case**
Logos with curved elements would benefit from smooth Bezier curves
instead of linear segments.

**Proposed Implementation**
- Detect curved segments in contours
- Fit Bezier curves using least squares
- Add --bezier flag to enable feature
```

## 🎉 Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Major contributions highlighted
- **Code comments**: Algorithm authors credited

### Hall of Fame
Significant contributors:
- **Algorithm Innovation**: New conversion methods
- **Performance**: Major speed/memory improvements  
- **Quality**: Testing, documentation, code review

## 📞 Getting Help

- **GitHub Issues**: Technical questions, bug reports
- **Discussions**: Ideas, general questions
- **Discord**: Real-time chat (link in README)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to PNG2SVG! 🚀**
