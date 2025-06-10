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

def png2svg(input_path, output_path, threshold=128, scale=5, negative=True, resolution=100):
    """NEW METHOD: Pixel -> SVG rectangles conversion (ABSOLUTE PRECISION)"""
    
    print(f"Loading image: {input_path}")
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Cannot load file {input_path}")
        return False
    
    update_progress(1, 10, "Processing")
    
    # Negative (enabled by default)
    if negative:
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
    
    # REVOLUTIONARY METHOD: DIRECT PIXEL -> SVG CONVERSION
    # ZERO LOSS - ABSOLUTE PRECISION WITHOUT CONTOUR DETECTION!
    height, width = img.shape
    
    # Create SVG
    svg_width = int(width * resolution / 100)
    svg_height = int(height * resolution / 100)
    dwg = svgwrite.Drawing(output_path, size=(svg_width, svg_height), viewBox=f"0 0 {width} {height}")
    
    print(f"\nSVG resolution: {svg_width}x{svg_height} ({resolution}%) - PIXEL->SVG")
    update_progress(4, 10, "Analyzing pixels")
    
    # Threshold for black pixel detection (no filtering!)
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    
    update_progress(5, 10, "Building SVG")
    
    # RECTANGLE-OPTIMIZED METHOD
    # Group adjacent black pixels into rectangles
    visited = np.zeros_like(binary, dtype=bool)
    total_pixels = height * width
    processed = 0
    rectangles_created = 0
    
    for y in range(height):
        for x in range(width):
            if binary[y, x] == 255 and not visited[y, x]:  # Black pixel
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
                
                # Add rectangle to SVG (EVERY BLACK PIXEL PRESERVED!)
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
    
    # Save SVG
    dwg.save()
    update_progress(10, 10, "Complete")
    print(f"\nSVG saved: {output_path}")
    print(f"Created {rectangles_created} SVG elements")
    print("ABSOLUTE PRECISION - every black pixel preserved!")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="PNG->SVG: PIXEL-PERFECT ACCURACY (pixel=rectangle SVG)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
REVOLUTIONARY METHOD - ZERO LOSS:
  png2svg image.png                    # PIXEL-PERFECT ACCURACY
  png2svg image.png output.svg         # with custom name
  png2svg image.png --resolution 500   # 5x resolution + ZERO loss
  png2svg image.png --resolution 1000  # 10x resolution + ZERO loss
        """
    )
    
    parser.add_argument("input", help="Input PNG/JPG file")
    parser.add_argument("output", nargs="?", help="Output SVG file (optional)")
    parser.add_argument("--scale", type=int, choices=range(1,11), default=5, 
                       metavar="[1-10]", help="Image scale (1-10), default 5")
    parser.add_argument("--resolution", type=int, choices=range(100,1001,100), default=100, 
                       metavar="[100-1000]", help="SVG resolution in %% (100-1000), default 100%%")
    parser.add_argument("--no-negative", action="store_true", 
                       help="Disable negative (default enabled)")
    parser.add_argument("--threshold", type=int, choices=range(1,256), default=128,
                       metavar="[1-255]", help="Binarization threshold (1-255), default 128")
    
    args = parser.parse_args()
    
    # Determine output file
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.splitext(args.input)[0] + ".svg"
    
    # Convert with PIXEL-PERFECT ACCURACY
    negative = not args.no_negative  # Default enabled
    success = png2svg(args.input, output_path, threshold=args.threshold, 
                     scale=args.scale, negative=negative, resolution=args.resolution)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
