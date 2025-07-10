import sys
from PIL import Image
import numpy as np
import os

def detect_lsb(image_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        arr = np.array(img)
        flat = arr.flatten()
        # Check the first 32 bits for a probable data length
        len_bits = flat[:32] & 1
        data_len = int(''.join(str(b) for b in len_bits), 2)
        if 0 < data_len < len(flat) - 32:
            # Check if the next data_len bits are not all zero or all one
            data_bits = flat[32:32+min(data_len, 1000)] & 1
            if np.any(data_bits != data_bits[0]):
                return True
    except Exception:
        pass
    return False

def detect_f5(image_path):
    # F5 is for JPEGs and works in DCT domain, not pixels.
    # Here, we just check if the file is JPEG and has suspicious markers.
    if not image_path.lower().endswith('.jpg') and not image_path.lower().endswith('.jpeg'):
        return False
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        # F5 often leaves "F5" or "stego" markers, but not always.
        if b'F5' in data or b'stego' in data:
            return True
    except Exception:
        pass
    return False

def analyze(image_path):
    if detect_lsb(image_path):
        print(f"{image_path}: LSB steganography detected.")
    elif detect_f5(image_path):
        print(f"{image_path}: F5 steganography (JPEG) detected.")
    else:
        print(f"{image_path}: No known steganography detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <image_file>")
        sys.exit(1)
    analyze(sys.argv[1])
