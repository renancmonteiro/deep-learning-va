import sys
import os

import PIL
from PIL import Image

def cropscale_image(source_image, nw = 1242, nh = 375):
  img = Image.open(source_image)
  if img.size[0] != nw:
    wpercent = (nw /float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((nw,hsize), PIL.Image.ANTIALIAS)
  if img.size[1] != nh:
    h2 = img.size[1] / 2
    srow = int(h2 - nh / 2)
    img = img.crop((0, srow, img.size[0], srow + nh))
  return img

def main(source, destination):
  if not source.endswith('/'):
    source += '/'
  if not destination.endswith('/'):
    destination += '/'
  for filename in os.listdir(source):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tiff"):
      nimg = cropscale_image(source_image = source + filename, nw = 1242, nh = 375)
      nimg.save(destination + filename)
      nimg.close()

if __name__ == "__main__":
  if 2 < len(sys.argv):
    main(sys.argv[1], sys.argv[2])
  else:
    print("usage: python3 source/folder/path/ destination/folder/path/\n")