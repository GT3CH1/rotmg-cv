import cv2
import pathlib
import numpy as np
from const import CV2_METHOD, CONFIDENCE

ROTMG_CV_PATH = pathlib.Path(__file__).parent.absolute()


def find_items(confidence=CONFIDENCE, ss_cropped=None):
    print(f"Confidence: {confidence}")
    path = pathlib.Path(f"{ROTMG_CV_PATH}/items")
    print(path)
    items = list(path.glob("*.png"))
    found_items = []
    for _item in items:
        item = cv2.imread(str(_item), cv2.IMREAD_COLOR)
        res = cv2.matchTemplate(ss_cropped, item, 5)
        loc = np.where(res >= confidence)
        if not np.any(loc):
            continue
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
        (startX, startY) = maxLoc
        endX = startX + item.shape[1]
        endY = startY + item.shape[0]
        cv2.rectangle(ss_cropped, (startX, startY), (endX, endY), (255, 0, 0), 3)
        found_items.append(f"{str(_item.stem)}")
    found_items.sort()
    return found_items

def scan_image(path, show=False):
    ss = cv2.imread(str(path), cv2.IMREAD_COLOR)
    height = ss.shape[0]
    width = ss.shape[1]

    print(width, height)
    # crop image so that the last 30% horizontally and the middle 20% vertically are used
    ss_cropped = ss[530:660, 1550:1910]
    #ss_cropped = ss
    confidence = 0.9
    print(ss_cropped.shape)
    items = set(find_items(confidence, ss_cropped))
    print(items)
    while confidence > 0.80:
        print("No items found")
        confidence -= 0.01
        new_items = set(find_items(confidence, ss_cropped))
        if new_items:
            items = items.union(new_items)
        print(items)
    if(show):
        cv2.imshow("Screenshot", ss_cropped)
        cv2.waitKey(0)
    return items

