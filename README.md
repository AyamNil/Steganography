# Steganography Toolkit

This project provides Python tools for embedding, extracting, and analyzing steganography in images.

## Setup

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```powershell
   pip install pillow numpy
   ```

---

## Tools

### 1. LSB Steganography (`lsb_stego.py`)

**Embed data into an image:**
```powershell
python lsb_stego.py embed <input_image> <output_image> <data_file>
```
- `<input_image>`: Path to the source PNG or BMP image.
- `<output_image>`: Path to save the stego image.
- `<data_file>`: File to embed (text or binary).

**Extract data from an image:**
```powershell
python lsb_stego.py extract <stego_image> <output_file>
```
- `<stego_image>`: Image suspected to contain hidden data.
- `<output_file>`: File to save the extracted data. If it ends with `.txt`, the data will be saved as text.

---

### 2. Steganography Analyzer (`analyzer.py`)

Detects if an image uses LSB or F5 steganography.

**Usage:**
```powershell
python analyzer.py <image_file>
```
- `<image_file>`: Image to analyze (PNG, BMP, or JPEG).

The script will print the detected steganography type or report if none is found.

---

## Notes
- Only lossless images (PNG, BMP) are supported for LSB embedding/extraction.
- F5 detection is basic and only works for JPEGs with certain markers.
- For best results, use images with no prior compression for LSB steganography.

---

## Example

**Embed text:**
```powershell
python lsb_stego.py embed TEST.png output.png secret.txt
```

**Extract text:**
```powershell
python lsb_stego.py extract output.png extracted.txt
```

**Analyze an image:**
```powershell
python analyzer.py output.png
```
