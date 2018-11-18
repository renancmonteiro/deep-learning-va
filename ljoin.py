import sys
import os
import subprocess

def save_uniques(uniques, source, destination):
  for filename in uniques:
    subprocess.run(['cp', source + filename, destination + filename])

def merge_duplis(duplis, sourceA, sourceB, destination):
  save_uniques(duplis, sourceA, destination)
  for filename in duplis:
    with open(sourceB + filename) as f, open(destination + filename, 'a') as g:
      for l in f:
        if 2 < len(l):
          g.write(l)


def main(sourceA, sourceB, destination):

  a = set()
  b = set()
  for filename in os.listdir(sourceA):
    if filename.endswith('.txt'):
      a.add(filename)

  for filename in os.listdir(sourceB):
    if filename.endswith('.txt'):
      b.add(filename)

  amb = a - b
  bma = b - a
  ab = a & b

  save_uniques(amb, sourceA, destination)
  save_uniques(bma, sourceB, destination)
  merge_duplis(ab, sourceA, sourceB, destination)

if __name__ == "__main__":
  if 3 < len(sys.argv):
    main(sys.argv[1],sys.argv[2], sys.argv[3])
  else:
    print("usage: python3 first/source/folder/path/ second/source/folder/path destination/folder/path/\n")

