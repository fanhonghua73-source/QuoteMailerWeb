import os
import requests
from PIL import Image
import io
import numpy as np

# Logo URLs from BRAND_ASSETS
logos = {
    'main': 'https://files.catbox.moe/60x3q1.png',
    'sub1': 'https://files.catbox.moe/lrowca.png',
    'sub2': 'https://files.catbox.moe/zzybjq.png',
    'sub3': 'https://files.catbox.moe/4ma01c.png',
    'sub4': 'https://files.catbox.moe/sttfse.png',
    'sub5': 'https://files.catbox.moe/0r05x4.png',
}

output_dir = r'F:\QuoteMailerWeb\assets\processed'
os.makedirs(output_dir, exist_ok=True)

def make_white_transparent(img):
    """Convert near-white pixels to transparent"""
    img = img.convert('RGBA')
    data = np.array(img)
    
    # White threshold (tune this value)
    threshold = 240
    
    # Create mask for white-ish pixels
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    white_mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    
    # Set alpha to 0 for white pixels
    data[:,:,3] = np.where(white_mask, 0, 255)
    
    return Image.fromarray(data, 'RGBA')

def process_image(url, name):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f'FAILED: {name} - status {r.status_code}')
            return None
        
        img = Image.open(io.BytesIO(r.content))
        processed = make_white_transparent(img)
        
        out_path = os.path.join(output_dir, f'{name}.png')
        processed.save(out_path)
        print(f'OK: {name} -> {out_path}')
        return out_path
    except Exception as e:
        print(f'ERROR: {name} - {e}')
        return None

for key, url in logos.items():
    result = process_image(url, key)
    if result:
        print(f'Local: {result}')