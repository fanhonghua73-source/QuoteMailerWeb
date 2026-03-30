import os
import zipfile
import shutil

pptx = r'C:\Users\DELL\Desktop\DesktopStuff\L selection-Funky retro collection -Hydration-202511.pptx'
out_dir = r'C:\Users\DELL\Desktop\FunkyRetro_Hydration_images'
os.makedirs(out_dir, exist_ok=True)

count = 0
with zipfile.ZipFile(pptx, 'r') as z:
    for name in z.namelist():
        if name.startswith('ppt/media/') and not name.endswith('/'):
            ext = os.path.splitext(name)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
                data = z.read(name)
                fname = os.path.basename(name)
                # Rename with index to avoid conflicts
                safe_fname = f'funky_{count+1}_{fname}'
                dst = os.path.join(out_dir, safe_fname)
                with open(dst, 'wb') as f:
                    f.write(data)
                count += 1
                print(f'Extracted: {safe_fname}')

print(f'\nTotal: {count} images -> {out_dir}')