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


pyautogui.FAILSAFE = True

if __name__ == '__main__':
    pass
