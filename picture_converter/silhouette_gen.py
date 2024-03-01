import os
from PIL import Image


def image_to_black(image_name):
    im = Image.open(f"./images/{image_name}")

    image = im.convert("RGBA")
    alpha = image.getchannel("A")
    alphaThresh = alpha.point(lambda p: 255 if p > 200 else 0)

    # Make a new completely black image same size as original
    res = Image.new("RGB", im.size)

    # Copy across the alpha channel from original
    res.putalpha(alphaThresh)
    res.save(f"./silhouette/{image_name}")


for file in os.listdir("./images/"):
   image_to_black(file)
