import os, shutil

# BONBON - rename back from catbox IDs to original names
bonbon_map = {
    '98rlb8.jpeg.jpeg': 'bonbon_1_image1.jpeg',
    'oj41iv.jpeg.jpeg': 'bonbon_2_image2.jpeg',
    '5aq5js.jpeg.jpeg': 'bonbon_3_image3.jpeg',
    'ewq748.jpeg.jpeg': 'bonbon_4_image4.jpeg',
}

bonbon_dir = r'C:\Users\DELL\Desktop\BONBON_Dentelle_images'
for old, new in bonbon_map.items():
    src = os.path.join(bonbon_dir, old)
    if os.path.exists(src):
        dst = os.path.join(bonbon_dir, new)
        os.rename(src, dst)
        print(f'Renamed: {old} -> {new}')

# FUNKY - rename back
funky_map = {
    'jyk5sp.jpeg.jpeg': 'funky_1_image1.jpeg',
    'sivsfz.jpeg.jpeg': 'funky_2_image10.png',
    'waibsd.jpeg.jpeg': 'funky_3_image11.png',
    'xjrkhw.jpeg.jpeg': 'funky_4_image12.png',
    'q1nkv4.jpeg.jpeg': 'funky_11_image2.jpeg',
    'dwx9xc.jpeg.jpeg': 'funky_12_image3.jpeg',
}

funky_dir = r'C:\Users\DELL\Desktop\FunkyRetro_Hydration_images'
for old, new in funky_map.items():
    src = os.path.join(funky_dir, old)
    if os.path.exists(src):
        dst = os.path.join(funky_dir, new)
        os.rename(src, dst)
        print(f'Renamed: {old} -> {new}')

print('Done!')
print('\nBONBON files:')
for f in sorted(os.listdir(bonbon_dir)):
    print(f'  {f}')

print('\nFUNKY files:')
for f in sorted(os.listdir(funky_dir)):
    print(f'  {f}')