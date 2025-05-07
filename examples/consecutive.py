import argparse
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scraping # import ../scraping.py

# Script to downnload images with consecutive numbers in the name

# Usage: python3 consecutive.py -b <base> -p <page-range> [-e <ext> -s <step> -d <digits> -D <directory>]

# Examples:
# python3 consecutive.py -b https://esquire.blob.core.windows.net/esquire20010201thumbnails/Spreads/0x600/ -p 37 40
# python3 consecutive.py -b https://esquire.blob.core.windows.net/esquire20010201thumbnails/Spreads/0x600/ -p 1 9
# python3 consecutive.py -b https://esquire.blob.core.windows.net/esquire20010201thumbnails/Spreads/0x600/ -p 1 99 --no-fill

# Parse arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-b", help="common base of the files", required=True, metavar="BASE")
parser.add_argument("-p", help="pages", nargs=2, required=True, metavar=("FIRST", "LAST"))
parser.add_argument("-e", help="file extension", default=".jpg", metavar="EXT")
parser.add_argument("-s", help="step", default=1, type=int, metavar="STEP")
parser.add_argument("-d", help="digits (Default: len of last page)", metavar="DIGITS")
parser.add_argument("-D", help="Directory", default=".", metavar="DIR")
parser.add_argument("--no-fill", help="Don't fill, (8, 9, 10) instead of (08, 09, 10)", action="store_true")
parser.add_argument("--use-num", help="Use numbers FILLED as final titles", action="store_true")

config = vars(parser.parse_args())
base_url = config["b"]
ext = config["e"]
pages = config["p"]
first = int(pages[0])
last = int(pages[1])
if(config["d"] == None):
    digits = len(pages[1])
else:
    digits = int(config["d"])
step = int(config["s"])
directory = config["D"]
nofill = config["no_fill"]
usenum = config["use_num"]

# Download files
for i in range(first, last + 1, step):
    ii = str(i)
    if(not nofill):
        ii = ii.zfill(digits)
    url = base_url + ii + ext

    if(usenum):
        filename = ii.zfill(digits) + ext
    else:
        filename = url.split("/")[-1]

    scraping.download_image(url, directory + "/" + filename)
