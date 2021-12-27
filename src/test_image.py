
import pytesseract
from PIL import Image
from PIL import ImageEnhance
import cv2
import matplotlib as plot


'''
img = Image.open(r'check.png')
#img.show()
imgry = img.convert('L')
imgry.show()

threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
out = imgry.point(table, '1')

enhancer = ImageEnhance.Contrast(imgry)
image2 = enhancer.enhance(4)
image2.show()

text = pytesseract.image_to_string(image2)  # 將圖片轉成字串
print(text.replace(' ', '').replace('\n', '')) #這裡因為識別出來的文字可能會有空格和回車
'''
'''
text = pytesseract.image_to_string(imgry, lang="chi_tra+eng")
print('辨識結果:' + text)
'''



def _get_p_black_count(self, img: Image, _w: int, _h: int):
    ''' 獲取當前比特置周圍像素點中黑色元素的個數
    Args:
    img (img): 圖像信息
    _w (int): w坐標
    _h (int): h坐標
    Returns:
    int: 個數
    '''
    w, h = img.size
    p_round_items = []

    # 超過了橫縱坐標
    if _w == 0 or _w == w-1 or 0 == _h or _h == h-1:
        return 0

    p_round_items = [img.getpixel((_w, _h-1)), img.getpixel((_w, _h+1)), img.getpixel((_w-1, _h)), img.getpixel((_w+1, _h))]
    p_black_count = 0
    for p_item in p_round_items:
        if p_item == (0, 0, 0):
            p_black_count = p_black_count+1

    return p_black_count

img = Image.open(r'CaptchaImage.aspx.jpg')
#img.show()
# 嘗試去掉紅像素點

w, h = img.size

for _w in range(w):

    for _h in range(h):

        o_pixel = img.getpixel((_w, _h))

        print(o_pixel)
        if o_pixel == (255, 0, 0):

            img.putpixel((_w, _h), (255, 255, 255))

            img.show()
            img_l = img.convert("L")

            img_l.show()

            verify_code1 = pytesseract.image_to_text(img)

            verify_code2 = pytesseract.image_to_text(img_l)

            print(f"verify_code1:{verify_code1}")

            print(f"verify_code2:{verify_code2}")