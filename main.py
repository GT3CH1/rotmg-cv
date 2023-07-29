import cv2
import pathlib
import numpy as np
ss = cv2.imread("/Users/gcpease/Downloads/image.png")

width_scale = 0.6
height_scale = 0.2

item_w = 77
item_h = 77

height = ss.shape[0]
width = ss.shape[1]

print(width, height)

method = "cv2.TM_CCOEFF_NORMED"

# crop image so that the last 30% horizontally and the middle 20% vertically are used
ss_cropped = ss[540:640, 1550:1910]
# ss_cropped = ss

items = list(pathlib.Path("items").glob("*.png"))
found_items = []
for _item in items:
    item = cv2.imread(str(_item))
    res = cv2.matchTemplate(ss_cropped, item, eval(method))
    loc = np.where(res >= 0.70)
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

cv2.imshow("RotMG Items", ss_cropped)
cv2.waitKey()
# return found_items
