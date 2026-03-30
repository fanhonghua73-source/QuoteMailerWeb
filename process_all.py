import os
from PIL import Image
import numpy as np

# Process ALL cached logos to output
cache_dir = r'F:\QuoteMailerWeb\.logo_cache'
output_dir = r'F:\QuoteMailerWeb\assets\processed'
os.makedirs(output_dir, exist_ok=True)

files = sorted(os.listdir(cache_dir))
print(f"Total: {len(files)} files")

# Process each file and save as logo_1, logo_2, etc. in directory order
for i, f in enumerate(sorted(files)):
    src = os.path.join(cache_dir, f)
    dst = os.path.join(output_dir, f'logo_{i+1}.png')
    img = Image.open(src).convert('RGBA')
    data = np.array(img)
    threshold = 240
    r_ch, g_ch, b_ch, a_ch = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    white_mask = (r_ch >= threshold) & (g_ch >= threshold) & (b_ch >= threshold)
    data[:,:,3] = np.where(white_mask, 0, 255)
    img = Image.fromarray(data, 'RGBA')
    img.save(dst, 'PNG')
    orig = Image.open(src)
    print(f'{i+1}. {f} -> logo_{i+1}.png size={orig.size}')

print('\nProcessed files:')
for f in sorted(os.listdir(output_dir)):
    print(f'  {f}')