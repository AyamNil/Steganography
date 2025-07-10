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


**Embed data (including PDF) into an image:**
```sh
python lsb_stego.py embed <input_image> <output_image> <data_file>
```
- `<input_image>`: Path to the source PNG or BMP image.
- `<output_image>`: Name for the stego image (will be saved in `LSB_Outputs/`).
- `<data_file>`: File to embed (text, PDF, or any binary file).

**Extract data (including PDF) from an image:**
```sh
python lsb_stego.py extract <stego_image> <output_file>
```
- `<stego_image>`: Image suspected to contain hidden data.
- `<output_file>`: Name for the extracted file (will be saved in `LSB_Outputs/`).
   - If it ends with `.txt`, the data will be saved as text.
   - If it ends with `.pdf`, the data will be saved as a PDF (open with any PDF reader).

**All output files are saved in the `LSB_Outputs/` directory automatically.**

---

### 1b. LSB Steganography with Pseudo-Random Embedding (`lsb_stego_prng.py`)

This version increases security by embedding bits in a pseudo-random order determined by a user-provided key. You must use the same key for extraction.

**Embed data (including PDF) into an image with a key:**
```sh
python lsb_stego_prng.py embed <input_image> <output_image> <data_file> <key>
```
- `<input_image>`: Path to the source PNG or BMP image.
- `<output_image>`: Name for the stego image (will be saved in `LSB_Outputs/`).
- `<data_file>`: File to embed (text, PDF, or any binary file).
- `<key>`: Secret key for shuffling the embedding order.

**Extract data (including PDF) from an image with a key:**
```sh
python lsb_stego_prng.py extract <stego_image> <output_file> <key>
```
- `<stego_image>`: Image suspected to contain hidden data.
- `<output_file>`: Name for the extracted file (will be saved in `LSB_Outputs/`).
- `<key>`: The same key used for embedding.

**All output files are saved in the `LSB_Outputs/` directory automatically.**

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


**Embed a PDF:**
```sh
python lsb_stego.py embed TEST.png secret.png document.pdf
```

**Extract a PDF:**
```sh
python lsb_stego.py extract secret.png extracted.pdf
```

**Embed text:**
```sh
python lsb_stego.py embed TEST.png output.png secret.txt
```

**Extract text:**
```sh
python lsb_stego.py extract output.png extracted.txt
```

**Analyze an image:**
```powershell
python analyzer.py output.png
```

---

## Example (Pseudo-Random LSB)

**Embed a PDF with a key:**
```sh
python lsb_stego_prng.py embed TEST.png secret.png document.pdf mySecretKey
```

**Extract a PDF with a key:**
```sh
python lsb_stego_prng.py extract secret.png extracted.pdf mySecretKey
```
