from PIL import Image


def image_to_black(image_path, background_color=(0, 0, 0)):
    img = Image.open(image_path)

    img = img.convert("RGBA")

    img_data = list(img.getdata())

    for i, pixel in enumerate(img_data):

        if pixel[:3] != background_color:

            img_data[i] = (0, 0, 0, 255)

    img.putdata(img_data)

    img.save("./silhouette/test.png")


file = "./images/test.png"
image_to_black(file)
