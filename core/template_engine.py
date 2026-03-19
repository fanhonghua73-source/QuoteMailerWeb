"""
HTML 邮件模板引擎
支持 is_preview 模式切换，Base64 内联图片
"""

import os
import base64
import copy
import mimetypes
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class TemplateEngine:
    """Jinja2 邮件模板引擎"""
    
    DEFAULT_BRAND = "linklife"
    DEFAULT_TAGLINE = "Premium Sourcing Solutions"
    
    def __init__(self, template_name: str = 'nordic_template.html'):
        template_dir = Path(__file__).parent.parent / 'templates'
        
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        self.template_name = template_name
    
    def render(self, 
               products: list,
               title: str = "Product Quote",
               intro_text: str = None,
               custom_greeting: str = None,
               hero_image: str = None,
               video_url: str = None,
               brand: str = None,
               tagline: str = None,
               is_preview: bool = False) -> str:
        """
        渲染 HTML 邮件
        
        Args:
            products: 产品列表
            title: 邮件标题
            intro_text: 引言文字
            custom_greeting: 自定义问候语
            hero_image: 封面图 URL
            video_url: 视频链接
            brand: 品牌名
            tagline: 品牌标语
            is_preview: True=Base64图片, False=CID (邮件)
        """
        template = self.env.get_template(self.template_name)
        
        # 深拷贝，不污染原数据
        render_products = copy.deepcopy(products)
        
        # 处理产品图片
        render_products = self._process_products(render_products, is_preview)
        
        # 渲染
        html = template.render(
            title=title,
            intro_text=intro_text,
            custom_greeting=custom_greeting,
            hero_image=self._resolve_image_path(hero_image) if hero_image else None,
            video_url=video_url,
            products=render_products,
            brand=brand or self.DEFAULT_BRAND,
            tagline=tagline or self.DEFAULT_TAGLINE,
            is_preview=is_preview
        )
        
        return html
    
    def _process_products(self, products: list, is_preview: bool) -> list:
        """处理产品多张图片 - 统一生成 CID"""
        processed = []
        
        for idx, product in enumerate(products):
            p = dict(product)
            images = product.get('images', [])
            
            if images:
                # 统一生成 CID 列表 - 用于邮件模式
                cids = []
                item = product.get('item', f'itm{idx}')
                for i in range(len(images)):
                    # 统一格式: img_{item}_{index}
                    cid_str = f"img_{item}_{i}"
                    cids.append(cid_str)
                p['cids'] = cids
                
                if is_preview:
                    # 预览模式：转换为 Base64 列表
                    base64_images = []
                    for img_path in images:
                        try:
                            ext = Path(img_path).suffix.lower()
                            mime_type = {
                                '.png': 'image/png',
                                '.jpg': 'image/jpeg',
                                '.jpeg': 'image/jpeg',
                                '.gif': 'image/gif'
                            }.get(ext, 'image/png')
                            
                            with open(img_path, 'rb') as f:
                                b64_data = base64.b64encode(f.read()).decode('utf-8')
                            
                            base64_images.append(f"data:{mime_type};base64,{b64_data}")
                        except Exception as e:
                            print(f"[Error] Base64 转换失败: {img_path}, {e}")
                            base64_images.append("")
                    
                    p['preview_srcs'] = base64_images
                else:
                    # 邮件模式：使用统一的 cids
                    pass
            
            processed.append(p)
        
        return processed
    
    def _resolve_image_path(self, path: str) -> str:
        """转换本地图片路径为 file:// URL"""
        if not path:
            return path
            
        if path.startswith('http://') or path.startswith('https://'):
            return path
        
        abs_path = Path(path).resolve()
        return f"file:///{str(abs_path).replace(chr(92), '/')}"
    
    def render_to_file(self, products: list, output_path: str, **kwargs) -> str:
        """渲染并保存到文件"""
        html = self.render(products, is_preview=True, **kwargs)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html


if __name__ == "__main__":
    import sys
    from excel_parser import ExcelParser
    
    if len(sys.argv) < 2:
        print("用法: python template_engine.py <excel文件路径>")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    
    parser = ExcelParser(excel_path)
    data = parser.parse()
    
    engine = TemplateEngine()
    
    output_path = "preview.html"
    engine.render_to_file(
        products=data['products'],
        output_path=output_path,
        title="Product Quote Proposal"
    )
    
    print(f"已生成: {output_path}")
