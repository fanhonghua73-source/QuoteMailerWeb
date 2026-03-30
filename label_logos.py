#!/usr/bin/env python3
import os, base64, requests

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'
files = sorted([f for f in os.listdir(src_dir) if f.endswith('.png')])

results = {}

for fname in files:
    img_path = os.path.join(src_dir, fname)
    
    try:
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        b64 = base64.b64encode(img_bytes).decode()
        
        # Try with deepseek-r1 - might handle base64 vision
        payload = {
            'model': 'deepseek-r1:8b',
            'prompt': f'<image data:image/png;base64:{b64}</image>\nWhat brand name is shown in this logo? Reply with only the brand name. Think silently then give answer.',
            'stream': False
        }
        
        r = requests.post('http://localhost:11434/api/generate', json=payload, timeout=120)
        if r.status_code == 200:
            d = r.json()
            content = d.get('response', '').strip()
            # Clean think tags
            import re
            content = re.sub(r'<[^>]+think[^>]*>.*?</[^>]+think>', '', content, flags=re.DOTALL)
            results[fname] = content.strip()
            print(f'{fname}: {content.strip()}')
        else:
            print(f'{fname}: FAIL {r.status_code} {r.text[:200]}')
            results[fname] = None
    except Exception as e:
        results[fname] = None
        print(f'{fname}: ERR {e}')

print('\n=== RESULTS ===')
for k, v in results.items():
    print(f'{k}: {v}')

# Rename
print('\n=== RENAMING ===')
for fname, name in results.items():
    if name and name != 'None':
        safe_name = ''.join(c for c in name if c.isalnum() or c in ' -_').strip()[:30]
        if not safe_name:
            continue
        src = os.path.join(src_dir, fname)
        dst = os.path.join(src_dir, f'{safe_name}.png')
        i = 1
        while os.path.exists(dst) and dst != src:
            dst = os.path.join(src_dir, f'{safe_name}_{i}.png')
            i += 1
        if src != dst:
            os.rename(src, dst)
            print(f'{fname} -> {os.path.basename(dst)}')