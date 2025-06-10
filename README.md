# PNG to SVG Converter

🎯 **ABSOLUTNA PRECYZJA** - Konwersja PNG/JPG do SVG z rewolucyjną metodą piksel→prostokąt SVG

## 🚀 Nowy Algorytm

Zamiast tradycyjnej detekcji konturów (która traci szczegóły), używamy bezpośredniej konwersji:
- **Każdy czarny piksel** = **osobny prostokąt SVG**
- **ZERO STRAT** w szczegółach
- **Matematyczna precyzja** 1:1 z oryginalnym PNG

## ⚡ Funkcje

- ✅ **Domyślnie negatyw włączony** (--no-negative aby wyłączyć)
- ✅ **Rozdzielczość 100-1000%** (--resolution 500 = 5x większa)
- ✅ **Skala 1-10** (--scale 8 dla większej skali)
- ✅ **Próg binaryzacji** (--threshold 100-200)
- ✅ **Automatyczna nazwa** .svg jeśli nie podano
- ✅ **ViewBox** - poprawne skalowanie w przeglądarkach

## 📖 Użycie

```bash
# Podstawowa konwersja
png2svg logo.png

# Z większą rozdzielczością (5x ostrzej)
png2svg logo.png --resolution 500

# Z maksymalną rozdzielczością (10x ostrzej)
png2svg logo.png --resolution 1000

# Niższy próg dla cieńszych linii
png2svg logo.png --threshold 100

# Własna nazwa pliku
png2svg logo.png moje-logo.svg
```

## 🔧 Instalacja

1. Pobierz `png2svg.exe` z [Releases](https://github.com/ussdeveloper/png2svg/releases)
2. Umieść w folderze z obrazami
3. Uruchom z linii poleceń

Lub uruchom ze źródeł:

```bash
pip install opencv-python svgwrite numpy
python png2svg.py obraz.png
```

## 🎯 Algorytm

**REWOLUCYJNA METODA:**
1. Skanuje każdy piksel obrazu
2. Czarny piksel → prostokąt 1x1 w SVG
3. Optymalizacja: łączy sąsiednie piksele w większe prostokąty
4. **REZULTAT:** Identyczna kopia PNG w formacie SVG

**Różnice vs tradycyjne metody:**
- ❌ Stare: Detekcja konturów → aproksymacja → utrata szczegółów
- ✅ Nowe: Piksel → prostokąt → zachowanie 100% szczegółów

## 📊 Przykład

**Input:** `logo.png` (300x300px)  
**Output:** `logo.svg` z 2847 prostokątami SVG  
**Rezultat:** Matematycznie identyczny obraz

## 🎨 Rozwój

```bash
git clone https://github.com/ussdeveloper/png2svg.git
cd png2svg
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 📄 Licencja

MIT License - używaj jak chcesz! 🚀
