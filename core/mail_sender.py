"""
邮件发送模块 - 正确 MIME 结构
"""

import smtplib
import os
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
             products: List[Dict] = None) -> dict:
        """
        发送邮件（正确的 MIME 结构）
        
        关键：必须先 attach HTML，再 attach 图片
        """
        try:
            # 1. 创建根容器 (必须是 related)
            msg = MIMEMultipart('related')
            msg['From'] = f"{from_name} <{self.username}>"
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 2. 附加 HTML 正文 (必须最先 attach)
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 3. 循环附加图片 (带 Content-ID)
            if images_dir and products:
                self._attach_product_images(msg, images_dir, products)
            
            # 发送
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return {'success': True, 'message': f'已发送到 {len(to_emails)} 个收件人'}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}
    
    def _attach_product_images(self, msg, images_dir: str, products: List[Dict]):
        """附加产品图片"""
        img_dir = Path(images_dir)
        
        for idx, product in enumerate(products):
            images = product.get('images', [])
            item_name = product.get('item', f'product_{idx}')
            
            for img_idx, img_filename in enumerate(images):
                img_path = img_dir / img_filename
                if img_path.exists():
                    cid = f"{item_name}_{img_idx}"
                    self._attach_image(msg, str(img_path), cid)
    
    def _attach_image(self, msg, img_path: str, cid: str):
        """附加单张图片"""
        with open(img_path, 'rb') as f:
            img_data = f.read()
        
        img = MIMEImage(img_data)
        img.add_header('Content-ID', f'<{cid}>')
        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
        msg.attach(img)
    
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
