from PIL import Image
import os, sys
import tkinter as tk
from tkinter import filedialog


def ansi216_convert():
    os.system("cls||clear")
    win = tk.Tk()
    win.withdraw()
    win.attributes('-topmost', True)

    print("\033[38;5;10mSelect an image.\033[0m")    
    file_path = filedialog.askopenfilename(title="Select an image",filetypes=(("Image file", "*.png *.jpg *.jpeg"), ("Another image file", "*.*")))

    if file_path: 
        try:
            img = Image.open(file_path)
        except Exception:
            print("\033[38;5;1mYou opened a format, which not supported by the program. Try convert it into a .png or .jpg format.\033[0m")
            return
    else: 
        print("\033[38;5;1mFile not selected.\033[0m")
        return

    inp = input(f"\033[38;5;11mTimes to compress the image: \033[38;5;7m(min: 1);\n(press \033[38;5;10m[Enter] \033[38;5;7mto set to auto)\033[0m\n>>> ")
    if not inp.isdigit():
        if inp == "":
            compress_num = 32
        else:
            print("\033[38;5;1mIncorrect input.\033[0m")
            return
    else:
        compress_num = inp

    if not 0 < int(compress_num):
        print("\033[38;5;1mIncorrect input.\033[0m")
        return

    try:
        os.system(f"mode con: cols={int(img.width/int(compress_num)*2)} lines={int(img.height/int(compress_num))}")
        x = img.width // int(compress_num)
        y = img.height // int(compress_num)
        resized_img = img.resize((x, y), Image.Resampling.LANCZOS)
        resized_img.save("compressed_image.png", optimize=True, compress_level=0)
        img = Image.open("compressed_image.png").convert("RGB")
        img_col = img.load()
        os.system("cls||clear") 
    except Exception:
        print("\033[38;5;1mError: The image is too small or the compression ratio is too high.\033[0m")
        return

    for y in range(img.height):
        row = []
        for x in range(img.width):
            r,g,b = img_col[x,y]
            r,g,b = min(5,int(r/256*6)),min(5,int(g/256*6)),min(5,int(b/256*6))
            index = 16+36*r+6*g+b

            row.append(f"\033[38;5;{index}m██")
        print("".join(row))
    print("\033[0m")

    os.remove("compressed_image.png")
    input()
    main()


def main():
    os.system("cls||clear")
    os.system("title ImageToANSI")
    os.system(f"mode con: cols=120 lines=30")
    print("\033[38;5;3m# \033[38;5;11mImage to ANSI by Zest4ek\033[0m\n")
    print("\033[38;5;10m#convert\033[0m - convert image to 216-palette ANSI.")
    print("\033[38;5;9m#exit\033[0m - exit the program.")

    inp = input(">>> ")
    if inp == "#convert":
        ansi216_convert()
    elif inp == "#exit":
        sys.exit()
    else:
        main()


main()