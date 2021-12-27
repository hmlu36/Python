from PIL import Image
from pytesseract import *

def convert_Image(img, standard=127.5):
    '''
    【灰度轉換】
    '''
    image = img.convert('L')

    '''
    【二值化】
    根據閾值 standard , 將所有畫素都置為 0(黑色) 或 255(白色), 便於接下來的分割
    '''
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image

def _get_p_black_count(img: Image, _w: int, _h: int):
    """ 获取当前位置周围像素点中黑色元素的个数
    Args:
        img (img): 图像信息
        _w (int): w坐标
        _h (int): h坐标
    Returns:
        int: 个数
    """
    w, h = img.size
    p_round_items = []
    # 超过了横纵坐标
    if _w == 0 or _w == w-1 or 0 == _h or _h == h-1:
        return 0
    p_round_items = [img.getpixel(
        (_w, _h-1)), img.getpixel((_w, _h+1)), img.getpixel((_w-1, _h)), img.getpixel((_w+1, _h))]
    p_black_count = 0
    for p_item in p_round_items:
        if p_item == (0, 0, 0):
            p_black_count = p_black_count+1
    return p_black_count

def _remove_pil(img: Image):
    """清理干扰识别的线条和噪点
    Args:
        img (img): 图像对象
    Returns:
        [img]: 被清理过的图像对象
    """
    w, h = img.size
    for _w in range(w):
        for _h in range(h):
            o_pixel = img.getpixel((_w, _h))
            # 当前像素点是红色(线段) 或者 绿色（噪点）
            if o_pixel == (255, 0, 0) or o_pixel == (0, 0, 255):
                # 周围黑色数量大于2，则把当前像素点填成黑色；否则用白色覆盖
                p_black_count = _get_p_black_count(img, _w, _h)
                if p_black_count >= 2:
                    img.putpixel((_w, _h), (0, 0, 0))
                else:
                    img.putpixel((_w, _h), (255, 255, 255))

    # img.show()
    return img

img = Image.open(r'CaptchaImage.aspx.jpg')
#img = convert_Image(img)
img = _remove_pil(img)
img.show()
data = pytesseract.image_to_string(img)
print(data)