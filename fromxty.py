import os
import sys
import json
import math

persons = ['sitting_person', 'pedestrian', 'biker', 'rider']
ignore = ['ignore', 'dontcare', 'misc', 'traffic_light', 'trafficlight']
labels = {"person": 0, "bicycle": 1, "car": 2, "motorbike": 3, "bus": 4, "truck": 5, "greentrafficlight": 6, "redtrafficlight": 7, "offtrafficlight": 8 }

def get_label(l):
  return labels.get(l)

def getIgnore():
  return ignore

def crop_scale(x, y, w, h, imgW, imgH, nw = 1242, nh=375):
  if imgW != nw:
    wpercent = (nw / float(imgW))
    x = math.ceil(x * wpercent)
    y = math.ceil(y * wpercent)
    w = math.ceil(w * wpercent)
    h = math.ceil(h * wpercent)
    imgW = imgW * wpercent
    imgH = imgH * wpercent

  # top area
  ho2 = imgH / 2
  srow = int(ho2 - nh / 2)
  erow = srow + nh
  
  if x + w > imgW:
    w = imgW - x

  yph = y + h
  
  if y <= srow and yph > srow:
    if yph > erow:
      h = nh
    y = 0
  elif srow <= y and y < erow:
    if yph > erow:
      h = erow - y
    y = y - srow
  else:
    return [0.0, 0.0, 0.0, 0.0]

  dw = 1.0 / nw;
  dh = 1.0 / nh;

  # get the center of the bounding box
  x = dw * (x + w / 2);
  y = dh * (y + h / 2);
  w = dw * w;
  h = dh * h;

  return [x, y, w, h]

def save_anotation(g, label, x, y, w, h):  
  if not (label in ignore):
    if label == 'greetrafficlight':
      label = 'greentrafficlight'
    elif label in persons:
      label = 'person'
    elif label == 'yellowtrafficlight':
      label = 'redtrafficlight'
    elif label == 'tram':
      label = 'bus'

    number = get_label(label)
    if number is not None:
      g.write('%d %f %f %f %f\n' % (number, x, y, w, h))


def get_udacity_values(sl, dataset):
  img = ''
  label = ''
  _x = _y = _w = _h = 0

  if 'crowdai' == dataset:
    img = sl[4]
    label = sl[5].lower()
    _x = int(sl[0])
    _y = int(sl[1])
    _w = int(sl[2]) - _x
    _h = int(sl[3]) - _y
  elif 'autti' == dataset:
    img = sl[0]
    _x = int(sl[1])
    _y = int(sl[2])
    _w = int(sl[3]) - _x
    _h = int(sl[4]) - _y
    label = sl[6].lower()
    if 7 < len(sl) and 0 < len(sl[7]):
      prefix = sl[7].lower()
      if prefix.endswith('left'):
        prefix = prefix[0:-4]
      label = prefix + label
    
  return [img, label, _x, _y, _w, _h]

# convert from original Person cityscapes format to yolo format
def fromcs(source, destination, imgW, imgH, nw = 1242, nh = 375):
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
            if 0 < w and 0 < h:
              save_anotation(g, 'person', x, y, w, h)

# convert from kitti to yolo format
def fromk(source, destination, imgW, imgH, _nw = 1242, _nh = 375):
  for filename in os.listdir(source):
    if filename.endswith('.txt'):
      with open(source + filename) as f, open(destination + filename, 'w') as g:
        for l in f:
          ss = l.split(' ')
          label = ss[0].lower()

          if not (label in ignore):
            _x1 = int(ss[4].split('.')[0])
            _y1 = int(ss[5].split('.')[0])
            _x2 = int(ss[6].split('.')[0])
            _y2 = int(ss[7].split('.')[0])
            _x = min(_x1, _x2)
            _y = min(_y1, _y2)
            _w = max(_x1, _x2) - _x
            _h = max(_y1, _y2) - _y
            x = _x
            y = _y
            w = _w
            h = _h
            x, y, w, h = crop_scale(_x, _y, _w, _h, imgW, imgH, nw = _nw, nh = _nh)
            if 0 < w and 0 < h:
              save_anotation(g, label, x, y, w, h)

# convert from udacity to yolo format
def fromu(source, destination, imgWidth, imgHeight, dataset = 'crowdai', _nw = 1242, _nh = 375):
  imgs = {}

  filename = 'labels_crowdai.csv'
  separator = ','
  hasHeader = True
  
  if 'autti' == dataset:
    filename = 'labels.csv'
    separator = ' '
    hasHeader = False
  elif 'crowdai' != dataset:
    print('Invalid dataset name!')
    return
  
  with open(source + filename) as f:
    if hasHeader:
      next(f)
    for l in f:
      ss = l.replace('\n', '').split(separator)
      img, label, _x, _y, _w, _h = get_udacity_values(ss, dataset)

      x = _x
      y = _y
      w = _w
      h = _h
      fstr = ''
      if not (img in imgs):
        imgs[img] = []
      if imgWidth != _nw or imgHeight != _nh:
        x, y, w, h = crop_scale(_x, _y, _w, _h, imgWidth, imgHeight, nw = _nw, nh = _nh)
      if 0 < w and 0 < h:
        fstr = label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
        imgs[img].append(fstr)
  for img in imgs:
    with open(destination + img.replace('.jpg', '.txt'), 'w') as g:
      for s in imgs[img]:
        if 0 < len(s):
          ss = s.split(' ')
          save_anotation(g, ss[0], float(ss[1]), float(ss[2]), float(ss[3]), float(ss[4]))

# convert from the IARA traffic light annotation format (separated files for each class)
def fromi(source, destination, imgWidth, imgHeight, _nw = 1242, _nh = 375):
  imgs = {}
  for filename in os.listdir(source):
    if filename.endswith('.txt') and 6 < len(filename):
      label = filename[0:-4]
      with open(source + filename) as f:
        for l in f:
          sl = l.split(' ')
          img = sl[0]
          _x = int(sl[1])
          _y = int(sl[2])
          _w = int(sl[3]) - _x
          _h = int(sl[4]) - _y

          x, y, w, h = crop_scale(_x, _y, _w, _h, imgWidth, imgHeight, _nw, _nh)
          if 0 < w and 0 < h:
            fstr = label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h)
            if img in imgs:
              imgs[img].append(fstr)
            else:
              imgs[img] = [fstr]
  for img in imgs:
    with open(destination + img.replace('.png', '.txt'), 'w') as g:
      for s in imgs[img]:
        ss = s.split(' ')
        save_anotation(g, ss[0], float(ss[1]), float(ss[2]), float(ss[3]), float(ss[4]))

def main(source, destination, dataset, imgWidth, imgHeight):
  if not source.endswith('/'):
    source += '/'
  if not destination.endswith('/'):
    destination += '/'

  if dataset in ['crowdai', 'autti']:
    fromu(source, destination, imgWidth, imgHeight, dataset)
  elif 'cityscapes' == dataset:
    fromcs(source, destination, imgWidth, imgHeight)
  elif 'kitti' == dataset:
    fromk(source, destination, imgWidth, imgHeight)
  elif 'iara' == dataset:
    fromi(source, destination, imgWidth, imgHeight)
  else:
    print("Invalid dataset name!\n")

if __name__ == "__main__":
  if 5 < len(sys.argv):
    main(sys.argv[1], sys.argv[2], sys.argv[3].lower(), int(sys.argv[4]), int(sys.argv[5]))
  else:
    print("usage: python3 source/folder/path/ destination/folder/path/ dataset imgWidth imgHeight\n")
