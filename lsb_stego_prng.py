"""
LSB (Least Significant Bit) Steganography with Pseudo-Random Embedding
- Embeds and extracts data in the least significant bits of image pixels
- Uses a key to shuffle embedding order for increased security
- Works with PNG and BMP (lossless) images
"""
from PIL import Image
import numpy as np
import sys
import os

class LSBStegoPRNG:
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
    def embed(input_image, data, output_image, key):
        img = Image.open(input_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        arr = np.array(img)
        flat = arr.flatten()
        data_bits = LSBStegoPRNG._to_bits(data)
        data_len = len(data_bits)
        len_bits = [int(b) for b in f'{data_len:032b}']
        bits = len_bits + data_bits
        if len(bits) > len(flat):
            raise ValueError('Data too large to embed in image.')
        # Pseudo-random embedding order
        indices = list(range(len(flat)))
        import random, hashlib
        seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        rng.shuffle(indices)
        for i, bit in enumerate(bits):
            idx = indices[i]
            flat[idx] = (flat[idx] & 0xFE) | bit
        arr = flat.reshape(arr.shape)
        out_img = Image.fromarray(arr)
        out_img.save(output_image)
        print(f"Embedded {data_len} bits into {output_image}")

    @staticmethod
    def extract(stego_image, key):
        img = Image.open(stego_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        arr = np.array(img)
        flat = arr.flatten()
        indices = list(range(len(flat)))
        import random, hashlib
        seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        rng.shuffle(indices)
        len_bits = []
        for i in range(32):
            idx = indices[i]
            len_bits.append(flat[idx] & 1)
        data_len = int(''.join(str(b) for b in len_bits), 2)
        data_bits = []
        for i in range(32, 32+data_len):
            idx = indices[i]
            data_bits.append(flat[idx] & 1)
        data = LSBStegoPRNG._from_bits(data_bits)
        return data

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python lsb_stego_prng.py <embed|extract> <input_image> <output_image|output_file> <data_file|key> <key>")
        print("  For embed: python lsb_stego_prng.py embed input.png output.png secret.pdf mySecretKey")
        print("  For extract: python lsb_stego_prng.py extract output.png extracted.pdf mySecretKey")
        sys.exit(1)
    mode = sys.argv[1]
    output_dir = "PRNG_Outputs"
    os.makedirs(output_dir, exist_ok=True)
    if mode == "embed":
        input_image = sys.argv[2]
        output_image = sys.argv[3]
        if not output_image.startswith(output_dir + os.sep):
            output_image = os.path.join(output_dir, os.path.basename(output_image))
        file_to_embed = sys.argv[4]
        key = sys.argv[5]
        with open(file_to_embed, "rb") as f:
            data = f.read()
        if file_to_embed.lower().endswith('.pdf'):
            print(f"Embedding PDF file '{file_to_embed}' into image '{output_image}'...")
        else:
            print(f"Embedding file '{file_to_embed}' into image '{output_image}'...")
        LSBStegoPRNG.embed(input_image, data, output_image, key)
        if file_to_embed.lower().endswith('.pdf'):
            print("To extract the PDF, use: python lsb_stego_prng.py extract <stego_image> <output.pdf> <key>")
    elif mode == "extract":
        input_image = sys.argv[2]
        output_file = sys.argv[3]
        key = sys.argv[4]
        if not output_file.startswith(output_dir + os.sep):
            output_file = os.path.join(output_dir, os.path.basename(output_file))
        data = LSBStegoPRNG.extract(input_image, key)
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
        if output_file.lower().endswith('.pdf'):
            print("You can now open the extracted PDF file.")
    else:
        print("Unknown mode.")
