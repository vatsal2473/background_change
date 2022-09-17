from PIL import Image, ImageFilter, ImageOps

def add_background():

    original_path = "input/segmented/transparent.png"
    background_path = "input/backgrounds/light_green.png"
    # background options: yellow, red, light_pink, dark_pink, light_green, blue_green, grey, blue

    original = Image.open(original_path)
    original = original.resize((1440, 3120))
    shadow = original.copy()
    background = Image.open(background_path)

    width, height = shadow.size
    shadow_color = (100, 100, 100)

    for i in range(width):
        for j in range(height):
            current_color = shadow.getpixel((i, j))
            if (current_color[3]!=0):
                shadow.putpixel((i, j), shadow_color)

    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    shadow = shadow.resize((int((width*7)/8), int((height*7)/8)))

    intr = background
    intr.paste(shadow, (300, 150), mask=shadow)
    intr.paste(original, (150, 0), mask=original)

    # intr = intr.save("/content/drive/MyDrive/2.png")

    flowers1 = Image.open("input/clipart/flowers1.png").convert("RGBA")

    result = intr.copy()

    result.paste(flowers1, (1000, -350), mask=flowers1)

    result.save('image.png')