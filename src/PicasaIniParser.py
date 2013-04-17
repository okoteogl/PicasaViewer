'''
Created on Mar 30, 2013

@author: olga
'''

import ImageViewer
from PIL import Image 
import re, sys, os

def appendInTags(frame, identity, coords):
  global myPicasaIniTags
  if frame in myPicasaIniTags:
    myPicasaIniTags[frame].append((identity, coords))
  else:
    myPicasaIniTags[frame] = [(identity, coords)]


def readPicasaIniFile(mypath, picasainiFile):
  
  picasainiFile = open(picasainiFile)
  
  p2 = re.compile("\(\w+\)")  # find rectangles 
  p3 = re.compile("\,\w+[\;|\n]")  # find identities
  contacts = re.compile("Contacts")
  line_number = 1
  global myPicasaIniTags
  myPicasaIniTags = {}
  for line in picasainiFile:
    print line_number
    # skip Contacts
    if contacts.findall(line) or re.compile(";;").findall(line):
      continue
    if line_number == 1:
      line_number = 2
      filename = str(line[1:-2])
      continue
    
      
    if line_number == 2:
      line_number = 3    
      list_of_identities = p3.findall(line)
      list_of_bounding_boxes = p2.findall(line)
      if list_of_identities:
        for i in range(0, len(list_of_identities)):
          identity = str(list_of_identities[i])
          identity = identity[1:-1]
    
          frame = Image.open(os.path.join(mypath, filename))
          width, height = frame.size          
          bounding_box = str(list_of_bounding_boxes[i])
          bounding_box = bounding_box[1:-1]
          while len(bounding_box) < 16:
            bounding_box = '0' + bounding_box
          coords = []
          for i in range(0, 4):
            coords.append(float(int(bounding_box[i * 4:(i + 1) * 4], 16)) / 65535)
          coords[0] = coords[0] * width
          coords[2] = coords[2] * width
          coords[1] = coords[1] * height
          coords[3] = coords[3] * height
          appendInTags(filename, identity, coords)
        continue      
        
    if line_number == 3:
      line_number = 1
      
  return myPicasaIniTags


def main():
  myTags = readPicasaIniFile(sys.argv[2], sys.argv[1])
  ImageViewer.runViewer(sys.argv[2], myTags)

if __name__ == '__main__':
  main()
  
        
        
    
