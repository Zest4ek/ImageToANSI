from PIL import Image
import os, sys
import tkinter as tk
from tkinter import filedialog

# import .ansi file
def _import():
    os.system("cls||clear")

    print("\033[38;5;10mSelect .ansi file.\033[0m")    
    file_path = filedialog.askopenfilename(title="Select .ansi file",
                                           filetypes=[("ANSI file", "*.ansi")])
    if file_path: 
        os.system("cls||clear")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            lines = content.split("|")
            if not set(content).issubset(set("0123456789,|")): # .ansi file can contain ONLY these characters
                return "\033[38;5;1mYou opened a file, which not supported by the program.\033[0m"

            for line in lines:
                ansi = line.split(",")
                for i in range(len(ansi)):
                    ansi[i] = f"\033[38;5;{ansi[i]}m██"
                print("".join(ansi))
            
            return ""
    else: 
        return "\033[38;5;1mFile not selected.\033[0m"
    
# export an image file
def _export():
    print(_compress())
    if check:
        img = Image.open("compressed_image.png").convert("RGB")
        img_col = img.load()
        os.remove("compressed_image.png") # delete this image

        name = input("\033[38;5;11mEnter file name:\033[0m\n>>> ")
        ansi = []

        for y in range(img.height):
            for x in range(img.width):
                r,g,b = img_col[x,y]
                r,g,b = min(5,int(r/26*6)),min(5,int(g/256*6)),min(5,int(b/256*6))
                index = 16+36*r+6*g+b
                ansi.append(f"{index},")
                ansi[-1] = ansi[-1]
            ansi.append("|")

        with open(f"Saves/{name}.ansi", "w", encoding="utf-8") as file:
            file.write("".join(ansi)[:-1])

        os.system("cls||clear")
        print("\033[38;5;11mANSI-file was created in the Saves folder.\n"+
            "To output this file use \033[38;5;10m.import \033[38;5;11mcommand.\n"+
            "Press \033[38;5;10m[Enter] \033[38;5;11mto continue.\033[0m")

# console output
def _print():
    print(_compress())
    if check:
        os.system("cls||clear")
        img = Image.open("compressed_image.png").convert("RGB")
        img_col = img.load()
        os.remove("compressed_image.png") # delete this image

        for y in range(img.height):
            row = []
            for x in range(img.width):
                r,g,b = img_col[x,y]
                r,g,b = min(5,int(r/256*6)),min(5,int(g/256*6)),min(5,int(b/256*6))
                index = 16+36*r+6*g+b

                row.append(f"\033[38;5;{index}m██")
            print("".join(row))

# compress image
def _compress():
    global check
    os.system("cls||clear")
    check = False

    print("\033[38;5;10mSelect an image.\033[0m")    
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=(("Image file", "*.png *.jpg *.jpeg *.ico *.gif"), 
                                                      ("Another image file", "*.*")))
    if file_path: 
        try:
            img = Image.open(file_path)
        except Exception:
            return "\033[38;5;1mYou opened a file, which not supported by the program.\033[0m"
    else: 
        return "\033[38;5;1mFile not selected.\033[0m"
    
    os.system("cls||clear")
    inp = ""
    inp = input(f"\033[38;5;11mTimes to compress the image [min: 1]\n\033[38;5;7m(press \033[38;5;10m[Enter] \033[38;5;7mto set to auto)\033[0m\n>>> ")

    if not inp.isdigit():
        if inp == "":
            # set to auto
            screen_width = win.winfo_screenwidth()
            if img.width > img.height:
                compress_num = (img.width / screen_width)*20
            else: 
                compress_num = (img.height / screen_width)*20
        else:
            return "\033[38;5;1mIncorrect input.\033[0m"
    else:
        # set to custom
        compress_num = int(inp)
        if not 0 < int(compress_num):
            return "\033[38;5;1mIncorrect input.\033[0m"
        
    try:
        # create a compressed image
        os.system("cls||clear")
        x = int(img.width / compress_num)
        y = int(img.height / compress_num)
        resized_img = img.resize((x, y), Image.Resampling.LANCZOS)
        os.system(f"mode con: cols={int(img.width/compress_num*2)} lines={int(img.height/compress_num)}") 
        resized_img.save("compressed_image.png", optimize=True, compress_level=0)
    except Exception:
        return "\033[38;5;1mError: The image is too small or the compression ratio is too high.\033[0m"
    
    check = True
    return "\033[38;5;10mImage was successfully compressed!"

# main function
def main():
    os.system("cls||clear")
    os.system("title ImageToANSI 1.0")
    os.system(f"mode con: cols=120 lines=30")
    
    print("\033[38;5;3m# \033[38;5;11mImage to ANSI by Zest4ek\033[0m\n", 
          "\033[38;5;10m.print\033[0m   :: print an image into console\n",
          "\033[38;5;10m.import\033[0m  :: import .ansi image into console\n",
          "\033[38;5;10m.export\033[0m  :: export an image to .ansi\n",
          "\033[38;5;9m.exit\033[0m    :: exit the program.")
    
    inp = input(">>> ")
    if inp == ".print":
        _print()
        input()
    elif inp == ".import":
        print(_import())
        input()
    elif inp == ".export":
        _export()
        input()
    elif inp == ".exit":
        sys.exit()

# tkinter settings
win = tk.Tk()
win.withdraw()
win.attributes('-topmost', True)

while True:
    main()
