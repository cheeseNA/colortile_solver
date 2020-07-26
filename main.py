import random
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab, Image


def get_refpoint():
    np_screen_shot = np.array(ImageGrab.grab())
    cv_screen_shot = cv2.cvtColor(np_screen_shot, cv2.COLOR_RGBA2BGR)
    template = cv2.imread('template.png')

    match_res = cv2.matchTemplate(
        cv_screen_shot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_res)

    return max_loc


def get_tiles(x, y):
    tile = np.full((23 + 2, 15 + 2), -1)
    tile[1:-1, 1:-1] = 0

    np_screen_shot = np.array(ImageGrab.grab())
    tileimg = np_screen_shot[y + 136:y + 858:50, x + 110:x + 1234:50]
    Image.fromarray(tileimg).save("tile.png")
    tileimg = tileimg.transpose(1, 0, 2)

    color_list = np.array([
        [191, 109, 41], [37, 110, 246], [187, 189, 189], [93, 200, 61],
        [240, 158, 58], [238, 147, 249], [190, 113, 200], [236, 114, 110],
        [128, 203, 204], [204, 203, 119]
    ])
    for i in range(len(color_list)):
        tp = np.where(
            (tileimg[:, :, 0] == color_list[i][0])
            & (tileimg[:, :, 1] == color_list[i][1])
            & (tileimg[:, :, 2] == color_list[i][2])
        )
        tp = tuple(tp[0] + 1), tuple(tp[1] + 1)
        tile[tp] = i + 1

    return tile


pyautogui.FAILSAFE = True

if __name__ == '__main__':
    pass
