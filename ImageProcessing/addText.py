from PIL import Image, ImageDraw, ImageFont

defaultFont = ImageFont.truetype("C:\Windows\Fonts\msyh.ttc", 48)


def add_text_to_image(image, text, font=defaultFont,color='black'):
    rgba_image = image.convert('RGBA')
    # 生成白底的图片
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    print(rgba_image)
    # 设置文本文字位置
    text_xy = ((rgba_image.size[0] - text_size_x) / 2, rgba_image.size[1] - text_size_y - 50)
    # 设置文本的颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=color)
    # 合成
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text


before = Image.open("1.jpg")
# before.show()
after = add_text_to_image(before, "不，你不想")
after.show()
