#!/usr/bin/env python3
"""Use ollama package to label logos"""
import os
import subprocess

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'
out_dir = r'C:\Users\DELL\Desktop\linkgroup_logo'

files = sorted([f for f in os.listdir(src_dir) if f.endswith('.png')])

results = {}

for fname in files:
    img_path = os.path.join(src_dir, fname)
    
    cmd = ['ollama', 'run', 'qwen3-vl:8b', 
           f'/path/to/{fname}\nWhat brand name is shown in this logo? Just the brand name.']
    
    try:
        # Copy image to a temp path accessible by ollama
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, 
                               cwd=src_dir)
        print(f'{fname}: stdout={result.stdout[:100]}, stderr={result.stderr[:100]}')
    except Exception as e:
        print(f'{fname}: ERR {e}')

print('Done')