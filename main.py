import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtWidgets
from module.mainWindowUi import Ui_MainWindow
from module.findBook import FindBook
from module.bfMatchingWithORB import Measure, Descriptor
from module.helper import Helper
import cv2 
import os 
import numpy as np 
import time 

class DetectionBook(QMainWindow):
	def __init__(self, threshold_img, threshold_new):
		super(DetectionBook, self).__init__()
		self.threshold_img = threshold_img
		self.threshold_new = threshold_new
		self.book = FindBook('book')
		self.measure = Measure()
		self.discriptor = Descriptor()
		self.helper = Helper()
		self.lst_disptor = self.load()
		self.page = 0
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.btn_start.clicked.connect(self.btn_start_click)
		self.ui.btn_close.clicked.connect(self.btn_close_click)
		self.ui.btn_stop.clicked.connect(self.btn_stop_click)
		self.show()
		self.is_open = False
		self.timer = QTimer()
		self.start_time = time.time()
		self.timer.timeout.connect(self.viewCam)

		content_widget = QtWidgets.QWidget()
		self.ui.scrollArea.setWidget(content_widget)
		self._lay = QtWidgets.QVBoxLayout(content_widget)

		self.files_it = iter( self.helper.readfiles(self.helper.folder_name))

		self._timer = QTimer(self, interval=1)
		self._timer.timeout.connect(self.on_timeout)
		self._timer.start()
	
	def load(self):
		file_name = os.path.join(self.helper.folder_name, self.helper.txt_name)
		files = self.helper.read_txt(file_name)
		return files 

	def is_valid_img(self, image):
		'''
		check image is valid to crop book. 
		'''
		is_val = False
		if len(image.shape) >=3:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blur = cv2.Laplacian(image, cv2.CV_64F).var()
		if blur > self.threshold_img:
			is_val = True
		return is_val

	def write_info(self, image, discriptor):
		file_name = os.path.join(self.helper.folder_name, self.helper.txt_name)
		line = str(list(discriptor.flatten())) +';'+ str(discriptor.shape) + '\n'
		self.helper.write_txt(file_name,line)
		self.helper.write_image(image)

	def update_info(self):
		self.ui.lable_status.setText('Mới' if self.is_new else 'Cũ')
		self.ui.label_da_doc.setText(str(self.page))

	def process(self, image):
		discriptor = self.discriptor.get_descriptor(image)
		self.is_new = False
		if discriptor is not None:
			if self.lst_disptor is None:
				self.write_info(image, discriptor)
				self.lst_disptor.append(discriptor)
				self.is_new = True 
				self.page +=1
			else:
				scores  = [self.measure.compare(discriptor, val) for val in self.lst_disptor]
				self.is_new = all(score < self.threshold_new for score in scores)
				if self.is_new:
					self.lst_disptor.append(discriptor)
					self.write_info(image, discriptor)
					self.page += 1
		return self.is_new

	def on_timeout(self):
		try:
			file = next(self.files_it)
			pixmap = QPixmap(file)
			self.add_pixmap(pixmap)
		except StopIteration:
			self._timer.stop()

	def add_pixmap(self, pixmap):
		if not pixmap.isNull():
			pixmap = pixmap.scaled(self.ui.scrollArea.width(), self.ui.scrollArea.height())
			label = QLabel(pixmap=pixmap)
			self._lay.addWidget(label)

	def viewCam(self):
		ret, frame = self.cap.read()
		image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		height, width, channel = image_rgb.shape
		step = channel * width
		qImg = QImage(image_rgb.data, width, height, step, QImage.Format_RGB888)
		qImg = qImg.scaled(self.ui.image.width(), self.ui.image.height())
		# show image in img_label
		self.ui.image.setPixmap(QPixmap.fromImage(qImg))
		exectime = time.time() - self.start_time
		if exectime >=5:
			self.start_time = time.time()
			if self.is_valid_img(frame):
				print('is valid')
				crop_book = self.book.crop_book(frame)
				if crop_book is not None:
					status = self.process(crop_book)
					if status:
						print('=====> new page')
			self.update_info()

	def btn_start_click(self):
		self.cap = cv2.VideoCapture(0)
		self.timer.start(20)          

	def btn_stop_click(self):
		self.timer.stop()
		self.cap.release()

	def btn_close_click(self):
		sys.exit()

def main():
	app = QApplication(sys.argv)
	ex = DetectionBook(100,0.01)
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()