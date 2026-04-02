"""
Logo 裁剪脚本：裁剪透明背景并上传到 Catbox
"""
import os
import sys
import io
from PIL import Image

# 使用 curl 下载的图片
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_logos')

# 下载的图片文件
image_files = {
    'main': os.path.join(TEMP_DIR, 'main.png'),
    'sub1': os.path.join(TEMP_DIR, 'sub1.png'),
    'sub2': os.path.join(TEMP_DIR, 'sub2.png'),
    'sub3': os.path.join(TEMP_DIR, 'sub3.png'),
    'sub4': os.path.join(TEMP_DIR, 'sub4.png'),
    'sub5': os.path.join(TEMP_DIR, 'sub5.png'),
}


def crop_transparent(image_path):
    """裁剪透明区域"""
    img = Image.open(image_path)

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    data = img.getdata()
    width, height = img.size

    left, top, right, bottom = width, height, 0, 0

    for y in range(height):
        for x in range(width):
            pixel = data[x + y * width]
            if len(pixel) >= 4 and pixel[3] > 0:
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    if left > right or top > bottom:
        print(f"  未找到非透明像素")
        return img

    # 添加 3% 边距
    padding_x = max(1, int((right - left) * 0.03))
    padding_y = max(1, int((bottom - top) * 0.03))

    left = max(0, left - padding_x)
    top = max(0, top - padding_y)
    right = min(width, right + padding_x)
    bottom = min(height, bottom + padding_y)

    cropped = img.crop((left, top, right, bottom))
    print(f"  原始: {width}x{height} -> 裁剪: {cropped.size}")
    return cropped


def upload_to_catbox(image):
    """上传到 Catbox"""
    import requests

    buf = io.BytesIO()
    image.save(buf, 'PNG')
    buf.seek(0)

    url = "https://catbox.moe/user/api.php"
    files = {'fileToUpload': ('logo.png', buf, 'image/png')}
    data = {'reqtype': 'fileupload', 'userhash': ''}

    try:
        resp = requests.post(url, files=files, data=data, timeout=60)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except Exception as e:
        print(f"  上传失败: {e}")
    return None


def main():
    print("=" * 60)
    print("开始裁剪 Logo 图片")
    print("=" * 60)

    results = {}

    for name, path in image_files.items():
        if not os.path.exists(path):
            print(f"跳过 {name}: 文件不存在")
            continue

        print(f"\n处理 {name}: {path}")
        cropped = crop_transparent(path)

        # 保存裁剪后的
        cropped_path = path.replace('.png', '_cropped.png')
        cropped.save(cropped_path, 'PNG')

        # 上传
        print(f"  上传到 Catbox...")
        url = upload_to_catbox(cropped)
        if url:
            results[name] = url
            print(f"  成功: {url}")
        else:
            print(f"  失败")

    print("\n" + "=" * 60)
    print("结果:")
    print("=" * 60)
    for k, v in results.items():
        print(f"{k}: {v}")

    if 'main' in results:
        print(f"\n主 Logo:")
        print(f"  'main_logo': '{results['main']}',")

    sub_logos = [results.get('sub1'), results.get('sub2'), results.get('sub3'), results.get('sub4'), results.get('sub5')]
    print(f"\n子品牌 Logo:")
    for i, url in enumerate(sub_logos):
        if url:
            print(f"  '{url}',")


if __name__ == '__main__':
    main()