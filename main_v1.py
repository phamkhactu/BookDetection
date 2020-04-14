import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer, QThreadPool
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from module.mainWindowUi import Ui_MainWindow
from module.findBook import FindBook
from module.bfMatchingWithORB import Measure, Descriptor
from module.helper import Helper
import cv2 
import os 
import numpy as np 
import time 
import traceback, sys


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        # self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
        

class DetectionBook(QMainWindow):
    def __init__(self, threshold_img, threshold_new, *args, **kwargs):
        super(DetectionBook, self).__init__(*args, **kwargs)
        self.threshold_img = threshold_img
        self.threshold_new = threshold_new
        self.book = FindBook('book')
        self.measure = Measure()
        self.discriptor = Descriptor()
        self.helper = Helper()
        self.lst_disptor = self.load()
        self.page = 0
        self.start = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_start.clicked.connect(self.btn_start_click)
        self.ui.btn_close.clicked.connect(self.btn_close_click)
        self.ui.btn_stop.clicked.connect(self.btn_stop_click)
        self.show()
        self.is_new = False
        self.thread_1 = QThreadPool()
        self.thread_2 = QThreadPool()
        self.timer_1 = QTimer()
        self.timer_1.timeout.connect(self.viewCam)
        self.timer_2 = QTimer()
        self.timer_2.timeout.connect(self.execute)
        self.start_time = time.time()

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

    def is_new_image(self, image):
        discriptor = self.discriptor.get_descriptor(image)
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

    def process(self):
        exectime = time.time() - self.start_time
        if exectime >=5:
            self.start_time = time.time()
            if self.is_valid_img(self.frame):
                self.ui.lable_thong_bao.setText('Đang xử lý')
                crop_book = self.book.crop_book(self.frame)
                if crop_book is not None:
                    # crop = cv2.cvtColor(crop_book, cv2.COLOR_BGR2RGB)
                    crop = self.set_Qimage(crop_book)
                    crop = crop.scaled(self.ui.image_crop.width(), self.ui.image_crop.height())
                    self.ui.image_crop.setPixmap(QPixmap.fromImage(crop))
                    worker = Worker(self.is_new_image, crop_book)
                    self.thread_2.start(worker)
                    # status = self.is_new_image(crop_book)
                    if self.is_new:
                        print('=====> new page')
            else:            
                self.ui.lable_thong_bao.setText('Ảnh quá mờ để xử lý')
            self.update_info()

    def execute(self):
        work_1 = Worker(self.process)
        self.thread_1.start(work_1)
       

    def set_Qimage(self, image):
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        return qImg

    def viewCam(self):
        ret, self.frame = self.cap.read(0)
        image_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        qImg = self.set_Qimage(image_rgb)
        qImg = qImg.scaled(self.ui.image.width(), self.ui.image.height())
        # show image in img_label
        self.ui.image.setPixmap(QPixmap.fromImage(qImg))
            
    def btn_start_click(self):
        self.cap = cv2.VideoCapture(0)
        self.timer_1.start(20)  
        self.timer_2.start(20)

    def btn_stop_click(self):
        self.timer.stop()
        self.cap.release()

    def btn_close_click(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    ex = DetectionBook(60,0.1)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()