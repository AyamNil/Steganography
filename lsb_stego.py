"""
LSB (Least Significant Bit) Steganography Implementation in Python
- Embeds and extracts data in the least significant bits of image pixels
- Works with PNG and BMP (lossless) images
"""
from PIL import Image
import numpy as np
import sys

class LSBSteganography:
    @staticmethod
    def _to_bits(data):
        return [int(bit) for byte in data for bit in f'{byte:08b}']

    @staticmethod
    def _from_bits(bits):
        bytes_out = bytearray()
        for b in range(0, len(bits), 8):
            byte = 0
            for bit in bits[b:b+8]:
                byte = (byte << 1) | bit
            bytes_out.append(byte)
        return bytes(bytes_out)

    @staticmethod
    def embed(input_image, data, output_image):
        img = Image.open(input_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        arr = np.array(img)
        flat = arr.flatten()
        data_bits = LSBSteganography._to_bits(data)
        data_len = len(data_bits)
        # Store data length in first 32 bits
        len_bits = [int(b) for b in f'{data_len:032b}']
        bits = len_bits + data_bits
        if len(bits) > len(flat):
            raise ValueError('Data too large to embed in image.')
        for i, bit in enumerate(bits):
            flat[i] = (flat[i] & 0xFE) | bit
        arr = flat.reshape(arr.shape)
        out_img = Image.fromarray(arr)
        out_img.save(output_image)
        print(f"Embedded {data_len} bits into {output_image}")

    @staticmethod
    def extract(stego_image):
        img = Image.open(stego_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        arr = np.array(img)
        flat = arr.flatten()
        # Read data length from first 32 bits
        len_bits = flat[:32] & 1
        data_len = int(''.join(str(b) for b in len_bits), 2)
        data_bits = flat[32:32+data_len] & 1
        data = LSBSteganography._from_bits(data_bits)
        return data

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python lsb_stego.py <embed|extract> <input_image> <output_image|output_file> [data_file]")
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "embed":
        if len(sys.argv) < 5:
            print("Provide a file to embed.")
            sys.exit(1)
        input_image = sys.argv[2]
        output_image = sys.argv[3]
        with open(sys.argv[4], "rb") as f:
            data = f.read()
        LSBSteganography.embed(input_image, data, output_image)
    elif mode == "extract":
        input_image = sys.argv[2]
        output_file = sys.argv[3]
        data = LSBSteganography.extract(input_image)
        # If output file ends with .txt, decode as text
        if output_file.lower().endswith('.txt'):
            try:
                text = data.decode('utf-8')
            except UnicodeDecodeError:
                text = data.decode('utf-8', errors='replace')
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Extracted text data to {output_file}")
        else:
            with open(output_file, "wb") as f:
                f.write(data)
            print(f"Extracted data to {output_file}")
    else:
        print("Unknown mode.")