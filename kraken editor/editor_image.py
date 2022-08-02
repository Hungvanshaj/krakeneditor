import os
from PyQt5.QtWidgets import*

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter, ImageEnhance

app = QApplication([])
win = QWidget()       
win.resize(900, 600) 
win.setWindowTitle('Kraken Editor')
Show_IMG = QLabel("Your Image")
IMG_NOTFOUND = QLabel("File Not Found!")

btn_dir = QPushButton("Folder")
list_img = QListWidget()
btn_editor = QPushButton("Left Your Image")
btn_editor1 = QPushButton("Crop Your Image")
btn_editor2 = QPushButton("B/W Your Image")
btn_editor3 = QPushButton("Blur Your Image")
btn_editor4 = QPushButton("Rotate Your Image")
btn_editor5 = QPushButton("Contrast Your Image")


row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(Show_IMG, 95)
col1.addWidget(list_img)
col1.addWidget(btn_dir)
row_btn = QVBoxLayout()
row_btn.addWidget(btn_editor)
row_btn.addWidget(btn_editor1)
row_btn.addWidget(btn_editor2)
row_btn.addWidget(btn_editor3)
row_btn.addWidget(btn_editor4)
row_btn.addWidget(btn_editor5)
col2.addLayout(row_btn)

row.addLayout(col1)
row.addLayout(col2)
win.setLayout(row)
win.show()

folder = ''
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def choosefolder():
   global folder
   folder = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   choosefolder()
   filenames = filter(os.listdir(folder), extensions)
 
   list_img.clear()
   for filename in filenames:
       list_img.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)

class Editor_IMG():
    def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
       '''When loading, remember the path and file name'''
       self.dir = dir
       self.filename = filename
       image_path = os.path.join(dir, filename)
       self.image = Image.open(image_path)
 
    def showImage(self, path):
       Show_IMG.hide()
       pixmapimage = QPixmap(path)
       w, h = Show_IMG.width(), Show_IMG.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       Show_IMG.setPixmap(pixmapimage)
       Show_IMG.show()
 
workimage = Editor_IMG()
 
def showChosenImage():
   if list_img.currentRow() >= 0:
       filename = list_img.currentItem().text()
       workimage.loadImage(folder, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)
       workimage.showImage(image_path)
 
list_img.currentRowChanged.connect(showChosenImage)

class ImageEditor:
   def __init__(self, filename):
      self.filename = filename
      self.original = None
      self.changed = list()

   
   def open(self):
      try:
         self.original = Image.open(self.filename)
      except:
         print('file not found!')
      self.original.show()


   def do_left(self):
      rotated = self.original.transpose(Image.FLIP_LEFT_RIGHT)
      self.changed.append(rotated)
      rotated.save(f'rotated {len(self.changed)}.png')

   def do_crop(self):
      box = (250, 100, 600, 400) #left, up, right, down
      cropped = self.original.crop(box)
      self.changed.append(cropped)
      cropped.save(f'cropped {len(self.changed)}.png')


   def do_gray(self):
      gray = self.original.convert('L')
      self.changed.append(gray)
      gray.save(f'gray {len(self.changed)}.png')


   def do_blur(self):
      blur = self.original.filter(ImageFilter.BLUR)
      self.changed.append(blur)
      blur.save(f'blur {len(self.changed)}.png')


   def do_up(self):
      up = self.original.transpose(Image.ROTATE_180)
      self.changed.append(up)
      up.save(f'up {len(self.changed)}.png')


   def do_contrast(self):
      contrast = ImageEnhance.Contrast(self.original)
      contrast = contrast.enhance(-100)
      self.changed.append(contrast)
      contrast.save(f'contrast {len(self.changed)}.png')

   def btn_left(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_left()
         for img in MyImage.changed:
            img.show()      

   btn_editor.clicked.connect(btn_left)

   def btn_crop(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_crop()
         for img in MyImage.changed:
            img.show()      

   btn_editor1.clicked.connect(btn_crop)

   def btn_gray(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_gray()
         for img in MyImage.changed:
            img.show()      

   btn_editor2.clicked.connect(btn_gray)

   def btn_blur(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_blur()
         for img in MyImage.changed:
            img.show()      

   btn_editor3.clicked.connect(btn_blur)

   def btn_rotate(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_up()
         for img in MyImage.changed:
            img.show()      

   btn_editor4.clicked.connect(btn_rotate)

   def btn_contrast(self):
      if list_img.selectedItems():
         image_path = os.path.join(workimage.dir, workimage.filename)
         MyImage = ImageEditor(image_path)
         MyImage.open()
         MyImage.do_contrast()
         for img in MyImage.changed:
            img.show()      

   btn_editor5.clicked.connect(btn_contrast)



app.exec()