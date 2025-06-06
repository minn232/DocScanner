
img_file = '../inputImg.jpg'
output_path = "../outputImg.jpg"
SELECTED_SIZE = "A4"
# 선택지: "A4", "B4", "A3", "Letter", "Legal"

PAPER_SIZES_MM = {
    "A4": (210, 297),
    "B4": (250, 353),
    "A3": (297, 420),
    "Letter": (216, 279),
    "Legal": (216, 356),
}

DPI = 300
MM_TO_PX = lambda mm: int(mm * DPI / 25.4)  # 1 inch = 25.4 mm

PAPER_SIZES_PX = {
    name: (MM_TO_PX(w_mm), MM_TO_PX(h_mm))
    for name, (w_mm, h_mm) in PAPER_SIZES_MM.items()
}

doc_size = PAPER_SIZES_PX[SELECTED_SIZE]

hint_labels = ["좌상단", "우상단", "좌하단", "우하단"]
hint_radius = 8


points = []
dots = []
canvas = None
img = None
root = None