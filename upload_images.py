import os, requests, time

folders = [
    r'C:\Users\DELL\Desktop\BONBON_Dentelle_images',
    r'C:\Users\DELL\Desktop\FunkyRetro_Hydration_images',
]

results = []

for folder in folders:
    print(f'\n=== {os.path.basename(folder)} ===')
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png','.jpg','.jpeg','.gif','.bmp','.webp'))])
    
    for fname in files:
        path = os.path.join(folder, fname)
        with open(path, 'rb') as f:
            data = f.read()
        
        url = None
        for attempt in range(3):
            try:
                # Try catbox first
                r = requests.post(
                    'https://catbox.moe/user/api.php',
                    data={'reqtype': 'fileupload'},
                    files={'fileToUpload': (fname, data, 'image/png' if fname.endswith('.png') else 'image/jpeg')},
                    timeout=45
                )
                if r.status_code == 200:
                    url = r.text.strip()
                    break
            except:
                time.sleep(2)
            
            try:
                # Fallback to tmpfiles.org
                r2 = requests.post(
                    'https://tmpfiles.org/api/v1/upload',
                    files={'file': (fname, data, 'image/png' if fname.endswith('.png') else 'image/jpeg')},
                    timeout=45
                )
                if r2.status_code == 200:
                    import json
                    resp = r2.json()
                    if resp.get('status') == 'success':
                        url = resp['data']['url'].replace('\\/', '/')
                        break
            except:
                time.sleep(2)
        
        if url:
            short_url = url.replace('https://files.catbox.moe/', 'https://tmpfiles.org/') if 'catbox' in url else url
            # Rename file with URL
            ext = os.path.splitext(fname)[1]
            if 'catbox' in url:
                new_name = url.replace('https://files.catbox.moe/', '') + ext
            else:
                new_name = url.split('/')[-1] + ext
            new_path = os.path.join(folder, new_name)
            try:
                os.rename(path, new_path)
            except:
                pass
            print(f'{fname} -> {url}')
            results.append((fname, url))
        else:
            print(f'{fname}: FAILED all attempts')
        
        time.sleep(0.5)

print(f'\n=== DONE: {len(results)} uploaded ===')
for fname, url in results:
    print(url)