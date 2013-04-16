'''
Created on Mar 30, 2013

@author: olga
'''

import ImageViewer
# from os import listdir
# from os.path import isfile, join
from PIL import Image  # , ImageDraw
import re

def appendInTags(frame, identity, coords):
  global myPicasaIniTags
  if frame in myPicasaIniTags:
    myPicasaIniTags[frame].append((identity, coords))
  else:
    myPicasaIniTags[frame] = [(identity, coords)]
  # print myPicasaIniTags


def readPicasaIniFile():
  
  # ImageViewer2.runViewer("C:/Users/olga/Downloads/Annarella/video_frames")
  global mypath
  picasainiFile = open("C:/Users/olga/Downloads/Annarella/video_frames/.picasa.ini")
  mypath = "C:/Users/olga/Downloads/Annarella/video_frames/"
  # onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".png" or ".jpg" or "jpeg")]
  # print onlyfiles

  # p1 = re.compile("\_[0-9]*\.")
  p2 = re.compile("\([0-9a-z]+\)")
  p3 = re.compile("\,[0-9a-z]+[\;|\n]")
  line_number = 1
  global myPicasaIniTags
  myPicasaIniTags = {}
  for line in picasainiFile:
  
    if line_number == 1:
      # print line_number, line,
      line_number = 2
      filename = str(line[1:-2])
      # print filename
      continue
#     list_of_frame_numbers = p1.findall(line)
#     if list_of_frame_numbers:
#       frame_number = str(list_of_frame_numbers.pop())
#       frame_number = int(frame_number[1:len(frame_number) - 1])
#       print "Frame number: ", frame_number
    
      
    if line_number == 2:
      # print line_number, line,
      line_number = 3    
      list_of_identities = p3.findall(line)
      list_of_bounding_boxes = p2.findall(line)
      if list_of_identities:
        # print "identities"
        for i in range(0, len(list_of_identities)):
          identity = str(list_of_identities[i])
          identity = identity[1:-1]
          # print identity  # , float.fromhex(identities[0:4])
    
          frame = Image.open(mypath + filename)
          width, height = frame.size          
          # if list_of_bounding_boxes:
          # print "bounding boxes:"
            # for j in list_of_bounding_boxes:
         
            
          bounding_box = str(list_of_bounding_boxes[i])
          bounding_box = bounding_box[1:-1]
          while len(bounding_box) < 16:
            bounding_box = '0' + bounding_box
          coords = []
          for i in range(0, 4):
            coords.append(float(int(bounding_box[i * 4:(i + 1) * 4], 16)) / 65535)
            # print int(bounding_box[i * 4:(i + 1) * 4 ], 16)
          coords[0] = coords[0] * width
          coords[2] = coords[2] * width
          coords[1] = coords[1] * height
          coords[3] = coords[3] * height
          # print coords
          appendInTags(filename, identity, coords)
#             draw = ImageDraw.Draw(frame)
#             draw.rectangle((coords[0], coords[1], coords[2], coords[3]), fill=None, outline="red")
#             frame.show()
        continue      
        
    if line_number == 3:
      # print line_number, line
      line_number = 1
      
  return myPicasaIniTags
        
if __name__ == '__main__':
  global mypath
  myTags = readPicasaIniFile()
  print myTags
  ImageViewer.runViewer(mypath, myTags)
        
        
    
