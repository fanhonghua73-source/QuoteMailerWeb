"""
QuoteMailerWeb Template Gallery Generator
"""

import os
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR.mkdir(exist_ok=True)

# 6 套配色
THEMES = {
    '01': {'name': 'Nordic Navy', 'bg': '#FFFFFF', 'primary': '#1E3A5F', 'accent': '#D4AF37', 'text': '#333', 'text_light': '#666', 'border': '#E5E5E5', 'button': '#1E3A5F', 'button_text': '#FFF'},
    '02': {'name': 'Executive Orange', 'bg': '#FAFAFA', 'primary': '#E65100', 'accent': '#1A1A1A', 'text': '#2D2D2D', 'text_light': '#666', 'border': '#E0E0E0', 'button': '#E65100', 'button_text': '#FFF'},
    '03': {'name': 'Premium Gray', 'bg': '#F5F5F5', 'primary': '#424242', 'accent': '#8D6E63', 'text': '#212121', 'text_light': '#757575', 'border': '#BDBDBD', 'button': '#424242', 'button_text': '#FFF'},
    '04': {'name': 'Morandi Green', 'bg': '#F9FAFB', 'primary': '#5D7B6F', 'accent': '#A8B5A0', 'text': '#37474F', 'text_light': '#78909C', 'border': '#CFD8DC', 'button': '#5D7B6F', 'button_text': '#FFF'},
    '05': {'name': 'Obsidian Bold', 'bg': '#FFFFFF', 'primary': '#1A1A1A', 'accent': '#FF5722', 'text': '#212121', 'text_light': '#757575', 'border': '#EEEEEE', 'button': '#1A1A1A', 'button_text': '#FFF'},
    '06': {'name': 'Champagne Gold', 'bg': '#FFFEF9', 'primary': '#9E9E9E', 'accent': '#C9A227', 'text': '#424242', 'text_light': '#757575', 'border': '#E8E8E8', 'button': '#C9A227', 'button_text': '#FFF'},
}

LAYOUTS = [
    ('nordic', 'Nordic Minimal'),
    ('zigzag', 'Zig-Zag Gallery'),
    ('card', 'Modern Card'),
    ('grid', 'Executive Grid'),
    ('bold', 'Bold Hero'),
]

def make_template(t, layout):
    """生成模板"""
    if layout == 'nordic':
        return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Quote</title><style>*{{margin:0;padding:0}}body{{font-family:Helvetica,Arial;background:{t['bg']};color:{t['text']}}}.c{{max-width:640px;margin:0 auto;background:{t['bg']}}.h{{padding:60px 40px 40px;text-align:center}}.h1{{font-size:12px;letter-spacing:6px;text-transform:uppercase;color:{t['text_light']}}.d{{width:60px;height:1px;background:{t['border']};margin:24px auto}}.he img{{width:100%;height:auto;display:block}}.g{{padding:40px 40px 20px}}.g p{{font-size:15px;white-space:pre-wrap}}.i{{padding:0 40px 40px;text-align:center}}.i p{{font-size:14px;color:{t['text_light']}}.p{{padding:0 40px 60px}}.pi{{margin-bottom:48px}}.pr{{display:flex;gap:24px}}.pi2{{flex:0 0 200px}}.pi2 img{{width:100%;height:auto}}.pi1{{flex:1;padding-top:8px}}.ino{{font-size:11px;color:{t['text_light']};letter-spacing:1px;margin-bottom:4px}}.nm{{font-size:16px;font-weight:600;color:{t['primary']};margin-bottom:8px}}.sp{{font-size:13px;color:{t['text_light']};margin-bottom:12px}}.pd{{font-size:12px;color:{t['text_light']}}.pd span{{display:block}}.prc{{font-size:20px;font-weight:600;color:{t['accent']};margin-top:12px}}.f{{padding:48px 40px;text-align:center;border-top:1px solid {t['border']}}.fl{{margin-bottom:24px}}.fl img{{display:inline-block;margin:0 12px;vertical-align:middle}}.fb{{margin-bottom:20px}}.fb a{{display:inline-block;padding:10px 24px;background:{t['button']};color:{t['button_text']};text-decoration:none;font-size:12px;margin:0 6px;border-radius:4px}}.fc{{font-size:10px;color:{t['text_light']}}</style></head><body><div class="c"><div class="h"><h1>{{{{ title }}}}</h1><div class="d"></div></div>{{{{ if hero_image }}}}<div class="he">{{{{ if video_url }}}}<a href="{{{{ video_url }}}}"><img src="{{{{ hero_image }}}}"></a>{{{{ else }}}}<img src="{{{{ hero_image }}}}">{{{{ endif }}}}</div>{{{{ endif }}}}{{{{ if custom_greeting }}}}<div class="g"><p>{{{{ custom_greeting }}}}</p></div>{{{{ endif }}}}{{{{ if intro_text }}}}<div class="i"><p>{{{{ intro_text }}}}</p></div>{{{{ endif }}}}<div class="p">{{{{ for product in products }}}}<div class="pi"><div class="pr">{{{{ if product.images and product.images|length > 0 }}}}<div class="pi2"><img src="{{{{ product.images[0] }}}}"></div>{{{{ endif }}}}<div class="pi1">{{{{ if product.item }}}}<div class="ino">{{{{ product.item }}}}</div>{{{{ endif }}}}<div class="nm">{{{{ product.name or 'Product Name' }}}}</div>{{{{ if product.spec }}}}<div class="sp">{{{{ product.spec }}}}</div>{{{{ endif }}}}<div class="pd">{{{{ if product.material }}}}<span>Material: {{{{ product.material }}}}</span>{{{{ endif }}}}{{{{ if product.size }}}}<span>Size: {{{{ product.size }}}}</span>{{{{ endif }}}}{{{{ if product.cbm }}}}<span>CBM: {{{{ product.cbm }}}}</span>{{{{ endif }}}}{{{{ if product.moq }}}}<span>MOQ: {{{{ product.moq }}}}</span>{{{{ endif }}}}</div>{{{{ if product.price }}}}<div class="prc">${{{{ product.price }}}}</div>{{{{ endif }}}}</div></div></div>{{{{ endfor }}}}</div><div class="f"><div class="fl">{{{{ if main_logo }}}}<a href="{{{{ link_website }}}}"><img src="{{{{ main_logo }}}}" width="150"></a>{{{{ endif }}}}</div><div class="fb">{{{{ if link_contact }}}}<a href="{{{{ link_contact }}}}">CONTACT</a>{{{{ endif }}}}{{{ if link_website }}}}<a href="{{{{ link_website }}}}">WEBSITE</a>{{{{ endif }}}}</div><div class="fc">{{{{ copyright_text }}}}</div></div></div></body></html>'''
    
    # 其他布局简化版
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{{{{ title }}}}</title><style>*{{margin:0;padding:0}}body{{font-family:Arial;background:{t['bg']};color:{t['text']}}.c{{max-width:680px;margin:0 auto}}.h{{background:linear-gradient(135deg,{t['primary']} 0%,{t['primary']} 100%);padding:48px;text-align:center}}.h h1{{color:#fff;font-size:14px;letter-spacing:4px;text-transform:uppercase}}.he img{{width:100%;height:auto;display:block}}.g{{padding:40px}}.g p{{font-size:15px;line-height:1.8;white-space:pre-wrap}}.p{{padding:40px}}.pi{{margin-bottom:40px}}.pr{{display:flex;gap:32px}}.pi2{{flex:0 0 240px}}.pi2 img{{width:100%;border-radius:8px}}.pi1{{flex:1}}.ino{{font-size:11px;color:{t['accent']};letter-spacing:2px;text-transform:uppercase;margin-bottom:8px}}.nm{{font-size:18px;font-weight:700;color:{t['primary']};margin-bottom:8px}}.sp{{font-size:13px;color:{t['text_light'];margin-bottom:16px}}.pm{{display:flex;gap:12px;margin-bottom:16px}}.pm span{{font-size:12px;padding:4px 10px;background:{t['bg']};border-radius:4px}}.prc{{font-size:24px;font-weight:700;color:{t['accent']}}.f{{background:{t['primary']};padding:48px;text-align:center}}.fl img{{display:inline-block;margin:0 10px}}.fb a{{display:inline-block;padding:10px 24px;background:#fff;color:{t['primary']};text-decoration:none;font-size:12px;margin:0 6px;border-radius:4px}}.fc{{font-size:10px;color:rgba(255,255,255,0.6)}}</style></head><body><div class="c"><div class="h"><h1>{{{{ title }}}}</h1></div>{{{{ if hero_image }}}}<div class="he">{{{{ if video_url }}}}<a href="{{{{ video_url }}}}"><img src="{{{{ hero_image }}}}"></a>{{{{ else }}}}<img src="{{{{ hero_image }}}}">{{{{ endif }}}}</div>{{{{ endif }}}}{{{{ if custom_greeting }}}}<div class="g"><p>{{{{ custom_greeting }}}}</p></div>{{{{ endif }}}}{{{{ if intro_text }}}}<div class="g"><p>{{{{ intro_text }}}}</p></div>{{{{ endif }}}}<div class="p">{{{{ for product in products }}}}<div class="pi"><div class="pr"><div class="pi2">{{{{ if product.images and product.images|length > 0 }}}}<img src="{{{{ product.images[0] }}}}">{{{{ endif }}}}</div><div class="pi1">{{{{ if product.item }}}}<div class="ino">{{{{ product.item }}}}</div>{{{{ endif }}}}<div class="nm">{{{{ product.name or 'Product' }}}}</div>{{{{ if product.spec }}}}<div class="sp">{{{{ product.spec }}}}</div>{{{{ endif }}}}<div class="pm">{{{{ if product.material }}}}<span>Material: {{{{ product.material }}}}</span>{{{{ endif }}}}{{{ if product.size }}}}<span>Size: {{{{ product.size }}}}</span>{{{{ endif }}}}{{{ if product.moq }}}}<span>MOQ: {{{{ product.moq }}}}</span>{{{{ endif }}}}</div>{{{{ if product.price }}}}<div class="prc">${{{{ product.price }}}}</div>{{{{ endif }}}}</div></div></div>{{{{ endfor }}}}</div><div class="f"><div class="fl">{{{{ if main_logo }}}}<a href="{{{{ link_website }}}}"><img src="{{{{ main_logo }}}}" width="150"></a>{{{{ endif }}}}</div><div class="fb">{{{{ if link_contact }}}}<a href="{{{{ link_contact }}}}">CONTACT</a>{{{{ endif }}}}{{{ if link_website }}}}<a href="{{{{ link_website }}}}">WEBSITE</a>{{{{ endif }}}}</div><div class="fc">{{{{ copyright_text }}}}</div></div></div></body></html>'''

# Mock 数据
MOCK = {
    'title': 'PRODUCT QUOTE PROPOSAL',
    'hero_image': 'https://via.placeholder.com/640x300/1E3A5F/FFFFFF?text=Hero+Image',
    'video_url': '',
    'custom_greeting': 'Dear Customer,\n\nThank you for your interest.',
    'intro_text': 'Please find our product quotes below.',
    'main_logo': 'https://via.placeholder.com/150x50/D4AF37/FFFFFF?text=LINKLIFE',
    'sub_logos': ['https://via.placeholder.com/80x35/666/FFF?text=B1', 'https://via.placeholder.com/80x35/666/FFF?text=B2', 'https://via.placeholder.com/80x35/666/FFF?text=B3'],
    'link_contact': '#', 'link_website': '#',
    'copyright_text': '2005-2026 linklife. All rights reserved.',
    'products': [
        {'item': 'SKU-001', 'name': 'Premium Product A', 'spec': 'High quality', 'material': 'Metal', 'size': '10x10cm', 'cbm': '0.01', 'moq': '100pcs', 'price': 25.99, 'images': ['https://via.placeholder.com/200x200/eee/333?text=Product+A']},
        {'item': 'SKU-002', 'name': 'Premium Product B', 'spec': 'Modern design', 'material': 'Wood', 'size': '20x20cm', 'cbm': '0.02', 'moq': '50pcs', 'price': 45.50, 'images': ['https://via.placeholder.com/200x200/eee/333?text=Product+B']},
    ]
}

if __name__ == '__main__':
    print("Generating templates...")
    
    # 生成 30 个模板
    count = 1
    for layout_key, layout_name in LAYOUTS:
        for theme_key, theme in THEMES.items():
            tpl = make_template(theme, layout_key)
            fname = f"theme_{count:02d}.html"
            with open(OUTPUT_DIR / fname, 'w', encoding='utf-8') as f:
                f.write(tpl)
            print(f"  {fname} - {layout_name} / {theme['name']}")
            count += 1
    
    print(f"\n✓ 30 templates generated!")
    
    # 生成索引页
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Template Gallery - QuoteMailerWeb</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #1a1a1a; color: #fff; display: flex; height: 100vh; overflow: hidden; }
        .sidebar { width: 280px; background: #252525; overflow-y: auto; padding: 20px; border-right: 1px solid #333; }
        .sidebar h2 { font-size: 14px; color: #888; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #333; }
        .template-btn { display: block; width: 100%; padding: 12px 16px; margin-bottom: 8px; background: #333; border: none; border-radius: 6px; color: #ccc; font-size: 13px; text-align: left; cursor: pointer; transition: all 0.2s; }
        .template-btn:hover { background: #444; color: #fff; }
        .template-btn.active { background: #E65100; color: #fff; }
        .template-btn .num { display: inline-block; width: 24px; height: 24px; background: rgba(255,255,255,0.1); border-radius: 4px; text-align: center; line-height: 24px; font-size: 11px; margin-right: 10px; }
        .preview { flex: 1; display: flex; align-items: center; justify-content: center; background: #666; }
        .preview iframe { width: 640px; height: 100%; border: none; background: #fff; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Template Gallery</h2>
'''
    
    count = 1
    for layout_key, layout_name in LAYOUTS:
        for theme_key, theme in THEMES.items():
            active = 'active' if count == 1 else ''
            index_html += f'        <button class="template-btn {active}" onclick="loadTemplate({count}, this)"><span class="num">{count}</span>Theme {count:02d}</button>\n'
            count += 1
    
    index_html += '''    </div>
    <div class="preview">
        <iframe id="previewFrame" src="templates/theme_01.html"></iframe>
    </div>
    <script>
        function loadTemplate(num, btn) {
            document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('previewFrame').src = 'templates/theme_' + String(num).padStart(2, '0') + '.html';
        }
    </script>
</body>
</html>'''
    
    with open(OUTPUT_DIR.parent / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✓ index.html generated!")
    print(f"\n模板位置: {OUTPUT_DIR}")
    print(f"预览页: {OUTPUT_DIR.parent / 'index.html'}")
