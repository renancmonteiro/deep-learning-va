import sys
import os
import json

def convert(bboxVis, imgW, imgH, nw = 1242, nh = 375):
  x, y, w, h = bboxVis
  if imgW	!= nw:
    wpercent = (nw /float(imgW))
    y = y * wpercent
    w = w * wpercent
    x = x * wpercent
    h = h * wpercent
    imgW = imgW * wpercent
    imgH = imgH * wpercent

  # top area
  ho2 = imgH / 2
  srow = int(ho2 - nh / 2)
  erow = srow + nh
  
  yph = y + h
  h = 0
  if y <= srow and yph > srow:
    h = nh if yph >= erow else yph - srow if yph >= srow else 0
    y = 0
  elif y < erow:
    h = erow - y
    y = y - srow
  else:
    x = y = w = h = 0
  return [int(x), int(y), int(w), int(h)]

def main(source, destination):
  for filename in os.listdir(source):
    if filename.endswith(".json"):
      with open(source + filename) as f, open(destination + filename[:-4] + 'txt', 'w') as g:
        data = json.loads(f.read())
        imgW = data.get('imgWidth')
        imgH = data.get('imgHeight')
        for obj in data.get('objects'):
          bboxVis = obj.get('bboxVis')
          if 'ignore' != obj.get('label') and 2 < bboxVis[2] and 2 < bboxVis[3]:
            x, y, w, h = convert(bboxVis, imgW, imgH, nw = 1242, nh = 375)
            if 4 < w and 4 < h:
              g.write('person %d %d %d %d\n' % (x, y, w, h))

if __name__ == "__main__":
  if 2 < len(sys.argv):
    main(sys.argv[1],sys.argv[2])
  else:
    print("usage: python3 source/folder/path/ destination/folder/path/\n")