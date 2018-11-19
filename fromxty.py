import os
import sys
import json

def crop_scale(x, y, w, h, imgW, imgH, nw = 1272, nh=375):
  if imgW != nw:
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

# convert from original Person cityscapes format to yolo format
def fromcs(source, destination, imgW, imgH, nw = 1272, nh = 375):
  for filename in os.listdir(source):
    if filename.endswith('.json'):
      with open(source + filename) as f, open(destination + filename.replace('.json', '.txt'), 'w') as g:
        data = json.loads(f.read())

        if imgW != data.get('imgWidth'):
          imgW = data.get('imgWidth')
        if imgH != data.get('imgHeight'):
          imgH = data.get('imgHeight')

        for obj in data.get('objects'):
          _x, _y, _w, _h = obj.get('bboxVis')
          if 'ignore' != obj.get('label') and 2 < _w and 2 < _h:
            x, y, w, h = crop_scale(_x, _y, _w, _h, imgW, imgH, nw, nh)
            if 4 < w and 4 < h:
              g.write('person %d %d %d %d\n' % (x, y, w, h))

# convert from kitti to yolo format
def fromk(source, destination, imgW, imgH, _nw = 1272, _nh = 375):
  for filename in os.listdir(source):
    if filename.endswith('.txt'):
      with open(source + filename) as f, open(destination + filename, 'w') as g:
        for l in f:
          ss = l.split(' ')
          label = ss[0].lower()
          if 'dontcare' != label:
            _x = int(ss[4].split('.')[0])
            _y = int(ss[5].split('.')[0])
            _w = int(ss[6].split('.')[0]) - _x
            _h = int(ss[7].split('.')[0]) - _y
            x, y, w, h = crop_scale(_x, _y, _w, _h, imgW, imgH, nw = _nw, nh = _nh)
            if 4 < w and 4 < h:
              g.write(label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')

# convert from udacity to yolo format
def fromu(source, destination, imgWidth, imgHeight, _nw = 1272, _nh = 375):
  imgs = {}
  with open(source + 'labels_crowdai.csv') as f:
    next(f)
    for l in f:
      ss = l.replace('\n', '').split(',')
      img = ss[4].lower()
      label = ss[5].lower()
      _x = int(ss[0])
      _y = int(ss[1])
      _w = int(ss[2]) - _x
      _h = int(ss[3]) - _y
      x, y, w, h = crop_scale(_x, _y, _w, _h, imgWidth, imgHeight, nw = _nw, nh = _nh)
      if 4 < w and 4 < h:
        if 'pedestrian' == label:
          label = 'person'
        fstr = label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
        if img in imgs:
          imgs[img].append(fstr)
        else:
          imgs[img] = [fstr]
  for img in imgs:
    with open(destination + img.replace('.jpg', '.txt'), 'w') as g:
      for s in imgs[img]:
        g.write(s + '\n')

def main(source, destination, dataset, imgWidth, imgHeight):
  if 'udacity' == dataset:
    fromu(source, destination, imgWidth, imgHeight)
  elif 'cityscapes' == dataset:
    fromcs(source, destination, imgWidth, imgHeight)
  elif 'kitti' == dataset or 'iara' == dataset:
    fromk(source, destination, imgWidth, imgHeight)

if __name__ == "__main__":
  if 5 < len(sys.argv):
    main(sys.argv[1], sys.argv[2], sys.argv[3].lower(), int(sys.argv[4]), int(sys.argv[5]))
  else:
    print("usage: python3 source/folder/path/ destination/folder/path/ dataset imgWidth imgHeight\n")