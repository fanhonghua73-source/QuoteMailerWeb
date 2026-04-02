"""
处理一.png - 去掉多余透明区域并调整到合适比例使其在副logo展示中更丰满
"""
import io
import requests
from PIL import Image

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

    cropped = img.crop((left, top, right, bottom))
    print(f"  原始: {width}x{height} -> 裁剪: {cropped.size}")
    return cropped


def make_it_full(cropped):
    """
    让图片在副logo展示中更丰满
    模板中第一个logo是50px宽，50px高，用object-fit:contain

    原图裁剪后是1772x279 ≈ 6.35:1
    按比例：当高度是50px时，宽度应该是 50 * 6.35 ≈ 317px

    这样上传后，在50px宽的contain显示中，会等比缩放到高度约8px显示
    但这不是丰满

    正确的理解：应该让图片在50px高度的显示区域中尽可能宽
    生成 317x50 的图片
    """
    cw, ch = cropped.size

    # 高度50px，宽度按比例
    new_height = 50
    new_width = int(cw * new_height / ch)

    result = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
    resized = cropped.resize((new_width, new_height), Image.LANCZOS)
    result.paste(resized, (0, 0))

    print(f"  调整到: {new_width}x{new_height}")
    return result


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

    # 调整使其更丰满
    full = make_it_full(cropped)

    # 保存
    full_path = r'F:\QuoteMailerWeb\temp_logos\new_sub1_full.png'
    full.save(full_path, 'PNG')
    print(f"  保存: {full_path}")

    # 上传
    print("  上传到 Catbox...")
    url = upload_to_catbox(full)
    if url:
        print(f"\n成功! URL: {url}")
    else:
        print("  上传失败")


if __name__ == '__main__':
    main()
