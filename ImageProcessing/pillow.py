from PIL import Image

i = Image.open("1.jpg")
# i.show()
box = (0, 0, 400, 400)
# 切除(0,0)到(400,400)之间的图片
region = i.crop(box)
# 切片旋转180度
region = region.transpose(Image.ROTATE_180)
# 粘回原图像
i.paste(region, box)
i.show()
