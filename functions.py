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
        canvas.create_oval(x - r, y - r, x + r, y + r, outline='red', width=2, tags="hint")
        canvas.create_text(x, y - 12, text=label, fill='red', font=("Arial", 10, "bold"), tags="hint")

def get_on_click(callback):
    def on_click(event):
        canvas = config.canvas
        x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)

        if event.num == 1:
            if len(config.points) < 4:
                config.points.append([x, y])
                dot = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')
                config.dots.append(dot)
                canvas.delete("hint")
                if len(config.points) < 4:
                    draw_hint()
                elif len(config.points) == 4:
                    result = apply_homography()
                    callback(result)  
                    
        elif event.num == 3:
            if config.points:
                config.points.pop()
                last_dot = config.dots.pop()
                canvas.delete(last_dot)
                draw_hint()
    return on_click

def apply_homography():
    pts_src = np.array(config.points, dtype=np.float32)
    pts_dst = np.array([
        [0, 0],
        [config.doc_size[0], 0],
        [0, config.doc_size[1]],
        [config.doc_size[0], config.doc_size[1]]
    ], dtype=np.float32)

    H, _ = cv.findHomography(pts_src, pts_dst)
    img_rectified = cv.warpPerspective(config.img, H, config.doc_size)
    return postprocess_white_bg(img_rectified)


def postprocess_white_bg(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.medianBlur(gray, 3)
    
    binary = cv.adaptiveThreshold(
        blurred,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        35, 10
    )

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    cleaned = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

    return cv.cvtColor(cleaned, cv.COLOR_GRAY2BGR)