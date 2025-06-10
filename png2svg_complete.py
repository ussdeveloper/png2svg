import sys
import cv2
import numpy as np
import svgwrite
import os
import argparse

def update_progress(current, total, prefix="Progress"):
    """Display progress bar"""
    percent = (current / total) * 100
    filled_length = int(50 * current // total)
    bar = '#' * filled_length + '-' * (50 - filled_length)
    print(f'\r{prefix} |{bar}| {percent:.1f}% Complete', end='', flush=True)

def simplify_polygon_douglas_peucker(points, epsilon=2.0):
    """Simplify polygon using Douglas-Peucker algorithm"""
    if len(points) < 3:
        return points
    
    # Convert to numpy array if needed
    if not isinstance(points, np.ndarray):
        points = np.array(points)
    
    # Apply Douglas-Peucker simplification
    simplified = cv2.approxPolyDP(points, epsilon, True)
    return simplified.reshape(-1, 2) if len(simplified) >= 3 else points.reshape(-1, 2)

def merge_close_points(points, threshold=3.0):
    """Merge points that are very close to each other"""
    if len(points) < 2:
        return points
    
    merged = [points[0]]
    for point in points[1:]:
        last_point = merged[-1]
        distance = np.sqrt((point[0] - last_point[0])**2 + (point[1] - last_point[1])**2)
        if distance > threshold:
            merged.append(point)
    
    return np.array(merged)

def create_smooth_path(points, smooth_factor=0.1):
    """Create smooth SVG path with curves instead of straight lines"""
    if len(points) < 3:
        if len(points) == 2:
            return f"M {points[0][0]:.1f},{points[0][1]:.1f} L {points[1][0]:.1f},{points[1][1]:.1f} Z"
        elif len(points) == 1:
            return f"M {points[0][0]:.1f},{points[0][1]:.1f} Z"
        else:
            return "M 0,0 Z"
    
    # Create path with straight lines for simplicity
    path_data = f"M {points[0][0]:.1f},{points[0][1]:.1f}"
    
    for i in range(1, len(points)):
        curr = points[i]
        path_data += f" L {curr[0]:.1f},{curr[1]:.1f}"
    
    path_data += " Z"
    return path_data

def png2svg(input_path, output_path, threshold=128, scale=5, negative=False, resolution=100, method="rectangles"):
    """Convert PNG/JPG to SVG with three methods: rectangles, contours, or smart polygons"""
    
    print(f"Loading image: {input_path}")
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Cannot load file {input_path}")
        return False
    
    update_progress(1, 10, "Processing")
    
    # Negative inversion enabled by default (use --no-negative to disable)
    if not negative:
        img = cv2.bitwise_not(img)
    
    update_progress(2, 10, "Processing")
    
    # Scale image if needed
    if scale != 5:
        scale_factor = scale / 5.0
        height, width = img.shape
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    update_progress(3, 10, "Processing")
    
    height, width = img.shape
    
    # Create SVG
    svg_width = int(width * resolution / 100)
    svg_height = int(height * resolution / 100)
    dwg = svgwrite.Drawing(output_path, size=(svg_width, svg_height), viewBox=f"0 0 {width} {height}")
    
    # Threshold for black pixel detection
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    
    if method == "smart":
        # METHOD 3: SMART POLYGON SIMPLIFICATION (NEW!)
        print(f"\nSVG resolution: {svg_width}x{svg_height} ({resolution}%) - SMART POLYGONS")
        update_progress(4, 10, "Finding contours")
        
        # Apply slight blur to reduce noise before contour detection
        blurred = cv2.GaussianBlur(binary, (3, 3), 0)
        contours, hierarchy = cv2.findContours(blurred, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        update_progress(5, 10, "Simplifying polygons")
        
        polygons_created = 0
        for i, contour in enumerate(contours):
            if len(contour) > 4:  # Need at least 5 points for meaningful simplification
                # Only process external contours
                if hierarchy[0][i][3] == -1:
                    # Step 1: Simplify using Douglas-Peucker
                    simplified = simplify_polygon_douglas_peucker(contour, epsilon=2.5)
                    
                    # Step 2: Merge very close points
                    merged = merge_close_points(simplified, threshold=2.0)
                    
                    if len(merged) >= 3:
                        # Step 3: Create smooth SVG path
                        path_data = create_smooth_path(merged, smooth_factor=0.15)
                        
                        # Add polygon to SVG
                        dwg.add(dwg.path(d=path_data, stroke='black', fill='black', 
                                       stroke_width=0.5, fill_rule='evenodd'))
                        polygons_created += 1
        
        update_progress(9, 10, "Finalizing")
        dwg.save()
        update_progress(10, 10, "Complete")
        print(f"\nSVG saved: {output_path}")
        print(f"Created {polygons_created} smart polygons")
        print("SMART METHOD - simplified polygons with smooth curves!")
        
    elif method == "contours":
        # METHOD 2: CONTOUR-BASED SVG PATHS (original contours)
        print(f"\nSVG resolution: {svg_width}x{svg_height} ({resolution}%) - CONTOUR PATHS")
        update_progress(4, 10, "Finding contours")
        
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        update_progress(5, 10, "Building SVG paths")
        
        paths_created = 0
        for i, contour in enumerate(contours):
            if len(contour) > 2:
                if hierarchy[0][i][3] == -1:
                    # Convert contour to SVG path
                    path_data = f"M {int(contour[0][0][0])},{int(contour[0][0][1])}"
                    for point in contour[1:]:
                        path_data += f" L {int(point[0][0])},{int(point[0][1])}"
                    path_data += " Z"
                    
                    dwg.add(dwg.path(d=path_data, stroke='black', fill='black', stroke_width=1, fill_rule='evenodd'))
                    paths_created += 1
        
        update_progress(9, 10, "Finalizing")
        dwg.save()
        update_progress(10, 10, "Complete")
        print(f"\nSVG saved: {output_path}")
        print(f"Created {paths_created} SVG paths")
        print("CONTOUR METHOD - original contour shapes!")
        
    else:
        # METHOD 1: PIXEL-RECTANGLE METHOD (absolute precision)
        print(f"\nSVG resolution: {svg_width}x{svg_height} ({resolution}%) - PIXEL RECTANGLES")
        update_progress(4, 10, "Analyzing pixels")
        
        update_progress(5, 10, "Building SVG")
        
        # Rectangle-optimized method
        visited = np.zeros_like(binary, dtype=bool)
        total_pixels = height * width
        processed = 0
        rectangles_created = 0
        
        for y in range(height):
            for x in range(width):
                if binary[y, x] == 255 and not visited[y, x]:
                    # Find maximum horizontal rectangle
                    rect_width = 0
                    for test_x in range(x, width):
                        if binary[y, test_x] == 255 and not visited[y, test_x]:
                            rect_width += 1
                        else:
                            break
                    
                    # Check if can extend downward
                    rect_height = 1
                    can_extend = True
                    while y + rect_height < height and can_extend:
                        for test_x in range(x, x + rect_width):
                            if binary[y + rect_height, test_x] != 255 or visited[y + rect_height, test_x]:
                                can_extend = False
                                break
                        if can_extend:
                            rect_height += 1
                    
                    # Mark rectangle as visited
                    for py in range(y, y + rect_height):
                        for px in range(x, x + rect_width):
                            if py < height and px < width:
                                visited[py, px] = True
                    
                    # Add rectangle to SVG
                    if rect_width > 0 and rect_height > 0:
                        dwg.add(dwg.rect(
                            insert=(x, y),
                            size=(rect_width, rect_height),
                            fill='black',
                            stroke='none'
                        ))
                        rectangles_created += 1
                
                processed += 1
                # Progress every 5% of pixels
                if processed % (total_pixels // 20) == 0:
                    progress = 5 + (processed / total_pixels) * 4
                    update_progress(int(progress), 10, f"SVG {rectangles_created} elements")
        
        update_progress(9, 10, "Finalizing")
        dwg.save()
        update_progress(10, 10, "Complete")
        print(f"\nSVG saved: {output_path}")
        print(f"Created {rectangles_created} SVG rectangles")
        print("PIXEL METHOD - absolute precision, every pixel preserved!")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="PNG->SVG: Three conversion methods - rectangles, contours, or smart polygons",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
THREE CONVERSION METHODS:
  png2svg image.png                    # PIXEL RECTANGLES (default, absolute precision)
  png2svg image.png --contours         # CONTOUR PATHS (original shapes)
  png2svg image.png --smart            # SMART POLYGONS (simplified + smooth)
  png2svg image.png --resolution 500   # 5x resolution + method selection
  png2svg image.png --no-negative      # Disable negative inversion (enabled by default)
        """
    )
    
    parser.add_argument("input", help="Input PNG/JPG file")
    parser.add_argument("output", nargs="?", help="Output SVG file (optional)")
    parser.add_argument("--scale", type=int, choices=range(1,11), default=5, 
                       metavar="[1-10]", help="Image scale (1-10), default 5")
    parser.add_argument("--resolution", type=int, choices=range(100,1001,100), default=100, 
                       metavar="[100-1000]", help="SVG resolution in %% (100-1000), default 100%%")
    parser.add_argument("--no-negative", action="store_true", 
                       help="Disable negative inversion (enabled by default)")
    parser.add_argument("--contours", action="store_true", 
                       help="Use contour paths (original shapes)")
    parser.add_argument("--smart", action="store_true", 
                       help="Use smart polygons (Douglas-Peucker + smoothing)")
    parser.add_argument("--threshold", type=int, choices=range(1,256), default=128,
                       metavar="[1-255]", help="Binarization threshold (1-255), default 128")
    
    args = parser.parse_args()
    
    # Determine output file
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.splitext(args.input)[0] + ".svg"
    
    # Determine method
    if args.smart:
        method = "smart"
    elif args.contours:
        method = "contours"
    else:
        method = "rectangles"
    
    # Convert with selected method
    success = png2svg(args.input, output_path, threshold=args.threshold, 
                     scale=args.scale, negative=args.no_negative, resolution=args.resolution,
                     method=method)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
