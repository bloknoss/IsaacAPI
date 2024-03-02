import os
from PIL import Image


def image_to_black(image_name):
    im = Image.open(f"./original/{image_name}")

    image = im.convert("RGBA")
    alpha = image.getchannel("A")
    alphaThresh = alpha.point(lambda p: 255 if p > 200 else 0)

    res = Image.new("RGBA", im.size)

    res.putalpha(alphaThresh)
    res.save(f"./silhouette/{image_name}")


for file in os.listdir("./original/"):
    image_to_black(file)
