import os
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'
out_path = os.path.join(src_dir, '2_canvas.png')

# Load original
img = Image.open(os.path.join(src_dir, '2.png')).convert('RGBA')
w, h = img.size

# Target: image occupies 50% of 3000x3000 = 1500x1500 max area
target_area = 1500
aspect = w / h

if w > h:
    new_w = target_area
    new_h = int(target_area / aspect)
else:
    new_h = target_area
    new_w = int(target_area * aspect)

# Resize to fit 50% area
img_resized = img.resize((new_w, new_h), Image.LANCZOS)

# Sharpen edges
img_sharp = img_resized.filter(ImageFilter.SHARPEN)
enhancer = ImageEnhance.Sharpness(img_sharp)
img_sharp = enhancer.enhance(2.5)

# Create 3000x3000 transparent canvas
canvas = Image.new('RGBA', (3000, 3000), (0, 0, 0, 0))

# Center on canvas
x = (3000 - new_w) // 2
y = (3000 - new_h) // 2
canvas.paste(img_sharp, (x, y), img_sharp)

canvas.save(out_path, 'PNG')
print(f'Done: {new_w}x{new_h} image on 3000x3000 canvas, centered, sharpened')
print(f'Saved: {out_path}')