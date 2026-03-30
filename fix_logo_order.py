import os
from PIL import Image
import numpy as np

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'

# 1. Create 3000x3000 transparent canvas for 2.png
canvas = Image.new('RGBA', (3000, 3000), (0, 0, 0, 0))
img_2 = Image.open(os.path.join(src_dir, '2.png')).convert('RGBA')

# Center the image on canvas
w, h = img_2.size
x = (3000 - w) // 2
y = (3000 - h) // 2
canvas.paste(img_2, (x, y), img_2)

canvas.save(os.path.join(src_dir, '2_canvas.png'), 'PNG')
print(f'2.png on 3000x3000 canvas saved')

# 2. Read all files in correct order
# Order: 一.png=main, 1.png, 2_canvas.png, 3.png, 4.png, 5.png
files_ordered = [
    ('main', '一.png'),
    ('sub1', '1.png'),
    ('sub2', '2_canvas.png'),
    ('sub3', '3.png'),
    ('sub4', '4.png'),
    ('sub5', '5.png'),
]

import requests
urls = {}

for name, fname in files_ordered:
    path = os.path.join(src_dir, fname)
    with open(path, 'rb') as f:
        data = f.read()
    
    try:
        r = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': (fname, data, 'image/png')},
            timeout=30
        )
        if r.status_code == 200:
            url = r.text.strip()
            urls[name] = url
            print(f'{name} ({fname}): {url}')
        else:
            print(f'{name}: FAIL {r.status_code}')
    except Exception as e:
        print(f'{name}: ERR {e}')

print('\n=== FINAL URLs ===')
for k, v in urls.items():
    print(f'{k}: {v}')