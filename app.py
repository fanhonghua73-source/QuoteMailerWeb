"""
QuoteMailer Web - 带项目管理
"""

import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from core.excel_parser import ExcelParser
from core.template_engine import TemplateEngine
from core.mail_sender import MailSender

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROJECTS_FOLDER'] = 'projects'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROJECTS_FOLDER'], exist_ok=True)

# 默认 SMTP 配置（管理员模式）
DEFAULT_SMTP = {
    'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', '587')),
    'user': os.getenv('SMTP_USER', ''),
    'pass': os.getenv('SMTP_PASS', ''),
    'from_name': os.getenv('SMTP_FROM', 'NINGBO FUTURE')
}

# 管理员密码
ADMIN_PASS = os.getenv('ADMIN_PASS', 'admin123')

# ============ 静默全局品牌配置 (不暴露给前端) ============
BRAND_ASSETS = {
    'main_logo': 'https://files.catbox.moe/15yc0o.png',
    'sub_logos': [
        'https://files.catbox.moe/tvjn84.png',
        'https://files.catbox.moe/zud8uf.png',
        'https://files.catbox.moe/mwrhlv.png',
        'https://files.catbox.moe/1mutgo.png',
        'https://files.catbox.moe/bs024j.png',
    ],
    'link_contact': 'https://www.linkedin.com/in/chaoyu-tong-666b89275',
    'link_website': 'https://link-int.com',
    'copyright_text': '2005-2026 linklife. All rights reserved.'
}


# ============ 项目管理辅助函数 ============

def get_projects():
    """获取所有项目"""
    projects = []
    # 使用绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    
    if not os.path.exists(projects_dir):
        return projects
    
    for name in os.listdir(projects_dir):
        path = os.path.join(projects_dir, name)
        if os.path.isdir(path):
            config_path = os.path.join(path, 'config.json')
            quote_path = os.path.join(path, 'quote.xlsx')
            
            project = {
                'name': name,
                'has_config': os.path.exists(config_path),
                'has_quote': os.path.exists(quote_path),
                'updated_at': os.path.getmtime(path)
            }
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    project['config'] = json.load(f)
            
            projects.append(project)
    
    # 按更新时间排序
    projects.sort(key=lambda x: x['updated_at'], reverse=True)
    return projects


def get_project(name):
    """获取单个项目"""
    # 使用绝对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    path = os.path.join(projects_dir, name)
    
    print(f"[DEBUG] get_project: base_dir={base_dir}, projects_dir={projects_dir}, path={path}")
    
    if not os.path.isdir(path):
        return None
    
    config_path = os.path.join(path, 'config.json')
    quote_path = os.path.join(path, 'quote.xlsx')
    
    project = {
        'name': name,
        'has_config': os.path.exists(config_path),
        'has_quote': os.path.exists(quote_path),
        'path': path
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            project['config'] = json.load(f)
    
    return project


def create_project(name):
    """创建新项目"""
    path = os.path.join(app.config['PROJECTS_FOLDER'], name)
    if os.path.exists(path):
        return False, "项目已存在"
    
    os.makedirs(path)
    
    # 创建默认配置
    config = {
        'hero_image': '',
        'video_url': '',
        'greeting': '',
        'template_name': 'tpl_nordic.html',
        'extra_modules': [],
        'smtp_host': DEFAULT_SMTP['host'],
        'smtp_port': DEFAULT_SMTP['port'],
        'smtp_user': DEFAULT_SMTP['user'],
        'from_name': DEFAULT_SMTP['from_name']
    }
    
    config_path = os.path.join(path, 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return True, "项目创建成功"


def save_project_config(name, config):
    """保存项目配置"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    path = os.path.join(projects_dir, name)
    
    if not os.path.isdir(path):
        return False, "项目不存在"
    
    config_path = os.path.join(path, 'config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return True, "配置已保存"


def upload_project_quote(name, file):
    """上传项目报价单"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    path = os.path.join(projects_dir, name)
    
    if not os.path.isdir(path):
        return False, "项目不存在"
    
    filename = secure_filename('quote.xlsx')
    filepath = os.path.join(path, filename)
    file.save(filepath)
    
    print(f"[DEBUG] File saved to: {filepath}")
    return True, "报价单已上传"


# ============ Flask 路由 ============

@app.route('/')
def index():
    """业务员端主页"""
    return render_template('index.html')


def check_admin_auth():
    """检查管理员认证"""
    auth = request.authorization
    if not auth:
        return False
    expected_password = os.getenv('ADMIN_PASS', 'linklife123')
    return auth.password == expected_password


@app.route('/admin')
def admin():
    """管理员端主页 - 需要 Basic Auth 密码保护"""
    if not check_admin_auth():
        return Response('需要登录', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'})
    return render_template('admin.html')


@app.route('/api/projects/<name>', methods=['DELETE'])
def delete_project_api(name):
    """删除项目"""
    if not check_admin_auth():
        return Response('需要登录', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'})
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    project_path = os.path.join(projects_dir, name)
    
    if not os.path.isdir(project_path):
        return jsonify({'error': '项目不存在'}), 404
    
    try:
        import shutil
        shutil.rmtree(project_path)
        print(f"[API] 项目已删除: {project_path}")
        return jsonify({'success': True, 'message': '项目已删除'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """获取项目列表"""
    projects = get_projects()
    return jsonify({'success': True, 'projects': projects})


@app.route('/api/projects', methods=['POST'])
def create_project_api():
    """创建新项目"""
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({'error': '请输入项目名称'}), 400
    
    # 验证名称
    name = secure_filename(name)
    if not name:
        return jsonify({'error': '项目名称不合法'}), 400
    
    success, msg = create_project(name)
    
    if success:
        return jsonify({'success': True, 'message': msg, 'name': name})
    else:
        return jsonify({'error': msg}), 400


@app.route('/api/projects/<name>', methods=['GET'])
def get_project_api(name):
    """获取项目详情"""
    print(f"[DEBUG] get_project_api called with name: {name}")
    project = get_project(name)
    
    if not project:
        print(f"[DEBUG] Project not found: {name}")
        return jsonify({'error': '项目不存在'}), 404
    
    print(f"[DEBUG] Project found: {project['name']}, has_quote: {project['has_quote']}, path: {project['path']}")
    
    # 检查实际文件是否存在
    quote_path = os.path.join(project['path'], 'quote.xlsx')
    actual_exists = os.path.exists(quote_path)
    print(f"[DEBUG] quote.xlsx exists check: {actual_exists}, full path: {quote_path}")
    
    return jsonify({'success': True, 'project': project})


@app.route('/api/projects/<name>', methods=['PUT'])
def update_project_api(name):
    """更新项目配置"""
    data = request.json
    
    config = data.get('config', {})
    success, msg = save_project_config(name, config)
    
    if success:
        return jsonify({'success': True, 'message': msg})
    else:
        return jsonify({'error': msg}), 400


@app.route('/api/projects/<name>/rename', methods=['POST'])
def rename_project_api(name):
    """重命名项目"""
    data = request.json
    new_name = data.get('new_name', '').strip()
    
    if not new_name:
        return jsonify({'error': '请输入新名称'}), 400
    
    # 检查非法字符
    import re
    if not re.match(r'^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$', new_name):
        return jsonify({'error': '名称只能包含字母、数字、中文、下划线和连字符'}), 400
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projects_dir = os.path.join(base_dir, app.config['PROJECTS_FOLDER'])
    
    old_path = os.path.join(projects_dir, name)
    new_path = os.path.join(projects_dir, new_name)
    
    if not os.path.isdir(old_path):
        return jsonify({'error': '原项目不存在'}), 400
    
    if os.path.isdir(new_path):
        return jsonify({'error': '新名称已存在'}), 400
    
    try:
        os.rename(old_path, new_path)
        return jsonify({'success': True, 'message': f'已重命名为 {new_name}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<name>/quote', methods=['POST'])
def upload_quote_api(name):
    """上传报价单"""
    print(f"[DEBUG] upload_quote_api called with name: {name}")
    
    if 'file' not in request.files:
        print("[DEBUG] No file in request.files")
        return jsonify({'error': '请选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("[DEBUG] Empty filename")
        return jsonify({'error': '未选择文件'}), 400
    
    success, msg = upload_project_quote(name, file)
    
    if success:
        # 验证文件确实保存了
        project_path = os.path.join(app.config['PROJECTS_FOLDER'], name)
        quote_path = os.path.join(project_path, 'quote.xlsx')
        exists = os.path.exists(quote_path)
        print(f"[DEBUG] After upload, quote.xlsx exists: {exists}, path: {quote_path}")
        return jsonify({'success': True, 'message': msg})
    else:
        print(f"[DEBUG] Upload failed: {msg}")
        return jsonify({'error': msg}), 400


@app.route('/api/preview', methods=['POST'])
def generate_preview():
    """生成预览"""
    try:
        data = request.json
        project_name = data.get('project_name')
        
        print(f"[DEBUG] generate_preview called with project_name: {project_name}")
        
        if not project_name:
            return jsonify({'error': '请选择项目'}), 400
        
        # 获取项目
        project = get_project(project_name)
        if not project:
            return jsonify({'error': '项目不存在'}), 400
        
        print(f"[DEBUG] project.has_quote: {project.get('has_quote')}")
        
        if not project['has_quote']:
            # 再次确认文件是否存在
            quote_path = os.path.join(project['path'], 'quote.xlsx')
            exists = os.path.exists(quote_path)
            print(f"[DEBUG] quote.xlsx path: {quote_path}, exists: {exists}")
            return jsonify({'error': '请先上传报价单'}), 400
        
        # 读取配置
        config = project.get('config', {})
        
        # 获取模板名称 - 前端可以覆盖
        template_name = data.get('template_name') or config.get('template_name', 'tpl_nordic.html')
        
        # 多图排版样式 - 前端可以覆盖
        gallery_style = data.get('gallery_style') or config.get('gallery_style', 'strip')
        
        # 单产品样式覆盖 - 前端可以覆盖
        gallery_overrides = data.get('gallery_overrides') or config.get('gallery_overrides', {})
        
        # 支持前端传入的自定义问候语（业务员模式）
        custom_greeting = data.get('custom_greeting')
        if not custom_greeting:
            custom_greeting = config.get('greeting')
        
        # 解析 Excel
        quote_path = os.path.join(project['path'], 'quote.xlsx')
        print(f"[DEBUG] Reading Excel from: {quote_path}")
        parser = ExcelParser(quote_path)
        excel_data = parser.parse()
        
        products = excel_data.get('products', [])
        
        print(f"[API] 项目 {project_name}: {len(products)} 个产品")
        
        # 生成预览 - 使用动态模板
        engine = TemplateEngine(template_name=template_name)
        
        html = engine.render(
            products=products,
            title="Product Quote Proposal",
            intro_text="Thank you for your interest in our products. Please find our carefully selected product quotes below.",
            custom_greeting=custom_greeting,
            hero_image=config.get('hero_image') or None,
            video_url=config.get('video_url') or None,
            gallery_style=gallery_style,
            gallery_overrides=gallery_overrides,
            extra_modules=config.get('extra_modules') or [],
            is_preview=True,
            **BRAND_ASSETS
        )
        
        return jsonify({
            'success': True,
            'html': html,
            'product_count': len(products)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/send', methods=['POST'])
def send_email():
    """发送邮件
    
    支持两种模式：
    1. 业务员模式：前端传入 smtp_user/smtp_pass（个人邮箱）
    2. 管理员模式：使用 .env 中的默认 SMTP 配置
    3. 测试模式：is_test=true，强制使用 TEST_RECIPIENT
    """
    try:
        data = request.json
        project_name = data.get('project_name')
        to_email = data.get('to_email')
        is_test = data.get('is_test', False)
        
        # 业务员个人配置（可选）
        smtp_user = data.get('smtp_user')
        smtp_pass = data.get('smtp_pass')
        
        if not project_name:
            return jsonify({'error': '请选择项目'}), 400
        
        # 测试模式：使用全局测试发件箱，但收件人仍是真实的客户邮箱
        if is_test:
            if not to_email:
                return jsonify({'error': '请输入客户邮箱'}), 400
            print(f"[API] 测试模式：使用全局发件箱，发送到 {to_email}")
        elif not to_email:
            return jsonify({'error': '请输入收件人'}), 400
        
        # 获取项目
        project = get_project(project_name)
        if not project:
            return jsonify({'error': '项目不存在'}), 404
        
        if not project['has_quote']:
            return jsonify({'error': '请先上传报价单'}), 400
        
        # 读取配置
        config = project.get('config', {})
        
        # 加载全局设置
        global_settings = load_settings()
        
        # SMTP 配置优先级：
        # 1. 前端传入的个人凭据（业务员正式发送模式）
        # 2. 全局测试发件箱配置（is_test 模式）
        # 3. 项目配置中的凭据
        # 4. .env 全局配置（管理员模式）
        if smtp_user and smtp_pass:
            # 业务员使用自己的邮箱
            smtp_host = data.get('smtp_host') or 'smtp.gmail.com'
            smtp_port = int(data.get('smtp_port') or 587)
            from_name = data.get('from_name') or config.get('from_name') or DEFAULT_SMTP['from_name']
        elif is_test and global_settings.get('smtp_user'):
            # 测试模式：使用全局配置的测试发件箱
            smtp_host = global_settings.get('smtp_host', 'smtp.gmail.com')
            smtp_port = int(global_settings.get('smtp_port', 587))
            smtp_user = global_settings.get('smtp_user', '')
            smtp_pass = global_settings.get('smtp_pass', '')
            from_name = global_settings.get('smtp_from', DEFAULT_SMTP['from_name'])
        else:
            # 管理员使用全局配置或 .env
            smtp_host = config.get('smtp_host') or global_settings.get('smtp_host') or DEFAULT_SMTP['host']
            smtp_port = int(config.get('smtp_port') or global_settings.get('smtp_port') or DEFAULT_SMTP['port'])
            smtp_user = config.get('smtp_user') or global_settings.get('smtp_user') or DEFAULT_SMTP['user']
            smtp_pass = config.get('smtp_pass') or global_settings.get('smtp_pass') or DEFAULT_SMTP['pass']
            from_name = config.get('from_name') or global_settings.get('smtp_from') or DEFAULT_SMTP['from_name']
        
        if not smtp_user or not smtp_pass:
            return jsonify({'error': '请配置发件邮箱'}), 400
        
        # 解析 Excel
        quote_path = os.path.join(project['path'], 'quote.xlsx')
        parser = ExcelParser(quote_path)
        excel_data = parser.parse()
        
        products = excel_data.get('products', [])
        assets_dir = excel_data.get('assets_dir')
        
        template_name = config.get('template_name', 'tpl_nordic.html')
        engine = TemplateEngine(template_name=template_name)
        
        # 业务员可以自定义问候语
        custom_greeting = data.get('custom_greeting') or config.get('greeting') or None
        
        # Debug: 打印关键参数
        print(f"[DEBUG] hero_image: {config.get('hero_image')}")
        print(f"[DEBUG] main_logo: {BRAND_ASSETS.get('main_logo')}")
        
        # 渲染 HTML（邮件模式）
        html_email = engine.render(
            products=products,
            title="Product Quote Proposal",
            intro_text="Thank you for your interest in our products. Please find our carefully selected product quotes below.",
            custom_greeting=custom_greeting,
            hero_image=config.get('hero_image') or None,
            video_url=config.get('video_url') or None,
            gallery_style=config.get('gallery_style', 'strip'),
            gallery_overrides=config.get('gallery_overrides', {}),
            extra_modules=config.get('extra_modules') or [],
            is_preview=False,
            **BRAND_ASSETS
        )
        
        # Debug: 检查生成的 HTML 中是否包含 hero_image 和 main_logo
        if html_email and 'hero_image' in str(config.get('hero_image', '')):
            print("[DEBUG] hero_image 存在于 config 中")
        if BRAND_ASSETS.get('main_logo'):
            print(f"[DEBUG] main_logo 已传递: {BRAND_ASSETS.get('main_logo')[:50]}...")
        
        print(f"[API] 发送邮件到: {to_email}, 发件人: {smtp_user}")
        print(f"[API] assets_dir: {assets_dir}")
        
        # ========== 显式构建 cid_image_mapping 列表 ==========
        cid_image_mapping = []
        
        for idx, p in enumerate(products):
            item_code = p.get('item', f'itm{idx}')
            images = p.get('images', [])
            
            print(f"[API] 产品 {idx}: {item_code}, 图片列表: {images}")
            
            for img_idx, img_path in enumerate(images):
                if img_path:
                    # 检查物理路径是否存在
                    if os.path.exists(img_path):
                        # 使用与 template_engine 统一的 CID 格式: img_{item}_{index}
                        cid = f"img_{item_code}_{img_idx}"
                        cid_image_mapping.append((img_path, cid))
                        print(f"[API]   图片 {img_idx}: {img_path} -> CID: {cid}")
                    else:
                        print(f"[警告] 图片物理路径不存在: {img_path}")
                else:
                    print(f"[警告] 图片路径为空: {img_path}")
        
        # 打印总数让我核对
        print(f"[API] 准备打包发送的图片总数: {len(cid_image_mapping)}")
        
        # 将 cid_image_mapping 传给 mail_sender
        sender = MailSender(smtp_host, smtp_port, smtp_user, smtp_pass)
        
        # 动态标题：项目名称 + 品牌
        email_subject = f"{project_name} - linklife: Premium Sourcing Solutions"
        
        result = sender.send(
            from_name=from_name,
            to_emails=[to_email],
            subject=email_subject,
            html_body=html_email,
            cid_image_mapping=cid_image_mapping  # 传递显式的图片映射
        )
        
        if result['success']:
            return jsonify({'success': True, 'message': result['message']})
        else:
            return jsonify({'error': result['message']}), 500
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============ 全局设置 ============
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'global_settings.json')

def load_settings():
    """加载全局设置"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    """保存全局设置"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """获取全局设置"""
    settings = load_settings()
    # 不返回密码
    safe_settings = {k: v for k, v in settings.items() if k != 'smtp_pass'}
    return jsonify({'success': True, 'settings': safe_settings})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """更新全局设置"""
    data = request.json
    settings = load_settings()
    
    if 'smtp_host' in data:
        settings['smtp_host'] = data['smtp_host']
    if 'smtp_port' in data:
        settings['smtp_port'] = data['smtp_port']
    if 'smtp_user' in data:
        settings['smtp_user'] = data['smtp_user']
    if 'smtp_pass' in data:
        settings['smtp_pass'] = data['smtp_pass']
    if 'smtp_from' in data:
        settings['smtp_from'] = data['smtp_from']
    
    save_settings(settings)
    return jsonify({'success': True, 'message': '设置已保存'})

@app.route('/api/settings/test', methods=['POST'])
def test_settings():
    """测试发送邮件"""
    data = request.json
    to_email = data.get('to_email')
    
    settings = load_settings()
    
    smtp_host = settings.get('smtp_host') or DEFAULT_SMTP['host']
    smtp_port = int(settings.get('smtp_port') or DEFAULT_SMTP['port'])
    smtp_user = settings.get('smtp_user') or DEFAULT_SMTP['user']
    smtp_pass = settings.get('smtp_pass') or DEFAULT_SMTP['pass']
    from_name = settings.get('smtp_from') or DEFAULT_SMTP['from_name']
    
    if not smtp_user or not smtp_pass:
        return jsonify({'error': '请先配置全局发件箱'}), 400
    
    if not to_email:
        return jsonify({'error': '请输入测试收件人'}), 400
    
    # 发送测试邮件
    try:
        sender = MailSender(smtp_host, smtp_port, smtp_user, smtp_pass)
        result = sender.send(
            from_name=from_name,
            to_emails=[to_email],
            subject="QuoteMailer 测试邮件",
            html_body="<h1>测试成功！</h1><p>全局发件箱配置正确。</p>",
            images_dir=None,
            products=[]
        )
        
        if result['success']:
            return jsonify({'success': True, 'message': '测试邮件发送成功'})
        else:
            return jsonify({'error': result['message']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("QuoteMailer Web - 项目管理版")
    print("访问: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')
