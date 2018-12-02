from fromxty import crop_scale, getIgnore, save_anotation
import os
import sys
import json
import glob
import math

def main(labelsFolder, destFolder, fileList):
    if not labelsFolder.endswith('/'):
        labelsFolder += '/'

    if not destFolder.endswith('/'):
        destFolder += '/'

    with open(fileList, 'r') as file: 
        for line in file.readlines():
            props = line.split(' ')

            file = 'tr_kitti_' + props[0].split('.')[0] + '.txt'
            width = int(props[1])
            height = int(props[2])

            print(file + ' ' + str(width) + ' ' +  str(height)) 
            
            if (os.path.isfile(labelsFolder + file) and os.path.getsize(labelsFolder + file) > 0):
                with open(labelsFolder + file, 'r') as f, open(destFolder + file, 'w') as g:
                    for l in f.readlines():
                        ss = l.split(' ')
                        label = ss[0].lower()

                        if not (label in getIgnore()):
                            _x1 = int(ss[4].replace(',', '.').split('.')[0]) # achei alguns arquivos com , no lugar de .
                            _y1 = int(ss[5].replace(',', '.').split('.')[0])
                            _x2 = int(ss[6].replace(',', '.').split('.')[0])
                            _y2 = int(ss[7].replace(',', '.').split('.')[0])

                            _x = min(_x1, _x2)
                            _y = min(_y1, _y2)

                            _w = max(_x1, _x2) - _x
                            _h = max(_y1, _y2) - _y

                            x = _x
                            y = _y
                            w = _w
                            h = _h

                            print(label + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + ' ' + str(h))
                            
                            x, y, w, h = crop_scale(_x, _y, _w, _h, width, height)

                            if 0 < w and 0 < h:
                                save_anotation(g, label, x, y, w, h)
                                

if __name__ == "__main__":
  if 3 < len(sys.argv):
    main(sys.argv[1], sys.argv[2], sys.argv[3].lower())
  else:
    print("usage: python3 source/folder/path/ destination/folder/path/ fileImageList\n")
