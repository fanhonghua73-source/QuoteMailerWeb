"""
邮件发送模块 - 严格 RFC 标准 MIME 结构
"""

import smtplib
import os
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from typing import List, Dict
from pathlib import Path


class MailSender:
    """SMTP 邮件发送器"""
    
    SMTP_CONFIG = {
        'gmail': {'host': 'smtp.gmail.com', 'port': 587},
        'outlook': {'host': 'smtp.office365.com', 'port': 587},
        'qq': {'host': 'smtp.qq.com', 'port': 587},
        '163': {'host': 'smtp.163.com', 'port': 587},
    }
    
    def __init__(self, 
                 smtp_host: str, 
                 smtp_port: int, 
                 username: str, 
                 password: str,
                 use_tls: bool = True):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    @classmethod
    def from_preset(cls, preset: str, username: str, password: str):
        if preset not in cls.SMTP_CONFIG:
            raise ValueError(f"Unknown preset: {preset}")
        
        config = cls.SMTP_CONFIG[preset]
        return cls(
            smtp_host=config['host'],
            smtp_port=config['port'],
            username=username,
            password=password
        )
    
    def send(self,
             from_name: str,
             to_emails: List[str],
             subject: str,
             html_body: str,
             images_dir: str = None,
             products: List[Dict] = None,
             cid_image_mapping: List[tuple] = None) -> dict:
        """
        发送邮件 - 严格 RFC MIME 嵌套结构
        multipart/related > multipart/alternative > HTML + Images
        
        参数:
        - cid_image_mapping: 显式的图片映射列表 [(物理路径, CID), ...]
        """
        try:
            # ========== 1. 最外层: related (关联图片和正文) ==========
            msg_root = MIMEMultipart('related')
            msg_root['From'] = f"{from_name} <{self.username}>"
            msg_root['To'] = ', '.join(to_emails)
            msg_root['Subject'] = Header(subject, 'utf-8')
            
            # 调试：打印 HTML 中的第一个 img 标签
            import re
            img_matches = re.findall(r'<img[^>]+src="[^"]+"[^>]*>', html_body[:2000])
            if img_matches:
                print(f"[MailSender] HTML 中第一个 img: {img_matches[0]}")
            
            # ========== 2. 创建 alternative 容器 (专门装 HTML 正文) ==========
            msg_alternative = MIMEMultipart('alternative')
            msg_root.attach(msg_alternative)
            
            # ========== 3. 将 HTML 正文附加到 alternative 容器 ==========
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg_alternative.attach(html_part)
            print("[MailSender] HTML 正文已附加到 alternative")
            
            # ========== 4. 使用显式的 cid_image_mapping 附加图片 ==========
            if cid_image_mapping:
                print(f"[MailSender] 使用显式图片映射，数量: {len(cid_image_mapping)}")
                self._attach_images_from_mapping(msg_root, cid_image_mapping)
            elif images_dir and products:
                # 兼容旧方式
                print(f"[MailSender] 使用旧方式附加图片")
                self._attach_images_to_related(msg_root, images_dir, products)
            else:
                print("[MailSender] 没有图片需要附加")
            
            # ========== 发送 ==========
            print(f"[MailSender] 准备发送邮件...")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg_root)
            
            print(f"[MailSender] 发送成功!")
            return {'success': True, 'message': f'已发送到 {len(to_emails)} 个收件人'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}
    
    def _attach_images_from_mapping(self, msg_root, cid_image_mapping: List[tuple]):
        """从显式映射附加图片"""
        print(f"[MailSender] _attach_images_from_mapping 被调用，图片数: {len(cid_image_mapping)}")
        
        for img_idx, (img_path, cid) in enumerate(cid_image_mapping):
            # 清理 CID
            clean_cid = cid.replace('cid:', '').strip('<>')
            print(f"[MailSender]   图片 {img_idx}: {img_path}, CID: {clean_cid}")
            
            # 强制校验
            if not os.path.exists(img_path):
                print(f"[致命错误] 找不到图片: {img_path}")
                raise FileNotFoundError(f"邮件打包丢失图片: {img_path}")
            
            # MIME 类型检测
            ctype, _ = mimetypes.guess_type(str(img_path))
            if ctype is None or not ctype.startswith('image/'):
                ctype = 'image/jpeg'
            
            maintype, subtype = ctype.split('/', 1)
            print(f"[MailSender]   MIME: {maintype}/{subtype}")
            
            # 读取图片
            with open(img_path, 'rb') as f:
                img_data = f.read()
            
            # 创建 MIMEImage
            image_part = MIMEImage(img_data, _subtype=subtype)
            
            # 核心：Content-ID 和 inline
            image_part.add_header('Content-ID', f'<{clean_cid}>')
            image_part.add_header('Content-Disposition', 'inline')
            
            # 附加到外层 related 容器
            msg_root.attach(image_part)
            print(f"[MailSender]   已附加: <{clean_cid}>")
        
        print("[MailSender] 所有图片附加完成")
    
    def _attach_images_to_related(self, msg_root, images_dir: str, products: List[Dict]):
        """严格 RFC - 将图片附加到 related 容器"""
        img_dir = Path(images_dir)
        print(f"[MailSender] 图片目录: {img_dir}")
        print(f"[MailSender] 产品数量: {len(products)}")
        
        for idx, product in enumerate(products):
            images = product.get('images', [])
            item_name = product.get('item', f'product_{idx}')
            cid_images = product.get('cid_images', [])
            
            print(f"[MailSender] 产品 {idx}: {item_name}, 图片数: {len(images)}")
            
            for img_idx, img_filename in enumerate(images):
                # 获取对应的 CID
                if img_idx < len(cid_images):
                    cid = cid_images[img_idx]
                else:
                    cid = f"{item_name}_img_{img_idx}"
                
                # 清理 CID
                clean_cid = cid.replace('cid:', '').strip('<>')
                print(f"[MailSender]   图片 {img_idx}: {img_filename}, CID: {clean_cid}")
                
                # 路径处理
                if os.path.isabs(img_filename):
                    img_path = img_filename
                else:
                    img_path = img_dir / img_filename
                
                # 强制校验
                if not os.path.exists(img_path):
                    print(f"[致命错误] 找不到图片: {img_path}")
                    raise FileNotFoundError(f"邮件打包丢失图片: {img_path}")
                
                # MIME 类型检测
                ctype, _ = mimetypes.guess_type(str(img_path))
                if ctype is None or not ctype.startswith('image/'):
                    ctype = 'image/jpeg'
                
                maintype, subtype = ctype.split('/', 1)
                print(f"[MailSender]   MIME: {maintype}/{subtype}")
                
                # 读取图片
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                
                # 创建 MIMEImage
                image_part = MIMEImage(img_data, _subtype=subtype)
                
                # 核心：Content-ID 和 inline
                image_part.add_header('Content-ID', f'<{clean_cid}>')
                image_part.add_header('Content-Disposition', 'inline')
                
                # 附加到外层 related 容器
                msg_root.attach(image_part)
                print(f"[MailSender]   已附加到 related: <{clean_cid}>")
        
        print("[MailSender] 所有图片附加完成")
    
    def _attach_product_images_strict(self, msg, images_dir: str, products: List[Dict]):
        """严格 RFC 标准 - 附加产品图片"""
        img_dir = Path(images_dir)
        print(f"[MailSender] 图片目录: {img_dir}")
        print(f"[MailSender] 产品数量: {len(products)}")
        
        for idx, product in enumerate(products):
            images = product.get('images', [])
            item_name = product.get('item', f'product_{idx}')
            cid_images = product.get('cid_images', [])
            
            print(f"[MailSender] 产品 {idx}: {item_name}, 图片数量: {len(images)}, CID数量: {len(cid_images)}")
            
            # 遍历所有图片
            for img_idx, img_filename in enumerate(images):
                # 获取对应的 CID
                if img_idx < len(cid_images):
                    cid = cid_images[img_idx]
                else:
                    cid = f"{item_name}_img_{img_idx}"
                
                # 清理 CID（去掉 cid: 前缀）
                clean_cid = cid.replace('cid:', '').strip('<>')
                print(f"[MailSender]   图片 {img_idx}: {img_filename}, CID: {clean_cid}")
                
                # 支持两种格式：完整路径或文件名
                if os.path.isabs(img_filename):
                    img_path = img_filename
                else:
                    img_path = img_dir / img_filename
                
                # 强制校验文件存在
                if not os.path.exists(img_path):
                    print(f"[致命错误] 找不到图片: {img_path}")
                    raise FileNotFoundError(f"邮件打包丢失图片: {img_path}")
                
                print(f"[MailSender]   找到图片: {img_path}")
                
                # ========== 严格 MIME 图片附件 ==========
                # 动态获取图片类型
                ctype, _ = mimetypes.guess_type(str(img_path))
                if ctype is None or not ctype.startswith('image/'):
                    ctype = 'image/jpeg'
                
                maintype, subtype = ctype.split('/', 1)
                print(f"[MailSender]   MIME类型: {maintype}/{subtype}")
                
                # 读取图片数据
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                
                # 创建 MIMEImage
                image_part = MIMEImage(img_data, _subtype=subtype)
                
                # 核心！标准头信息 - 只用尖括号包裹 CID
                image_part.add_header('Content-ID', f'<{clean_cid}>')
                image_part.add_header('Content-Disposition', 'inline')
                
                msg.attach(image_part)
                print(f"[MailSender]   图片已附加: <{clean_cid}>")
        
        print("[MailSender] 所有图片附加完成")
    
    def test_connection(self) -> dict:
        """测试 SMTP 连接"""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
            return {'success': True, 'message': '连接成功'}
        except Exception as e:
            return {'success': False, 'message': str(e)}


if __name__ == "__main__":
    sender = MailSender.from_preset(
        'gmail',
        username='your@gmail.com',
        password='your_app_password'
    )
    print(sender.test_connection())
