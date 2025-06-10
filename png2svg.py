import sys
import cv2
import numpy as np
import svgwrite
import os
import argparse

def update_progress(current, total, prefix="Progress"):
    """Wyswietla pasek postepu"""
    percent = (current / total) * 100
    filled_length = int(50 * current // total)
    bar = '#' * filled_length + '-' * (50 - filled_length)
    print(f'\r{prefix} |{bar}| {percent:.1f}% Complete', end='', flush=True)

def png2svg(input_path, output_path, threshold=128, scale=5, negative=True, resolution=100):
    """NOWA METODA: Konwersja piksel -> SVG prostokaty (ABSOLUTNA PRECYZJA)"""
    
    print(f"Ladowanie obrazu: {input_path}")
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Blad: Nie mozna wczytac pliku {input_path}")
        return False
    
    update_progress(1, 10, "Przetwarzanie")
    
    # Negatyw (domyslnie wlaczony)
    if negative:
        img = cv2.bitwise_not(img)
    
    update_progress(2, 10, "Przetwarzanie")
    
    # Skalowanie obrazu jesli potrzebne
    if scale != 5:
        scale_factor = scale / 5.0
        height, width = img.shape
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    update_progress(3, 10, "Przetwarzanie")
    
    # REWOLUCYJNA METODA: BEZPOSREDNIA KONWERSJA PIKSEL -> SVG
    # ZERO STRAT - ABSOLUTNA PRECYZJA BEZ DETEKCJI KONTUROW!
    height, width = img.shape
    
    # Utworz SVG
    svg_width = int(width * resolution / 100)
    svg_height = int(height * resolution / 100)
    dwg = svgwrite.Drawing(output_path, size=(svg_width, svg_height), viewBox=f"0 0 {width} {height}")
    
    print(f"\nRozdzielczosc SVG: {svg_width}x{svg_height} ({resolution}%) - PIXEL->SVG")
    update_progress(4, 10, "Analiza pikseli")
    
    # Progowanie dla wykrycia czarnych pikseli (bez filtrowania!)
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    
    update_progress(5, 10, "Budowanie SVG")
    
    # METODA PROSTOKAT-OPTYMALIZOWANA
    # Grupuj sasiednie czarne piksele w prostokaty
    visited = np.zeros_like(binary, dtype=bool)
    total_pixels = height * width
    processed = 0
    rectangles_created = 0
    
    for y in range(height):
        for x in range(width):
            if binary[y, x] == 255 and not visited[y, x]:  # Czarny piksel
                # Znajdz maksymalny prostokat poziomy
                rect_width = 0
                for test_x in range(x, width):
                    if binary[y, test_x] == 255 and not visited[y, test_x]:
                        rect_width += 1
                    else:
                        break
                
                # Sprawdz czy mozna rozszerzyc w dol
                rect_height = 1
                can_extend = True
                while y + rect_height < height and can_extend:
                    for test_x in range(x, x + rect_width):
                        if binary[y + rect_height, test_x] != 255 or visited[y + rect_height, test_x]:
                            can_extend = False
                            break
                    if can_extend:
                        rect_height += 1
                
                # Oznacz prostokat jako odwiedzony
                for py in range(y, y + rect_height):
                    for px in range(x, x + rect_width):
                        if py < height and px < width:
                            visited[py, px] = True
                
                # Dodaj prostokat do SVG (KAZDY CZARNY PIKSEL ZACHOWANY!)
                if rect_width > 0 and rect_height > 0:
                    dwg.add(dwg.rect(
                        insert=(x, y),
                        size=(rect_width, rect_height),
                        fill='black',
                        stroke='none'
                    ))
                    rectangles_created += 1
            
            processed += 1
            # Progress co 5% pikseli
            if processed % (total_pixels // 20) == 0:
                progress = 5 + (processed / total_pixels) * 4
                update_progress(int(progress), 10, f"SVG {rectangles_created} elementow")
    
    update_progress(9, 10, "Finalizacja")
    
    # Zapisz SVG
    dwg.save()
    update_progress(10, 10, "Gotowe")
    print(f"\nSVG zapisany: {output_path}")
    print(f"Utworzono {rectangles_created} elementow SVG")
    print("ABSOLUTNA PRECYZJA - kazdy czarny piksel zachowany!")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="PNG->SVG: ABSOLUTNA PRECYZJA (piksel=prostokat SVG)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
NOWA METODA - ZERO STRAT:
  png2svg obraz.png                    # ABSOLUTNA PRECYZJA
  png2svg obraz.png wynik.svg          # z nazwa
  png2svg obraz.png --resolution 500   # 5x rozdzielczosc + ZERO strat
  png2svg obraz.png --resolution 1000  # 10x rozdzielczosc + ZERO strat
        """
    )
    
    parser.add_argument("input", help="Plik wejsciowy PNG/JPG")
    parser.add_argument("output", nargs="?", help="Plik wyjsciowy SVG (opcjonalnie)")
    parser.add_argument("--scale", type=int, choices=range(1,11), default=5, 
                       metavar="[1-10]", help="Skala obrazu (1-10), domyslnie 5")
    parser.add_argument("--resolution", type=int, choices=range(100,1001,100), default=100, 
                       metavar="[100-1000]", help="Rozdzielczosc SVG w %% (100-1000), domyslnie 100%%")
    parser.add_argument("--no-negative", action="store_true", 
                       help="Wylacz negatyw (domyslnie wlaczony)")
    parser.add_argument("--threshold", type=int, choices=range(1,256), default=128,
                       metavar="[1-255]", help="Prog binaryzacji (1-255), domyslnie 128")
    
    args = parser.parse_args()
    
    # Okresl plik wyjsciowy
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.splitext(args.input)[0] + ".svg"
    
    # Konwertuj z ABSOLUTNA PRECYZJA
    negative = not args.no_negative  # Domyslnie wlaczony
    success = png2svg(args.input, output_path, threshold=args.threshold, 
                     scale=args.scale, negative=negative, resolution=args.resolution)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
