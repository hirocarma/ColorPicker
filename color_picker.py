import cv2
import os
import sys
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.colors as mcolors
from scipy.spatial import KDTree

# Global variables
drawing = False
ix, iy = -1, -1


def rgb_to_name(rgb):
    css4_colors = mcolors.CSS4_COLORS
    names = list(css4_colors.keys())
    rgb_values = [mcolors.hex2color(css4_colors[name]) for name in names]
    kdtree = KDTree(rgb_values)
    rgb_normalized = tuple([x / 255 for x in rgb])
    distance, index = kdtree.query(rgb_normalized)
    color_name = names[index]
    return f"{color_name}(approx)" if distance != 0 else color_name


def draw_text(image, text, position, font_scale=1, color=(0, 0, 0), thickness=1):
    cv2.putText(
        image,
        text,
        position,
        cv2.FONT_HERSHEY_PLAIN,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA,
    )


def calculate_average_color(image, color_space=cv2.COLOR_BGR2RGB):
    converted_img = cv2.cvtColor(image, color_space)
    return [int(np.mean(converted_img[:, :, i])) for i in range(3)]


def get_color_info_text(
    L_ast, a_ast, b_ast, c_ast, r, g, b, h, s, v, color_name, iy, y, ix, x
):
    return [
        f"Selected Color",
        f"L*a*b* c*: {L_ast} , {a_ast} , {b_ast} , {c_ast}",
        f"RGB: {r} , {g} , {b}",
        f"HSV: {h} , {s} , {v}",
        f"Colorcode: {r:02x}{g:02x}{b:02x}",
        f"Colorname: {color_name}",
        f"Coordinate: {iy}:{y}x{ix}:{x}",
    ]


def calculate_complementary_and_opposite(r, g, b):
    val = int(max([r, g, b])) + int(min([r, g, b]))
    c_rgb = (val - r, val - g, val - b)
    r_rgb = (255 - r, 255 - g, 255 - b)
    return c_rgb, r_rgb


def recimg_overlay(rec_img, rec_pt1, rec_pt2):
    overlay = rec_img.copy()
    cv2.rectangle(
        overlay,
        pt1=rec_pt1,
        pt2=rec_pt2,
        color=(255, 255, 255),
        thickness=-1,
    )
    mat_img = cv2.addWeighted(overlay, 0.4, rec_img, 0.6, 0)
    return mat_img.copy()


def show_pick_window(rec_img, x, y):
    L_ast, a_ast, b_ast = calculate_average_color(rec_img, cv2.COLOR_BGR2Lab)
    c_ast = int(np.sqrt(a_ast**2 + b_ast**2))
    r, g, b = calculate_average_color(rec_img, cv2.COLOR_BGR2RGB)
    h, s, v = calculate_average_color(rec_img, cv2.COLOR_BGR2HSV)
    color_name = rgb_to_name((r, g, b))

    c_rgb, r_rgb = calculate_complementary_and_opposite(r, g, b)

    height, width = rec_img.shape[:2]
    pick_height = max(240, int(height * 1.2))
    pick_width = max(500, int(width * 1.2))
    pick = np.full((pick_height, pick_width, 3), (b, g, r), dtype=np.uint8)
    pick[0:height, 0:width] = rec_img

    color_info = get_color_info_text(
        L_ast, a_ast, b_ast, c_ast, r, g, b, h, s, v, color_name, iy, y, ix, x
    )
    pick = recimg_overlay(pick, (0, 0), (290, 150))

    positions = [(3, i) for i in range(20, 141, 20)]
    for text, pos in zip(color_info, positions):
        draw_text(pick, text, pos)

    rec_pos_x = pick_width - 200
    rec_pos_y = pick_height - 180

    cv2.rectangle(
        pick,
        pt1=(rec_pos_x, rec_pos_y - 20),
        pt2=(pick_width, rec_pos_y + 80),
        color=c_rgb[::-1],
        thickness=-1,
    )
    pick = recimg_overlay(
        pick, (rec_pos_x, rec_pos_y - 20), (pick_width, rec_pos_y + 48)
    )
    draw_text(pick, "Complementary Color", (rec_pos_x, rec_pos_y))
    draw_text(
        pick,
        f"RGB: {c_rgb[0]}, {c_rgb[1]}, {c_rgb[2]}",
        (rec_pos_x, rec_pos_y + 20),
    )
    draw_text(pick, f"HSV: {h}, {s}, {v}", (rec_pos_x, rec_pos_y + 40))

    cv2.rectangle(
        pick,
        pt1=(rec_pos_x, rec_pos_y + 80),
        pt2=(pick_width, pick_height),
        color=r_rgb[::-1],
        thickness=-1,
    )
    pick = recimg_overlay(
        pick, (rec_pos_x, rec_pos_y + 80), (pick_width, rec_pos_y + 148)
    )
    draw_text(pick, "Opposite Color", (rec_pos_x, rec_pos_y + 100))
    draw_text(
        pick,
        f"RGB: {r_rgb[0]}, {r_rgb[1]}, {r_rgb[2]}",
        (rec_pos_x, rec_pos_y + 120),
    )
    draw_text(pick, f"HSV: {h}, {s}, {v}", (rec_pos_x, rec_pos_y + 140))

    cv2.imshow("pick", pick)
    view_img = img.copy()
    if ix == x and iy ==y:
        cv2.circle(view_img, (x, y), 6, (r_rgb[0], r_rgb[1], r_rgb[2]), 1)
    elif not np.array_equal(view_img, rec_img):
        cv2.rectangle(view_img, (ix, iy), (x, y), (0, 0, 255), 1)
    cv2.imshow(basename, view_img)


def printColor(event, x, y, flags, param):
    global ix, iy, drawing
    if event == cv2.EVENT_LBUTTONUP and flags & cv2.EVENT_FLAG_CTRLKEY:
        rec_img = img.copy()
        show_pick_window(rec_img, 0, 0)
    elif event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_SHIFTKEY:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        view_img = img.copy()
        cv2.rectangle(view_img, (ix, iy), (x, y), (0, 0, 255), 1)
        cv2.imshow(basename, view_img)
    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        rec_img = img[iy:y, ix:x]
        show_pick_window(rec_img, x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        ix, iy = x, y
        rec_img = img[y : y + 1, x : x + 1]
        show_pick_window(rec_img, x, y)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py image_file")
        sys.exit(1)

    IMG_FILE = sys.argv[1]
    img = cv2.imread(IMG_FILE)
    basename = os.path.basename(IMG_FILE)
    cv2.namedWindow(basename)
    cv2.setMouseCallback(basename, printColor)
    cv2.imshow(basename, img)

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            cv2.destroyWindow("pick")
            cv2.imshow(basename, img)
        elif key == 27:  # Esc
            break

    cv2.destroyAllWindows()
