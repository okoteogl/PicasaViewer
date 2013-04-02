'''
Created on Mar 30, 2013

@author: olga
'''

from os import listdir
from os.path import isfile, join
from PIL import Image, ImageDraw
import re

picasainiFile = open("C:/Users/olga/Downloads/Annarella/video_frames/.picasa.ini")
mypath = "C:/Users/olga/Downloads/Annarella/video_frames/"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".png" or ".jpg" or "jpeg")]
# print onlyfiles

p1 = re.compile("\_[0-9]*\.")
p2 = re.compile("\([0-9a-z]+\)")
p3 = re.compile("\,[0-9a-z]+[\;|\n]")
line_number = 1
for line in picasainiFile:
  
  if line_number == 1:
    line_number = 2
    filename = str(line[1:len(line) - 2])
    print filename
    continue
#     list_of_frame_numbers = p1.findall(line)
#     if list_of_frame_numbers:
#       frame_number = str(list_of_frame_numbers.pop())
#       frame_number = int(frame_number[1:len(frame_number) - 1])
#       print "Frame number: ", frame_number
    
      
  if line_number == 2:
    line_number = 3    
    list_of_identities = p3.findall(line)
    if list_of_identities:
      print "identities"
      for i in range(0, len(list_of_identities)):
        identities = str(list_of_identities.pop())
        identities = identities[1:len(identities) - 1]
        print identities  # , float.fromhex(identities[0:4])
    
      frame = Image.open(mypath + filename)
      width, height = frame.size
      list_of_bounding_boxes = p2.findall(line)
      if list_of_bounding_boxes:
        print "bounding boxes:"
        for i in range(0, len(list_of_bounding_boxes)):
          bounding_box = str(list_of_bounding_boxes.pop())
          bounding_box = bounding_box[1:len(bounding_box) - 1]
          print bounding_box
          coords = []
          for i in range(0, 4):
            coords.append(float(int(bounding_box[i * 4:(i + 1) * 4], 16)) / 65535)
            print int(bounding_box[i * 4:(i + 1) * 4 ], 16)
          coords[0] = coords[0] * width
          coords[2] = coords[2] * width
          coords[1] = coords[1] * height
          coords[3] = coords[3] * height
          print coords
      draw = ImageDraw.Draw(frame)
      draw.rectangle((coords[0], coords[1], coords[2], coords[3]), fill=None, outline="red")
      frame.show()
    continue      
        
  if line_number == 3:
    line_number = 1
    continue

        
        
        
        
    
