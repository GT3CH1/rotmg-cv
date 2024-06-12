import rotmg_cv
import sys
# firt arg is the image file path
# second arg is a boolean to show the image or not

FILE = sys.argv[1]
SHOW = sys.argv[2]

rotmg_cv.scan_image(FILE, show=SHOW)
