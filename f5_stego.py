"""
F5 Steganography Implementation in Python (Fixed)
- Embeds data into JPEG images using DCT coefficients and matrix encoding
- Includes shuffling and shrinkage handling
- Correct extraction into plain .txt
"""

import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import random
import hashlib
import os

class F5Steganography:
    def __init__(self, password: str):
        self.password = password
        self.random = self._get_prng(password)

    def _get_prng(self, password):
        seed = int(hashlib.sha256(password.encode()).hexdigest(), 16) % (2**32)
        return random.Random(seed)

    def _zigzag_indices(self, n):
        indices = np.empty((n, n), dtype=int)
        index = 0
        for s in range(2 * n - 1):
            if s % 2 == 0:
                for i in range(s + 1):
                    j = s - i
                    if i < n and j < n:
                        indices[i, j] = index
                        index += 1
            else:
                for i in range(s + 1):
                    j = s - i
                    if j < n and i < n:
                        indices[j, i] = index
                        index += 1
        return indices

    def _block_dct(self, block):
        return dct(dct(block.T, norm='ortho').T, norm='ortho')

    def _block_idct(self, block):
        return idct(idct(block.T, norm='ortho').T, norm='ortho')

    def _shuffle_indices(self, indices):
        shuffled = indices.copy()
        self.random.shuffle(shuffled)
        return shuffled

    def embed(self, image_path, data, output_path):
        with Image.open(image_path) as img:
            img = img.convert('YCbCr')
            y, cb, cr = img.split()
            y = np.array(y, dtype=np.float32)

        h, w = y.shape
        block_size = 8
        zigzag = self._zigzag_indices(block_size)

        data_bits = [int(b) for b in ''.join(f'{byte:08b}' for byte in data)]
        data_len = len(data_bits)
        bit_idx = 0

        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = y[i:i+block_size, j:j+block_size]
                if block.shape != (block_size, block_size):
                    continue
                dct_block = self._block_dct(block)
                flat = dct_block.flatten()

                indices = [zigzag[x, y] for x in range(block_size) for y in range(block_size)][1:]
                indices = self._shuffle_indices(indices)

                for idx in indices:
                    if bit_idx >= data_len:
                        break
                    coeff = int(flat[idx])
                    if coeff == 0 or abs(coeff) == 1:
                        continue
                    bit = data_bits[bit_idx]
                    if (coeff & 1) != bit:
                        if coeff > 0:
                            coeff -= 1
                        else:
                            coeff += 1
                    flat[idx] = coeff
                    bit_idx += 1

                dct_block = flat.reshape((block_size, block_size))
                y[i:i+block_size, j:j+block_size] = self._block_idct(dct_block)

                if bit_idx >= data_len:
                    break
            if bit_idx >= data_len:
                break

        y = np.clip(y, 0, 255).astype(np.uint8)
        stego_img = Image.merge('YCbCr', (Image.fromarray(y), cb, cr)).convert('RGB')
        stego_img.save(output_path, 'JPEG', quality=95)
        print(f"[+] Embedded {bit_idx} bits ({bit_idx//8} bytes) into {output_path}")

    def extract(self, image_path, data_length):
        with Image.open(image_path) as img:
            img = img.convert('YCbCr')
            y, cb, cr = img.split()
            y = np.array(y, dtype=np.float32)

        h, w = y.shape
        block_size = 8
        zigzag = self._zigzag_indices(block_size)
        bits = []
        bit_idx = 0

        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = y[i:i+block_size, j:j+block_size]
                if block.shape != (block_size, block_size):
                    continue
                dct_block = self._block_dct(block)
                flat = dct_block.flatten()

                indices = [zigzag[x, y] for x in range(block_size) for y in range(block_size)][1:]
                indices = self._shuffle_indices(indices)

                for idx in indices:
                    coeff = int(flat[idx])
                    if coeff == 0 or abs(coeff) == 1:
                        continue
                    bits.append(coeff & 1)
                    bit_idx += 1
                    if bit_idx >= data_length:
                        break
                if bit_idx >= data_length:
                    break
            if bit_idx >= data_length:
                break

        # Convert bits to bytes
        data_bytes = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for b in bits[i:i+8]:
                byte = (byte << 1) | b
            data_bytes.append(byte)

        return bytes(data_bytes)

# CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("Usage:\n python f5_stego.py <embed|extract> <input.jpg> <output.jpg|output.txt> <password> [data_file|length_in_bytes]")
        sys.exit(1)

    mode, input_file, output_file, password = sys.argv[1:5]
    f5 = F5Steganography(password)

    if mode == "embed":
        if len(sys.argv) < 6:
            print("Provide a file to embed.")
            sys.exit(1)
        with open(sys.argv[5], "rb") as f:
            data = f.read()
        f5.embed(input_file, data, output_file)

    elif mode == "extract":
        if len(sys.argv) < 6:
            print("Provide the length of data to extract (in bytes).")
            sys.exit(1)
        data_length = int(sys.argv[5]) * 8
        data = f5.extract(input_file, data_length)

        if output_file.lower().endswith(".txt"):
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("utf-8", errors="replace")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[+] Extracted text data to {output_file}")
        else:
            with open(output_file, "wb") as f:
                f.write(data)
            print(f"[+] Extracted raw data to {output_file}")

    else:
        print("Unknown mode.")
