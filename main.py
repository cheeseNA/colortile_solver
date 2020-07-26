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


def click_start(x, y):
    pyautogui.click(x / 2 + 300, y / 2 + 250)
    pyautogui.moveTo(10, 10, 1)


def get_tiles(x, y):
    tile = np.full((23 + 2, 15 + 2), -1)
    tile[1:-1, 1:-1] = 0

    np_screen_shot = np.array(ImageGrab.grab())
    tileimg = np_screen_shot[y + 136:y + 858:50, x + 110:x + 1234:50]
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


def solve(x, y, tile):
    end_flag = False
    while not end_flag:
        end_flag = True
        il = range(1, 23)
        jl = range(1, 15)
        if random.random() < 0.5:
            il = il[::-1]
        if random.random() < 0.5:
            jl = jl[::-1]

        for i in il:
            for j in jl:
                if tile[i, j] == 0:
                    cros = np.zeros(4)
                    klist = [0, 0, 0, 0]
                    for k in range(25):
                        if tile[i - k, j] != 0:
                            cros[0] = tile[i - k, j]
                            klist[0] = (i - k, j)
                            break
                    for k in range(25):
                        if tile[i + k, j] != 0:
                            cros[1] = tile[i + k, j]
                            klist[1] = (i + k, j)
                            break
                    for k in range(25):
                        if tile[i, j - k] != 0:
                            cros[2] = tile[i, j - k]
                            klist[2] = (i, j - k)
                            break
                    for k in range(25):
                        if tile[i, j + k] != 0:
                            cros[3] = tile[i, j + k]
                            klist[3] = (i, j + k)
                            break
                    dupl = [x for x in range(1, 11) if np.sum(cros == x) >= 2]
                    if len(dupl) >= 1:
                        pyautogui.click(
                            x / 2 + 55 + (i - 1) * 25,
                            y / 2 + 67 + (j - 1) * 25, interval=0.3
                        )
                        for i in range(4):
                            if cros[i] in dupl:
                                tile[klist[i][0], klist[i][1]] = 0
                        end_flag = False


if __name__ == '__main__':
    pyautogui.FAILSAFE = True
    x, y = get_refpoint()
    click_start(x, y)
    tile = get_tiles(x, y)
    solve(x, y, tile)
