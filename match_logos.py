import os
import hashlib
import requests

# Logo URLs in correct order
logos_ordered = [
    ('main', 'https://files.catbox.moe/60x3q1.png'),
    ('sub1', 'https://files.catbox.moe/lrowca.png'),
    ('sub2', 'https://files.catbox.moe/zzybjq.png'),
    ('sub3', 'https://files.catbox.moe/4ma01c.png'),
    ('sub4', 'https://files.catbox.moe/sttfse.png'),
    ('sub5', 'https://files.catbox.moe/0r05x4.png'),
]

cache_dir = r'F:\QuoteMailerWeb\.logo_cache'
output_dir = r'F:\QuoteMailerWeb\assets\processed'
os.makedirs(output_dir, exist_ok=True)

# Build hash map from cache files
hash_map = {}
for f in os.listdir(cache_dir):
    if f.endswith('.png'):
        path = os.path.join(cache_dir, f)
        with open(path, 'rb') as fp:
            h = hashlib.md5(fp.read()).hexdigest()
        hash_map[h] = path

print(f"Found {len(hash_map)} cached logos")

# Try to match by re-downloading and hashing
for name, url in logos_ordered:
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            h = hashlib.md5(r.content).hexdigest()
            if h in hash_map:
                print(f"MATCH {name} -> {hash_map[h]}")
            else:
                print(f"NO MATCH {name} ({h})")
                # Save anyway
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(r.content)).convert('RGBA')
                import numpy as np
                data = np.array(img)
                threshold = 240
                r_ch, g_ch, b_ch, a_ch = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
                white_mask = (r_ch >= threshold) & (g_ch >= threshold) & (b_ch >= threshold)
                data[:,:,3] = np.where(white_mask, 0, 255)
                img = Image.fromarray(data, 'RGBA')
                out = os.path.join(output_dir, f'{name}.png')
                img.save(out, 'PNG')
                print(f"  Saved {out}")
        else:
            print(f"FAIL {name} status={r.status_code}")
    except Exception as e:
        print(f"ERROR {name}: {e}")