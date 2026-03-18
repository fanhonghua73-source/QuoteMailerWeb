"""
QuoteMailer Web - Flask 后端
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from core.excel_parser import ExcelParser
from core.template_engine import TemplateEngine
from core.mail_sender import MailSender

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 临时存储会话数据
session_data = {}


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/preview', methods=['POST'])
def generate_preview():
    """生成预览"""
    try:
        # 获取表单数据
        hero_image = request.form.get('hero_image', '').strip()
        video_url = request.form.get('video_url', '').strip()
        greeting = request.form.get('greeting', '').strip()
        
        # 处理文件上传
        if 'file' not in request.files:
            return jsonify({'error': '请上传 Excel 文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': '请上传 .xlsx 或 .xls 文件'}), 400
        
        # 保存上传文件
        filename = secure_filename(file.filename)
        session_id = str(uuid.uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
        file.save(filepath)
        
        print(f"[API] 处理文件: {filepath}")
        
        # 解析 Excel
        parser = ExcelParser(filepath)
        data = parser.parse()
        
        products = data.get('products', [])
        assets_dir = data.get('assets_dir')
        
        print(f"[API] 解析产品数: {len(products)}")
        
        # 生成预览 HTML (Base64 图片)
        engine = TemplateEngine()
        
        html = engine.render(
            products=products,
            title="Product Quote Proposal",
            intro_text="Thank you for your interest in our products. Please find our carefully selected product quotes below.",
            custom_greeting=greeting if greeting else None,
            hero_image=hero_image if hero_image else None,
            video_url=video_url if video_url else None,
            is_preview=True
        )
        
        # 存储会话数据用于发送
        session_data[session_id] = {
            'html_email': None,  # 稍后生成
            'assets_dir': assets_dir,
            'products': products,
            'filepath': filepath
        }
        
        # 生成邮件 HTML (CID 模式) - 存储备用
        html_email = engine.render(
            products=products,
            title="Product Quote Proposal",
            intro_text="Thank you for your interest in our products. Please find our carefully selected product quotes below.",
            custom_greeting=greeting if greeting else None,
            hero_image=hero_image if hero_image else None,
            video_url=video_url if video_url else None,
            is_preview=False
        )
        
        session_data[session_id]['html_email'] = html_email
        
        return jsonify({
            'success': True,
            'html': html,
            'session_id': session_id,
            'product_count': len(products)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/send', methods=['POST'])
def send_email():
    """发送邮件"""
    try:
        data = request.json
        
        session_id = data.get('session_id')
        if not session_id or session_id not in session_data:
            return jsonify({'error': '会话已过期，请重新生成预览'}), 400
        
        # 获取 SMTP 配置
        smtp_host = data.get('smtp_host')
        smtp_port = int(data.get('smtp_port', 587))
        smtp_user = data.get('smtp_user')
        smtp_pass = data.get('smtp_pass')
        from_name = data.get('from_name', 'QuoteMailer')
        to_email = data.get('to_email')
        
        if not all([smtp_host, smtp_user, smtp_pass, to_email]):
            return jsonify({'error': '请填写完整的 SMTP 配置和收件人'}), 400
        
        # 获取会话数据
        session = session_data[session_id]
        html_email = session['html_email']
        assets_dir = session['assets_dir']
        products = session['products']
        
        print(f"[API] 发送邮件到: {to_email}")
        
        # 发送邮件
        sender = MailSender(smtp_host, smtp_port, smtp_user, smtp_pass)
        result = sender.send(
            from_name=from_name,
            to_emails=[to_email],
            subject="Product Quote Proposal",
            html_body=html_email,
            images_dir=assets_dir,
            products=products
        )
        
        if result['success']:
            return jsonify({'success': True, 'message': result['message']})
        else:
            return jsonify({'error': result['message']}), 500
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """清理会话"""
    try:
        session_id = request.json.get('session_id')
        if session_id and session_id in session_data:
            session = session_data.pop(session_id)
            # 删除临时文件
            if 'filepath' in session:
                try:
                    os.remove(session['filepath'])
                except:
                    pass
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("QuoteMailer Web")
    print("访问: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')
