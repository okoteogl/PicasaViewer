'''
Created on Apr 2, 2013

@author: olga
'''

from PIL import Image, ImageTk
import Tkinter
import os

def onRightArrowPress(event):
  global filename_index
  filename_index += 1
  event.widget.quit()  # exit mainloop and go to the next image
    
def onLeftArrowPress(event):
  global filename_index
  filename_index -= 1
  event.widget.quit()  # exit mainloop and go to the previous image

def findUniqueIDs(myTags):
  uniqueIDs = []
  for frame in myTags.keys(): 
    for tag in myTags[frame]:
      if tag[0] not in uniqueIDs:
        uniqueIDs.append(tag[0])
  return uniqueIDs
  
def runViewer(mypath, myTags):
  global filename_index
  dirlist = os.listdir(mypath)
  colormap = ["red", "blue", "green", "yellow", "black", "gray", "pale turquoise", "maroon"]

  uniqueIDs = findUniqueIDs(myTags)
  for item in dirlist[:]:
    if not item.endswith("png" or "jpg" or "jpeg"):  # whatever test you need to run goes here
      dirlist.remove(item)
  
  filename_index = 0
  root = Tkinter.Tk()
  frame_temp = Image.open(os.path.join(mypath, dirlist[0]))
  img_width, img_height = frame_temp.size   
  canvas = Tkinter.Canvas(root, width=img_width, height=img_height)
  canvas.pack()
  root.bind("<Right>", onRightArrowPress)
  root.bind("<Left>", onLeftArrowPress)
  root.geometry('+%d+%d' % (100, 100))

  while True:
    try:
      canvas.delete("all")
      image1 = Image.open(os.path.join(mypath, dirlist[filename_index]))
      root.geometry('%dx%d' % (image1.size[0], image1.size[1]))
      
      tkpi = ImageTk.PhotoImage(image1)
      canvas.create_image((img_width / 2, img_height / 2), image=tkpi)     
      root.title(dirlist[filename_index])
      
      if dirlist[filename_index] in myTags:
        for tag in myTags[dirlist[filename_index]]:
          color_index = uniqueIDs.index(tag[0])
          if color_index > len(colormap) - 1:
            print "Insert more colors in colormap list"
            exit(3)
          coords = tag[1]
          canvas.create_rectangle(coords, fill=None, outline=colormap[color_index], width="3.0")     

      root.mainloop()  # wait until user presses an arrow key
    except:
      root.mainloop()
    try:
      Tkinter.Label(root).pack()
    except:
      print "window has been destroyed, break loop"
      break

if __name__ == '__main__':
  runViewer()
