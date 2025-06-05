import tkinter as tk
from tkinter import Canvas, Scrollbar
from PIL import Image, ImageTk
import cv2 as cv
import config
import functions

def on_complete(img_rectified):
    cv.imwrite(config.output_path, img_rectified)
    config.root.destroy()

# Tkinter 윈도우 초기화
root = tk.Tk()
root.title("Perspective Correction (Click 4 corners)")
config.root = root

# 이미지 불러오기
img = cv.imread(config.img_file)
config.img = img

img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
photo = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))

# 스크롤 캔버스 구성
canvas = Canvas(root, width=800, height=600, scrollregion=(0, 0, img.shape[1], img.shape[0]))
canvas.pack(side="left", fill="both", expand=True)
config.canvas = canvas

hbar = Scrollbar(root, orient="horizontal", command=canvas.xview)
vbar = Scrollbar(root, orient="vertical", command=canvas.yview)
hbar.pack(side="bottom", fill="x")
vbar.pack(side="right", fill="y")
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# 이벤트 및 이미지 표시
canvas.bind("<Button-1>", functions.get_on_click(on_complete))
canvas.bind("<Button-3>", functions.get_on_click(on_complete))
canvas.create_image(0, 0, anchor="nw", image=photo)

functions.draw_hint()

root.mainloop()
