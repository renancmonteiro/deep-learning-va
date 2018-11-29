import sys
import cv2
import pickle as pkl
import random
import glob
import os.path
from sets import Set


def main(pathLabels):
    if not pathLabels.endswith('/'):
        pathLabels += '/'
    classes = Set()
    for filename in glob.glob(pathLabels + '*.txt'):

        with open(filename, 'r') as file: 
           for line in file.readlines():
                props = line.split(' ')

                label = props[0]
                classes.add(label)
    print(classes)
if __name__ == "__main__":
  if 1 < len(sys.argv):
    main(sys.argv[1])
  else:
    print("usage: python3 source/labels/path/\n")
