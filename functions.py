# functions.py
import numpy as np
import cv2 as cv
import config

def draw_hint():
    canvas = config.canvas
    img = config.img
    canvas.delete("hint")
    if len(config.points) < 4:
        w, h = img.shape[1], img.shape[0]
        positions = [
            (30, 30),
            (w - 30, 30),
            (30, h - 30),
            (w - 30, h - 30),
        ]
        x, y = positions[len(config.points)]
        label = config.hint_labels[len(config.points)]
        r = config.hint_radius
        canvas.create_oval(x - r, y - r, x + r, y + r, outline='green', width=2, tags="hint")
        canvas.create_text(x, y - 12, text=label, fill='green', font=("Arial", 10, "bold"), tags="hint")

def on_click(event):
    canvas = config.canvas
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)

    if event.num == 1:  # 좌클릭
        if len(config.points) < 4:
            config.points.append([x, y])
            dot = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')
            config.dots.append(dot)
            canvas.delete("hint")
            if len(config.points) < 4:
                draw_hint()
            elif len(config.points) == 4:
                apply_homography()

    elif event.num == 3:  # 우클릭
        if config.points:
            config.points.pop()
            last_dot = config.dots.pop()
            canvas.delete(last_dot)
            draw_hint()

def apply_homography():
    pts_src = np.array(config.points, dtype=np.float32)
    pts_dst = np.array([
        [0, 0],
        [config.card_size[0], 0],
        [0, config.card_size[1]],
        [config.card_size[0], config.card_size[1]]
    ], dtype=np.float32)

    H, _ = cv.findHomography(pts_src, pts_dst)
    img_rectified = cv.warpPerspective(config.img, H, config.card_size)

    cv.imwrite(config.output_path, img_rectified)
    print(f"저장 완료: {config.output_path}")

    config.root.destroy()
