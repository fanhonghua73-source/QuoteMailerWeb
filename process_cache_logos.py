import os
from PIL import Image
import numpy as np

# Process logos from cache directory
cache_dir = r'F:\QuoteMailerWeb\.logo_cache'
output_dir = r'F:\QuoteMailerWeb\assets\processed'
os.makedirs(output_dir, exist_ok=True)

def make_white_transparent(img_path):
    """Convert near-white pixels to transparent"""
    img = Image.open(img_path).convert('RGBA')
    data = np.array(img)
    
    # White threshold
    threshold = 240
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    white_mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    data[:,:,3] = np.where(white_mask, 0, 255)
    
    return Image.fromarray(data, 'RGBA')

for fname in os.listdir(cache_dir):
    if fname.endswith('.png'):
        src = os.path.join(cache_dir, fname)
        dst = os.path.join(output_dir, fname)
        processed = make_white_transparent(src)
        processed.save(dst)
        print(f'Processed: {fname}')

print('Done!')