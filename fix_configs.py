import json, os

for d in os.listdir(r'F:\QuoteMailerWeb\projects'):
    cfg_path = os.path.join(r'F:\QuoteMailerWeb\projects', d, 'config.json')
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            cfg = json.load(f)
        cfg.setdefault('template_name', 'tpl_nordic.html')
        cfg.setdefault('gallery_style', 'strip')
        cfg.setdefault('gallery_overrides', {})
        cfg.setdefault('extra_modules', [])
        with open(cfg_path, 'w') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        print(f'{d}: template={cfg["template_name"]}, style={cfg["gallery_style"]}')