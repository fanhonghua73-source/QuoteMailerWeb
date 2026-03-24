"""Template Gallery Generator - With Static Images for Live Server"""
import sys
import shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.excel_parser import ExcelParser
from jinja2 import Template
import json

OUT = Path(__file__).parent / "templates"
STATIC = Path(__file__).parent / "static" / "images"
OUT.mkdir(exist_ok=True)
STATIC.mkdir(parents=True, exist_ok=True)

# Read real data
PROJECT_DIR = Path(__file__).parent.parent / "projects" / "clic_collection"
config = json.load(open(PROJECT_DIR / "config.json", encoding='utf-8'))
parser = ExcelParser(str(PROJECT_DIR / "quote.xlsx"))
excel_data = parser.parse()
products = excel_data.get('products', [])

# Copy images to static folder and get relative paths
def copy_and_get_path(orig_path, product_idx):
    if not orig_path or not Path(orig_path).exists():
        return ''
    ext = Path(orig_path).suffix
    new_name = f"product_{product_idx}_{Path(orig_path).stem}{ext}"
    dest = STATIC / new_name
    shutil.copy2(orig_path, dest)
    return f"static/images/{new_name}"

# Process products
for idx, prod in enumerate(products):
    if prod.get('images'):
        new_imgs = []
        for img_path in prod['images']:
            new_path = copy_and_get_path(img_path, idx)
            if new_path:
                new_imgs.append(new_path)
        prod['images'] = new_imgs

print(f"Copied {sum(len(p.get('images',[])) for p in products)} images to static folder")

# Brand config
BRAND_ASSETS = {
    'main_logo': 'https://files.catbox.moe/60x3q1.png',
    'sub_logos': ['https://files.catbox.moe/lrowca.png','https://files.catbox.moe/zzybjq.png','https://files.catbox.moe/4ma01c.png','https://files.catbox.moe/sttfse.png','https://files.catbox.moe/0r05x4.png'],
    'link_contact': 'https://www.linkedin.com/in/chaoyu-tong-666b89275',
    'link_website': 'https://link-int.com',
    'copyright_text': '2005-2026 linklife. All rights reserved.'
}

def get_title(layout, products):
    if layout in ['nordic', 'card']:
        return 'PRODUCT QUOTE PROPOSAL'
    elif layout == 'zigzag':
        if products and products[0].get('name'):
            return products[0]['name'][:30]
        return 'PRODUCT QUOTE'
    return 'CLIC COLLECTION'

render_data_base = {
    'hero_image': config.get('hero_image', ''),
    'video_url': config.get('video_url', ''),
    'custom_greeting': config.get('greeting', ''),
    'intro_text': 'Thank you for your interest in our products.',
    'main_logo': BRAND_ASSETS.get('main_logo'),
    'sub_logos': BRAND_ASSETS.get('sub_logos', []),
    'link_contact': BRAND_ASSETS.get('link_contact'),
    'link_website': BRAND_ASSETS.get('link_website'),
    'copyright_text': BRAND_ASSETS.get('copyright_text'),
    'products': products
}

THEMES = [
    ('01', 'Nordic Navy', '#FFFFFF', '#1E3A5F', '#D4AF37', '#333333', '#666666', '#E5E5E5'),
    ('02', 'Executive Orange', '#FAFAFA', '#E65100', '#1A1A1A', '#2D2D2D', '#666666', '#E0E0E0'),
    ('03', 'Premium Gray', '#F5F5F5', '#424242', '#8D6E63', '#212121', '#757575', '#BDBDBD'),
    ('04', 'Morandi Green', '#F9FAFB', '#5D7B6F', '#A8B5A0', '#37474F', '#78909C', '#CFD8DC'),
    ('05', 'Obsidian Bold', '#FFFFFF', '#1A1A1A', '#FF5722', '#212121', '#757575', '#EEEEEE'),
    ('06', 'Champagne Gold', '#FFFEF9', '#9E9E9E', '#C9A227', '#424242', '#757575', '#E8E8E8'),
]

def get_css(theme):
    key, name, bg, pri, acc, txt, tl, bd = theme
    return f'''*{{margin:0;padding:0}}body{{font-family:Helvetica,Arial;background:{bg};color:{txt}}}.c{{max-width:640px;margin:0 auto;background:{bg}}}.h{{padding:60px 40px 40px;text-align:center}}.h1{{font-size:12px;letter-spacing:6px;text-transform:uppercase;color:{tl};font-weight:400}}.dv{{width:60px;height:1px;background:{bd};margin:24px auto}}.he img{{width:100%;height:auto;display:block}}.g{{padding:40px 40px 20px}}.g p{{font-size:15px;white-space:pre-wrap;line-height:1.8}}.i{{padding:0 40px 40px;text-align:center}}.i p{{font-size:14px;color:{tl}}}.p{{padding:0 40px 60px}}.pi{{margin-bottom:48px}}.pr{{display:flex;gap:24px}}.rvs{{flex-direction:row-reverse}}.pi2{{flex:0 0 220px}}.pi2 img{{width:100%;height:auto;display:block}}.pi2s{{display:flex;gap:8px;margin-top:10px}}.pi2s img{{width:80px;height:80px;object-fit:cover;border-radius:4px}}.pi1{{flex:1;padding-top:8px}}.ino{{font-size:11px;color:{tl};letter-spacing:1px;margin-bottom:4px}}.nm{{font-size:17px;font-weight:600;color:{pri};margin-bottom:8px}}.sp{{font-size:13px;color:{tl};margin-bottom:12px}}.pd{{font-size:12px;color:{tl};line-height:1.8}}.pd span{{display:block}}.pg{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.pii{{background:#fff;border-radius:8px;overflow:hidden}}.pii2{{width:100%;aspect-ratio:4/3;background:#f5f5f5}}.pii2 img{{width:100%;height:100%;object-fit:cover}}.pii2s{{display:flex;gap:4px;padding:8px;background:#fafafa}}.pii2s img{{width:40px;height:40px;object-fit:cover;border-radius:3px}}.pii1{{padding:14px}}.ino2{{font-size:9px;color:{tl};letter-spacing:1px;margin-bottom:4px}}.nm2{{font-size:13px;font-weight:600;color:{pri};margin-bottom:4px}}.pc{{display:flex;flex-direction:column;gap:20px}}.pic{{background:#fff;border-radius:16px;overflow:hidden}}.pic2{{width:100%;aspect-ratio:16/10}}.pic2 img{{width:100%;height:100%;object-fit:cover}}.pic2s{{display:flex;gap:8px;padding:12px}}.pic2s img{{width:50px;height:50px;object-fit:cover;border-radius:4px}}.pic1{{padding:22px}}.sk{{background:{pri}}}.dv2{{width:40px;height:2px;background:{pri};margin:20px auto}}.f{{padding:48px 40px;text-align:center;border-top:1px solid {bd}}}.fl{{margin-bottom:24px}}.fl img{{display:inline-block;margin:0 12px;vertical-align:middle;height:35px}}.fb{{margin-bottom:20px}}.fb a{{display:inline-block;padding:10px 24px;background:{pri};color:#fff;text-decoration:none;font-size:12px;margin:0 6px;border-radius:4px}}.fc{{font-size:10px;color:{tl}}}'''

FOOTER = '''<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #FFFFFF; border-top: 1px solid #F0F0F0; margin-top: 40px;">
<tr><td align="center" style="padding: 40px 20px;">
{% if main_logo %}<img src="{{ main_logo }}" alt="Main Brand" width="160" style="display: block; max-width: 160px; height: auto; margin: 0 auto 30px auto; border: 0;">{% endif %}
{% if sub_logos and sub_logos|length > 0 %}
<table cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto 30px auto;"><tr>
{% for logo in sub_logos %}
<td align="center" valign="middle" style="padding: 0 10px;">
<img src="{{ logo }}" alt="Sub Brand" width="110" style="display: block; width: 110px; max-width: 110px; height: auto; border: 0;">
</td>
{% endfor %}
</tr></table>
{% endif %}
<div style="margin-bottom: 20px;">{% if link_contact %}<a href="{{ link_contact }}" style="display:inline-block;padding:10px 24px;background:#333;color:#fff;text-decoration:none;font-size:12px;margin:0 6px;border-radius:4px;">CONTACT</a>{% endif %}{% if link_website %}<a href="{{ link_website }}" style="display:inline-block;padding:10px 24px;background:#333;color:#fff;text-decoration:none;font-size:12px;margin:0 6px;border-radius:4px;">WEBSITE</a>{% endif %}</div>
<div style="font-size:10px;color:#999">{{copyright_text}}</div>
</td></tr></table>'''

MULTI_IMG_MAIN = '''{% if product.images and product.images|length > 0 %}
<div style="margin-bottom: 10px;"><img src="{{ product.images[0] }}" alt="{{ product.name }}" style="display: block; width: 100%; max-width: 100%; height: auto; border: 0;"></div>
{% if product.images|length > 1 %}
<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
{% for img in product.images[1:] %}
<td align="center" valign="top" style="padding-right: 5px;"><img src="{{ img }}" alt="Detail" style="display: block; width: 100%; max-width: 100%; height: auto; border: 0;"></td>
{% endfor %}
</tr></table>
{% endif %}
{% endif %}'''

MULTI_IMG_GRID = '''{% if product.images and product.images|length > 0 %}
<div style="width:100%;aspect-ratio:4/3;background:#f5f5f5">{% if product.images[0] %}<img src="{{ product.images[0] }}" style="width:100%;height:100%;object-fit:cover">{% endif %}</div>
{% if product.images|length > 1 %}
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafafa"><tr>
{% for img in product.images[1:6] %}<td align="center"><img src="{{ img }}" width="35" height="35" style="object-fit:cover;border-radius:3px"></td>{% endfor %}
</tr></table>
{% endif %}
{% endif %}'''

LAYOUTS = {
    'nordic': '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title><style>{{CSS}}</style></head><body>
<div class="c"><div class="h"><h1 class="h1">{{title}}</h1><div class="dv"></div></div>
{% if hero_image %}<div class="he">{% if video_url %}<a href="{{video_url}}"><img src="{{hero_image}}"></a>{% else %}<img src="{{hero_image}}">{% endif %}</div>{% endif %}
{% if custom_greeting %}<div class="g"><p>{{custom_greeting}}</p></div>{% endif %}
{% if intro_text %}<div class="i"><p>{{intro_text}}</p></div>{% endif %}
<div class="p">{% for product in products %}<div class="pi"><div class="pr"><div class="pi2">''' + MULTI_IMG_MAIN + '''</div><div class="pi1">{% if product.item %}<div class="ino">{{product.item}}</div>{% endif %}<div class="nm">{{product.name or 'Product Name'}}</div>{% if product.spec %}<div class="sp">{{product.spec}}</div>{% endif %}<div class="pd">{% if product.material %}<span>Material: {{product.material}}</span>{% endif %}{% if product.size %}<span>Size: {{product.size}}</span>{% endif %}{% if product.packing %}<span>Packing: {{product.packing}}</span>{% endif %}{% if product.cbm %}<span>CBM: {{product.cbm}}</span>{% endif %}{% if product.moq %}<span>MOQ: {{product.moq}}</span>{% endif %}</div></div></div></div>{% endfor %}</div>
''' + FOOTER + '</div></body></html>',

    'zigzag': '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title><style>{{CSS}}</style></head><body>
<div class="c"><div class="sk"><div class="h"><h1 class="h1">{{title}}</h1></div></div>
{% if hero_image %}<div class="he">{% if video_url %}<a href="{{video_url}}"><img src="{{hero_image}}"></a>{% else %}<img src="{{hero_image}}">{% endif %}</div>{% endif %}
{% if custom_greeting %}<div class="g"><p>{{custom_greeting}}</p></div>{% endif %}
{% if intro_text %}<div class="i"><p>{{intro_text}}</p></div>{% endif %}
<div class="p">{% for product in products %}<div class="pi"><div class="pr {% if loop.index is even %}rvs{% endif %}"><div class="pi2">''' + MULTI_IMG_MAIN + '''</div><div class="pi1">{% if product.item %}<div class="ino">{{product.item}}</div>{% endif %}<div class="nm">{{product.name or 'Product Name'}}</div>{% if product.spec %}<div class="sp">{{product.spec}}</div>{% endif %}<div class="pd">{% if product.material %}<span>{{product.material}}</span>{% endif %}{% if product.size %}<span>{{product.size}}</span>{% endif %}{% if product.cbm %}<span>{{product.cbm}}</span>{% endif %}{% if product.moq %}<span>{{product.moq}}</span>{% endif %}</div></div></div></div>{% endfor %}</div>
''' + FOOTER + '</div></body></html>',

    'grid': '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title><style>{{CSS}}</style></head><body>
<div class="c"><div class="sk"><div class="h"><h1 class="h1">{{title}}</h1></div></div>
{% if hero_image %}<div class="he">{% if video_url %}<a href="{{video_url}}"><img src="{{hero_image}}"></a>{% else %}<img src="{{hero_image}}">{% endif %}</div>{% endif %}
{% if custom_greeting %}<div class="g"><p>{{custom_greeting}}</p></div>{% endif %}
{% if intro_text %}<div class="i"><p>{{intro_text}}</p></div>{% endif %}
<div class="p"><div class="pg">{% for product in products %}<div class="pii">''' + MULTI_IMG_GRID + '''<div class="pii1">{% if product.item %}<div class="ino2">{{product.item}}</div>{% endif %}<div class="nm2">{{product.name or 'Product'}}</div>{% if product.spec %}<div class="sp">{{product.spec}}</div>{% endif %}<div class="pd">{% if product.material %}{{product.material}}<br>{% endif %}{% if product.size %}Size: {{product.size}}<br>{% endif %}{% if product.cbm %}CBM: {{product.cbm}}<br>{% endif %}{% if product.moq %}MOQ: {{product.moq}}{% endif %}</div></div></div>{% endfor %}</div></div>
''' + FOOTER + '</div></body></html>',

    'card': '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title><style>{{CSS}}</style></head><body>
<div class="c"><div class="h"><h1 class="h1">{{title}}</h1><div class="dv2"></div></div>
{% if hero_image %}<div class="he">{% if video_url %}<a href="{{video_url}}"><img src="{{hero_image}}"></a>{% else %}<img src="{{hero_image}}">{% endif %}</div>{% endif %}
{% if custom_greeting %}<div class="g"><p>{{custom_greeting}}</p></div>{% endif %}
{% if intro_text %}<div class="i"><p>{{intro_text}}</p></div>{% endif %}
<div class="pc">{% for product in products %}<div class="pic"><div class="pic2">''' + MULTI_IMG_MAIN + '''</div><div class="pic1">{% if product.item %}<div class="ino">{{product.item}}</div>{% endif %}<div class="nm">{{product.name or 'Product Name'}}</div>{% if product.spec %}<div class="sp">{{product.spec}}</div>{% endif %}<div class="pd">{% if product.material %}<span>{{product.material}}</span>{% endif %}{% if product.size %}<span>{{product.size}}</span>{% endif %}{% if product.packing %}<span>{{product.packing}}</span>{% endif %}{% if product.cbm %}<span>{{product.cbm}}</span>{% endif %}{% if product.moq %}<span>MOQ: {{product.moq}}</span>{% endif %}</div></div></div>{% endfor %}</div>
''' + FOOTER + '</div></body></html>',

    'bold': '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title><style>{{CSS}}</style></head><body>
<div class="c"><div class="sk"><div class="h"><h1 class="h1">{{title}}</h1></div></div>
{% if hero_image %}<div class="he">{% if video_url %}<a href="{{video_url}}"><img src="{{hero_image}}"></a>{% else %}<img src="{{hero_image}}">{% endif %}</div>{% endif %}
<div class="sk">{% if custom_greeting %}<div class="g"><p>{{custom_greeting}}</p></div>{% endif %}{% if intro_text %}<div class="i"><p>{{intro_text}}</p></div>{% endif %}</div>
<div class="p">{% for product in products %}<div class="pi"><div class="pi2">''' + MULTI_IMG_MAIN + '''</div><div class="pi1">{% if product.item %}<div class="ino">{{product.item}}</div>{% endif %}<div class="nm">{{product.name or 'Product Name'}}</div>{% if product.spec %}<div class="sp">{{product.spec}}</div>{% endif %}<div class="pd">{% if product.material %}<span>Material: {{product.material}}</span>{% endif %}{% if product.size %}<span>Size: {{product.size}}</span>{% endif %}{% if product.packing %}<span>Packing: {{product.packing}}</span>{% endif %}{% if product.cbm %}<span>CBM: {{product.cbm}}</span>{% endif %}{% if product.moq %}<span>MOQ: {{product.moq}}</span>{% endif %}</div></div></div>{% endfor %}</div>
''' + FOOTER + '</div></body></html>',
}

cnt = 1
layout_names = list(LAYOUTS.keys())
for layout_key in layout_names:
    template_str = LAYOUTS[layout_key]
    for theme in THEMES:
        render_data = dict(render_data_base)
        render_data['title'] = get_title(layout_key, products)
        css = get_css(theme)
        html = template_str.replace('{{CSS}}', css)
        t = Template(html)
        rendered = t.render(**render_data)
        fname = f"theme_{cnt:02d}.html"
        (OUT / fname).write_text(rendered, encoding='utf-8')
        print(f"Generated: {fname}")
        cnt += 1

index = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Template Gallery</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial;background:#1a1a1a;color:#fff;display:flex;height:100vh;overflow:hidden}
.s{width:280px;background:#252525;overflow-y:auto;padding:15px;border-right:1px solid #333}
.s h2{font-size:12px;color:#888;letter-spacing:2px;text-transform:uppercase;margin:0 0 15px 0;padding-bottom:10px;border-bottom:1px solid #333}
.l{display:block;width:100%;padding:10px 14px;margin-bottom:6px;background:#333;border:none;border-radius:5px;color:#bbb;font-size:12px;text-align:left;cursor:pointer;transition:all .2s}
.l:hover{background:#444;color:#fff}
.l.active{background:#E65100;color:#fff}
.n{display:inline-block;width:22px;height:22px;background:rgba(255,255,255,.1);border-radius:4px;text-align:center;line-height:22px;font-size:10px;margin-right:8px}
.v{flex:1;display:flex;align-items:center;justify-content:center;background:#555}
.v iframe{width:640px;height:100%;border:none;background:#fff}
</style></head><body>
<div class="s"><h2>Template Gallery</h2>
'''

for i in range(1, 31):
    active = 'active' if i == 1 else ''
    num = str(i).zfill(2)
    layout = layout_names[(i-1)//6]
    theme = THEMES[(i-1)%6][1]
    btn = '<button class="l ' + active + '" onclick="load(' + str(i) + ',this)"><span class="n">' + num + '</span>' + layout.capitalize() + ' - ' + theme + '</button>\n'
    index += btn

index += '''</div><div class="v"><iframe id="f" src="templates/theme_01.html"></iframe></div>
<script>
function load(n,t){document.querySelectorAll('.l').forEach(b=>b.classList.remove('active'));t.classList.add('active');var s=String(n).padStart(2,'0');document.getElementById('f').src='templates/theme_'+s+'.html'}
</script></body></html>'''

(OUT.parent / 'index.html').write_text(index, encoding='utf-8')
print("\nDone! Images copied to static folder, templates generated!")
print(f"Static images: {STATIC}")
