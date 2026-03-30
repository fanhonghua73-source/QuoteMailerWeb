import os, requests

src_dir = r'C:\Users\DELL\Desktop\linkgroup_logo\processed'
files = sorted([f for f in os.listdir(src_dir) if f.endswith('.png')])

main = None
subs = []
urls = {}

for i, fname in enumerate(files):
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
            urls[fname] = url
            if i == 0:
                main = url
            else:
                subs.append(url)
            print(f'{fname} -> {url}')
        else:
            print(f'{fname}: FAIL {r.status_code}')
    except Exception as e:
        print(f'{fname}: ERR {e}')

print('\n=== RESULT ===')
print(f'MAIN: {main}')
print(f'SUBS: {subs}')

# Save to file for reference
with open(r'F:\QuoteMailerWeb\logo_urls.txt', 'w') as f:
    f.write(f'MAIN: {main}\n')
    for i, u in enumerate(subs):
        f.write(f'SUB{i+1}: {u}\n')

print('\nSaved to logo_urls.txt')