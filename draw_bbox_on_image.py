import sys
import cv2
import pickle as pkl
import random

def main(path, labels, label):
    if not path.endswith('/'):
        path += '/'

    colors = pkl.load(open("./pallete", "rb"))

    with open(labels, 'r') as file: 
        for line in file.readlines():
            props = line.split(' ')

            image = props[0].split('/')[-1]
            xmin = int(props[1])
            ymin = int(props[2])
            xmax = int(props[3])
            ymax = int(props[4])

            img = cv2.imread(path + image)

            color = random.choice(colors)

            t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]

            cv2.putText(img, label, (xmin, ymax + t_size[1]), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)

            cv2.imwrite(label + '/' + image, img)


if __name__ == "__main__":
  if 3 < len(sys.argv):
    main(sys.argv[1], sys.argv[2], sys.argv[3])
  else:
    print("usage: python3 source/images/path/ label.txt labelclass\n")