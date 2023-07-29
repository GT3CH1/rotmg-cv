import cv2
import pathlib
import numpy as np
from .const import CV2_METHOD, CONFIDENCE

ROTMG_CV_PATH = pathlib.Path(__file__).parent.absolute()

def scan_image(path):

    ss = cv2.imread(str(path))

    height = ss.shape[0]
    width = ss.shape[1]

    print(width, height)


    # crop image so that the last 30% horizontally and the middle 20% vertically are used
    ss_cropped = ss[540:640, 1550:1910]
    # ss_cropped = ss

    items = list(pathlib.Path(f"{ROTMG_CV_PATH}/items").glob("*.png"))
    found_items = []
    for _item in items:
        item = cv2.imread(str(_item))
        res = cv2.matchTemplate(ss_cropped, item, eval(CV2_METHOD))
        loc = np.where(res >= CONFIDENCE)
        if not np.any(loc):
            continue
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
        (startX, startY) = maxLoc
        endX = startX + item.shape[1]
        endY = startY + item.shape[0]
        cv2.rectangle(ss_cropped, (startX, startY), (endX, endY), (255, 0, 0), 3)
        found_items.append(f"{str(_item.stem)}")

    found_items.sort()
    print(found_items)
    return found_items

