# Perform LSB steganography detection plausibility test on the uploaded images
# to check if any hidden data is embedded in their least significant bits

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import entropy

def lsb_extract_bits(image_path: str, channel: int = 0) -> np.ndarray:
    """Extracts the LSB plane from the selected channel (0=R, 1=G, 2=B) from an image file path."""
    image = Image.open(image_path)
    arr = np.array(image)
    lsb_plane = arr[:,:,channel] & 1
    return lsb_plane

# Extract LSB planes for red channel (as most LSB stego hides here)
lsb_img1 = lsb_extract_bits("hammersonic.png", channel=0)
lsb_img2 = lsb_extract_bits("PRNG_Outputs/secret.png", channel=0)

# Visualize LSB planes to detect hidden structures/patterns
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.title("LSB Plane - Image 1 (R)")
plt.imshow(lsb_img1, cmap='gray')
plt.axis("off")

plt.subplot(1,2,2)
plt.title("LSB Plane - Image 2 (R)")
plt.imshow(lsb_img2, cmap='gray')
plt.axis("off")

plt.tight_layout()
plt.show()

def lsb_entropy(lsb_plane):
    counts = np.bincount(lsb_plane.flatten(), minlength=2)
    return entropy(counts, base=2)

entropy_img1 = lsb_entropy(lsb_img1)
entropy_img2 = lsb_entropy(lsb_img2)

print(f"Entropy Image 1: {entropy_img1:.4f}")
print(f"Entropy Image 2: {entropy_img2:.4f}")
# Compare the entropy values to see if one image has significantly lower entropy
if entropy_img1 < entropy_img2:
    print("Image 1 likely has hidden data (lower entropy).")
elif entropy_img1 > entropy_img2:
    print("Image 2 likely has hidden data (lower entropy).")
else:
    print("Both images have similar entropy values, no clear hidden data detected.")
# This code extracts the least significant bit (LSB) planes from two images,
# visualizes them, and calculates their entropy to detect potential hidden data.
# Lower entropy in an LSB plane may indicate the presence of hidden data.
# The code uses numpy for array manipulation, PIL for image processing, and matplotlib for visualization.
# It also uses scipy's entropy function to compute the entropy of the LSB planes.