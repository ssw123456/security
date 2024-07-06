import json
import requests
import base64
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
import numpy as np

font_path = 'font/msyh.ttc'  # 字体文件路径，请根据实际路径设置


# 使用 Pillow 加载字体文件
def load_font(size):
    return ImageFont.truetype(font_path, size)


# 使用 Pillow 绘制中文文本
def draw_chinese_text(img_pil, text, position, font_size, color):
    font = load_font(font_size)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    return np.array(img_pil)


# opencv 图片处理
def vehicle_detect(img):
    request_url1 = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num"
    request_url2 = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"

    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    params = {"image": base64_image}
    access_token = '24.bf8fc0cf59f834052ca4229c4bd9b66e.2592000.1722754959.282335-90883695'
    request_url1 = request_url1 + "?access_token=" + access_token
    request_url2 = request_url2 + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response1 = requests.post(request_url1, data=params, headers=headers)
    response2 = requests.post(request_url2, data=params, headers=headers)

    num = 0
    if response1.status_code == 200:
        data1 = response1.json()
        num = data1.get('person_num', 0)

    if response2.status_code == 200:
        data2 = response2.json()
        for item in data2.get('person_info', []):
            attr = item.get('location', {})
            x1 = attr.get('left', 0)
            y1 = attr.get('top', 0)
            x2 = x1 + attr.get('width', 0)
            y2 = y1 + attr.get('height', 0)

            # 使用 Pillow 绘制中文文本
            smoke_name = item.get('attributes', {}).get('smoke', {}).get('name', '')
            if smoke_name:
                position = (x1, y1 - 30)  # 调整文本位置，确保不会与矩形框重叠
                img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))  # 转换为 Pillow 图像格式
                img_pil = draw_chinese_text(img_pil, smoke_name, position, 24, (255, 0, 0))  # 绘制中文文本
                img = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)  # 转换回 OpenCV 图像格式

            # 使用 OpenCV 绘制矩形框
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return img, num



