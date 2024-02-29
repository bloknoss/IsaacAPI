import os
from PIL import Image


def image_to_black(image_name, background_color=(0, 0, 0)):
    img = Image.open(f"./images/{image_name}")

    img = img.convert("RGBA")

    img_data = list(img.getdata())

    for i, pixel in enumerate(img_data):

        if pixel[:3] != background_color:
            img_data[i] = (0, 0, 0, 255)

    img.putdata(img_data)

    img.save(f"./silhouette/{image_name}")


for file in os.listdir("./images/"):
    image_to_black(file)
