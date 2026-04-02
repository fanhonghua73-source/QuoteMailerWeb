# QuoteMailerWeb 产品报价邮件系统

一个用于生成和发送产品报价邮件的 Web 管理系统，支持多模板、多项目、产品图片管理。

## 功能特性

### 核心功能
- **项目管理** - 创建、编辑、删除报价项目
- **产品报价** - 从 Excel 导入产品数据（名称、价格、图片）
- **邮件模板** - 3 种精心设计的邮件模板（Nordic、Apple、Vogue）
- **邮件预览** - 支持电脑端/手机端实时预览切换
- **邮件发送** - 支持 SMTP 邮件发送，支持测试模式
- **Logo 管理** - 自动处理主 Logo 和子品牌 Logo

### 邮件模板

| 模板 | 风格 | 适用场景 |
|------|------|----------|
| Nordic | 简约现代 | 时尚品牌 |
| Apple | 科技时尚 | 电子产品 |
| Vogue | 奢华优雅 | 高端品牌 |

### 技术栈
- **后端**: Flask + Python
- **前端**: Tailwind CSS + 原生 JavaScript
- **数据**: Excel 文件存储
- **邮件**: SMTP 协议

## 快速开始

### 1. 环境要求
- Python 3.8+
- Windows/macOS/Linux

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
创建 `.env` 文件：
```env
# SMTP 配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=Your Company Name

# 测试收件人
TEST_RECIPIENT=test@example.com
```

### 4. 启动服务
```bash
python app.py
```

访问：http://localhost:5000

### 5. 访问控制台
- 业务员端：http://localhost:5000
- 管理后台：http://localhost:5000/admin?password=linklife123

## 项目结构

```
QuoteMailerWeb/
├── app.py                 # Flask 主应用
├── core/                  # 核心模块
│   ├── template_engine.py    # 模板引擎
│   ├── excel_parser.py       # Excel 解析器
│   └── mail_sender.py        # 邮件发送器
├── templates/             # 邮件模板
│   ├── tpl_nordic.html   # Nordic 模板
│   ├── tpl_apple.html    # Apple 模板
│   └── tpl_vogue.html    # Vogue 模板
├── projects/             # 项目数据目录
│   └── [项目名]/
│       ├── config.json       # 项目配置
│       ├── quote.xlsx        # 产品报价表
│       └── uploads/          # 产品图片
├── uploads/              # 上传资源
├── static/                # 静态资源
└── .env                  # 环境配置
```

## 数据格式

### Excel 报价表 (quote.xlsx) - 标准格式

**重要说明**：系统按 Excel 列顺序读取数据，表头自动匹配字段名。标准列顺序如下：

#### 标准列顺序
| 列序号 | 字段名 | 说明 | 示例 |
|--------|--------|------|------|
| 1 | item | 型号/编号 | TS-001 |
| 2 | name | 产品名称 | Classic T-Shirt |
| 3 | spec | 规格/描述 | 100% Cotton, S-XXL |
| 4 | packing | 包装 | 50pcs/carton |
| 5 | cbm | 体积/材积 | 0.015 |
| 6 | moq | 起订量 | 500 |
| 7 | price | 价格 | 29.99 |
| 8 | currency | 货币 | USD |

#### 支持的表头别名（自动识别）
| 字段 | 支持的表头名 |
|------|-------------|
| item | item, item_no, Item, 品名, 型号 |
| name | name, product_name, 产品名称, Name, Product Name |
| spec | spec, specification, 规格, Specification, 型号 |
| packing | packing, 包装, Packing |
| cbm | cbm, 体积, CBM, cuft |
| moq | moq, 最小起订量, MOQ |
| price | price, price_fob, 单价, 价格, Price, Price FOB |
| currency | currency, 货币, Currency |

#### Excel 示例
| item | name | spec | packing | cbm | moq | price | currency |
|------|------|------|---------|-----|-----|-------|----------|
| TS-001 | Classic T-Shirt | 100% Cotton, S-XXL | 50pcs/carton | 0.015 | 500 | 29.99 | USD |
| TS-002 | Graphic T-Shirt | 80% Cotton | 50pcs/carton | 0.018 | 300 | 34.99 | USD |

#### 图片嵌入
- 直接在 Excel 中嵌入图片（插入 → 图片）
- 图片将自动提取并绑定到对应行
- 无需在 Excel 中填写图片列

### 项目配置 (config.json)
```json
{
  "hero_image": "https://example.com/hero.jpg",
  "video_url": "",
  "greeting": "Thank you for your interest in our products.",
  "template_name": "tpl_apple.html",
  "main_logo": "/uploads/main_logo.png",
  "sub_logos": [
    "/uploads/sub1.png",
    "/uploads/sub2.png"
  ],
  "link_website": "https://example.com",
  "reply_to_email": "contact@example.com"
}
```

## 使用指南

### 1. 创建新项目
1. 访问管理后台
2. 点击"新建项目"
3. 填写项目名称和基本信息

### 2. 上传产品数据
1. 在项目目录下创建 `quote.xlsx`
2. 按上述格式填写产品信息
3. 将产品图片放入 `uploads` 目录

### 3. 配置 Logo
- 主 Logo：显示在邮件顶部和尾部左侧
- 子 Logo：显示在邮件尾部（最多 6 个）

### 4. 预览邮件
1. 选择项目
2. 点击"预览"按钮
3. 切换电脑端/手机端查看效果

### 5. 发送邮件
1. 填写收件人邮箱
2. 可选择使用测试收件人
3. 点击发送

## API 接口

### 预览邮件
```
POST /api/preview
{
  "project_name": "项目名",
  "template": "模板名"
}
```

### 发送邮件
```
POST /api/send
{
  "project_name": "项目名",
  "to_email": "收件人邮箱",
  "is_test": false
}
```

### 项目列表
```
GET /api/projects
```

## 模板定制

### 手机端响应式
模板已内置响应式 CSS，支持手机端自动适配：
- 主 Logo 在手机端居中显示
- 子 Logo 在手机端保持一行 3 个
- CONTACT/WEBSITE 链接样式优化

### 自定义样式
可在各模板的 `<style>` 标签中修改样式。

## 常见问题

### SMTP 发送失败
- 检查 `.env` 中的 SMTP 凭证
- Google 邮箱需要使用"应用专用密码"
- 确保 SMTP 服务已开启

### 图片不显示
- 检查图片路径是否正确
- 确保图片已上传到项目目录

### 预览空白
- 检查 Excel 文件格式是否正确
- 查看浏览器控制台错误信息

## 更新日志

### 2026-04-02
- 优化预览功能：支持电脑/手机端切换
- 优化尾页 Logo 布局
- 修复邮箱中 CONTACT 链接样式问题
- 修复手机端主 Logo 居中显示

### 2026-04-01
- 新增 3 种邮件模板
- 实现响应式预览
- 优化手机端显示效果

## 许可证

MIT License