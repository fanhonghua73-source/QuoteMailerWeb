import os
import requests

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'
out_urls = {}

for fname in sorted(os.listdir(src_dir)):
    if fname.lower().endswith('.png'):
        path = os.path.join(src_dir, fname)
        with open(path, 'rb') as f:
            file_data = f.read()
        
        try:
            r = requests.post(
                'https://catbox.moe/user/api.php',
                data={'reqtype': 'fileupload'},
                files={'fileToUpload': (fname, file_data, 'image/png')},
                timeout=30
            )
            if r.status_code == 200:
                url = r.text.strip()
                out_urls[fname] = url
                print(f'{fname}: {url}')
            else:
                print(f'{fname}: FAIL status={r.status_code} resp={r.text[:100]}')
        except Exception as e:
            print(f'{fname}: ERR {e}')

print('\n--- URLs ---')
for k, v in out_urls.items():
    print(f'{k}: {v}')