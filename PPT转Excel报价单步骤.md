# PPT 转 Excel 报价单处理步骤

## 1. 从 PPT 提取图片
```python
from pptx import Presentation
import os

pptx = 'xxx.pptx'
prs = Presentation(pptx)

output_dir = '项目名/images'
os.makedirs(output_dir, exist_ok=True)

for i, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if hasattr(shape, 'image'):
            img = shape.image
            img_bytes = img.blob
            # 保存图片
            with open(f'{output_dir}/slide{i+1}_{img_count}.{img.ext}', 'wb') as f:
                f.write(img_bytes)
```

## 2. 识别白底图 vs 氛围图
- **氛围图**：PPT前面几张，通常是场景图、大图
- **白底图**：PPT最后几页，背景白色，产品细节图

## 3. 复制到 static/images
```
BONBON:
- bonbon_1.jpg ~ bonbon_4.jpg (氛围图/产品大图)
- bonbon_5.png ~ bonbon_7.png (白底图/slide5)

Funky:
- funky_1.jpg ~ funky_6.jpg (氛围图)
- funky_7.png ~ funky_18.png (白底图/slide7-9)
```

## 4. 创建 Excel 报价单

### 表头格式（根据实际白底图数量）
- 1张白底图：Item | Photo 1 | Name | ...
- 3张白底图：Item | Photo 1 | Photo 2 | Photo 3 | Name | ...

### 代码示例
```python
import openpyxl
from openpyxl.drawing.image import Image

wb = openpyxl.Workbook()
ws = wb.active

# 只有1张白底图的情况
headers = ['Item', 'Photo 1', 'Name', 'Specification', 'Packing', 'CBM', 'Price FOB (USD)', 'MOQ']
ws.append(headers)

# 产品数据
data = [
    ['D010226701', None, '产品A', '规格...', 'color box', '12/40*30*35cm', '15.80', '500'],
    ['D010226702', None, '产品B', '规格...', 'color box', '12/35*35*30cm', '12.50', '500'],
]

for row in data:
    ws.append(row)

# 每个产品的白底图放在对应行的B列
# 产品1 -> B2, 产品2 -> B3, 产品3 -> B4
img_files = ['白底图1.png', '白底图2.png', '白底图3.png']

for i, fname in enumerate(img_files):
    img = Image(f'static/images/{fname}')
    img.width = 80
    img.height = 80
    ws.add_image(img, f'B{i+2}')  # row 2,3,4

wb.save('quote.xlsx')
```

## 5. 关键要点
1. **白底图才放入Excel**：不是所有图，是PPT中的白底细节图
2. **每产品1张图**：根据实际数量，不是固定3张
3. **图片位置**：放在对应产品行的B列(Photo 1)
4. **验证**：打开Excel确认图片显示正确后再使用
