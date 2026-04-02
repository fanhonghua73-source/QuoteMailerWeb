"""
裁剪图片透明背景并上传到 Catbox
"""
import os
import io
import requests
from PIL import Image

# 输入文件
input_file = r'C:\Users\DELL\Desktop\linkgroup_logo\processed\一.png'
output_dir = r'F:\QuoteMailerWeb\temp_logos'


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
        print("  未找到非透明像素")
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
    print("处理图片...")

    # 裁剪
    cropped = crop_transparent(input_file)

    # 保存裁剪后的
    cropped_path = os.path.join(output_dir, 'new_sub1_cropped.png')
    cropped.save(cropped_path, 'PNG')
    print(f"  保存: {cropped_path}")

    # 上传
    print("  上传到 Catbox...")
    url = upload_to_catbox(cropped)
    if url:
        print(f"\n成功! URL: {url}")
        print(f"\n替换 sub_logos[0] 为:")
        print(f"  '{url}',")
    else:
        print("  上传失败")


if __name__ == '__main__':
    main()