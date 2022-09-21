from PIL import Image, ImageFilter, ImageOps
import os

def add_background_with_shadow():

    backgrounds = os.listdir('input/backgrounds/')
    
    for i in range(len(backgrounds)):

        original_path = "input/segmented/transparent.png"
        bg_path = 'input/backgrounds/'+backgrounds[i]
        background_path = bg_path
        # background options: yellow, red, light_pink, dark_pink, light_green, blue_green, grey, blue, wall.jpeg

        original = Image.open(original_path)

        background = Image.open(background_path)
        background = background.resize((1640, 2360))

        bg_w, bg_h = background.size
        obj_w, obj_h = original.size

        # finding real width
        flag = 0
        for i in range(obj_w):
            for j in range(obj_h):
                current_color = original.getpixel((i, j))
                if (current_color[3]!=0 and flag==0):
                    flag=1
                    start_w = i
                if (current_color[3]!=0):
                    end_w = i
        real_w = end_w - start_w

        # finding real height
        flg = 0
        for j in range(obj_h):
            for i in range(obj_w):
                current_color = original.getpixel((i, j))
            if (current_color[3]!=0 and flg==0):
                flg=1
                start_h = j
            if (current_color[3]!=0):
                end_h = j
        real_h = end_h - start_h

        obj_w = real_w
        obj_h = real_h

        w_inner = (bg_w*14)/16
        h_inner = (bg_w*6)/8

        if obj_w > w_inner and obj_h > h_inner:
            if (obj_w-w_inner > obj_h-h_inner and obj_w > obj_h):
                original = original.resize((int(original.size[0]*(w_inner/obj_w)), int(original.size[1]*(w_inner/obj_w))))
            elif (obj_w-w_inner < obj_h-h_inner and obj_w < obj_h):
                original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))
            elif (obj_w-w_inner == obj_h-h_inner):
                original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))
        elif obj_w > w_inner:
            original = original.resize((int(original.size[0]*(w_inner/obj_w)), int(original.size[1]*(w_inner/obj_w))))
        elif obj_h > h_inner:
            original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))


        shadow = original.copy()
        width, height = shadow.size
        shadow_color = (100, 100, 100)

        for i in range(width):
            for j in range(height):
                current_color = shadow.getpixel((i, j))
                if (current_color[3]!=0):
                    shadow.putpixel((i, j), shadow_color)

        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
        shadow = shadow.resize((int((width*7)/8), int((height*7)/8)))

        intr = background
        obj_w, obj_h = original.size
        dist_from_below = background.size[1] - 2000
        img_offset = (((bg_w - obj_w) // 2, dist_from_below))
        shadow_offset = ((((bg_w - obj_w) // 2) + 150, dist_from_below + 125))
        intr.paste(shadow, shadow_offset, mask=shadow)
        intr.paste(original, img_offset, mask=original)
        result = intr.copy()

        #display(result)

        name = 'image_ws' + backgrounds[i]
        result.save(name)

def add_background_without_shadow():

    backgrounds = os.listdir('input/backgrounds/')
    
    for i in range(len(backgrounds)):
    

        original_path = "input/segmented/transparent.png"
        bg_path = 'input/backgrounds/'+backgrounds[i]
        background_path = bg_path
        # bg1.jpeg, bg3.jpeg, 33.png

        original = Image.open(original_path)

        background = Image.open(background_path)
        background = background.resize((1640, 2360))

        bg_w, bg_h = background.size
        obj_w, obj_h = original.size

        # finding real width
        flag = 0
        for i in range(obj_w):
            for j in range(obj_h):
                current_color = original.getpixel((i, j))
                if (current_color[3]!=0 and flag==0):
                    flag=1
                    start_w = i
                if (current_color[3]!=0):
                    end_w = i
        real_w = end_w - start_w

        # finding real height
        flg = 0
        for j in range(obj_h):
            for i in range(obj_w):
                current_color = original.getpixel((i, j))
                if (current_color[3]!=0 and flg==0):
                    flg=1
                    start_h = j
                if (current_color[3]!=0):
                    end_h = j
        real_h = end_h - start_h

        obj_w = real_w
        obj_h = real_h

        w_inner = (bg_w*12)/16
        h_inner = (bg_w*6)/8

        if obj_w > w_inner and obj_h > h_inner:
            if (obj_w-w_inner > obj_h-h_inner and obj_w > obj_h):
                original = original.resize((int(original.size[0]*(w_inner/obj_w)), int(original.size[1]*(w_inner/obj_w))))
            elif (obj_w-w_inner < obj_h-h_inner and obj_w < obj_h):
                original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))
            elif (obj_w-w_inner == obj_h-h_inner):
                original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))
        elif obj_w > w_inner:
            original = original.resize((int(original.size[0]*(w_inner/obj_w)), int(original.size[1]*(w_inner/obj_w))))
        elif obj_h > h_inner:
            original = original.resize((int(original.size[0]*(h_inner/obj_h)), int(original.size[1]*(h_inner/obj_h))))

        intr = background
        obj_w, obj_h = original.size
        dist_from_below = background.size[1] - 1830
        img_offset = (((bg_w - obj_w) // 2, dist_from_below))
        intr.paste(original, img_offset, mask=original)
        result = intr.copy()

        name = 'image_ns' + backgrounds[i]
        result.save(name)