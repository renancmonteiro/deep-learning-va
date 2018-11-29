import sys
import cv2
import pickle as pkl
import random
import glob
import os.path

def main(pathImage, pathLabel):
    if not pathImage.endswith('/'):
        pathImage += '/'

    if not pathLabel.endswith('/'):
        pathLabel += '/'

    colors = pkl.load(open("./pallete", "rb"))

    for filename in glob.glob(pathImage + '*.png'):
        print(filename)

        labelFile = filename.split('\\')[-1].split('.png')[0]

        imageName = filename.split('\\')[-1]

        labelFile = labelFile + '.txt'

        with open(pathLabel + labelFile, 'r') as file: 
            for line in file.readlines():
                props = line.split(' ')

                label = props[0]
                x = int(props[1])
                y = int(props[2])
                width = int(props[3])
                height = int(props[4])

                xmin = x
                ymin = y
                xmax = x+width
                ymax = y+height

                if(os.path.isfile(imageName)):
                    img = cv2.imread(imageName)
                else:
                    img = cv2.imread(filename)

                color = random.choice(colors)

                t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]

                cv2.putText(img, label, (xmin, ymax + t_size[1]), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);

                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)

                cv2.imwrite(imageName, img)

if __name__ == "__main__":
  if 2 < len(sys.argv):
    main(sys.argv[1], sys.argv[2])
  else:
    print("usage: python3 source/images/path/ source/label/path\n")