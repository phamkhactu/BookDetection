from datetime import date
import os
import string
import random
import cv2 
import numpy as np 

class Helper():
    def __init__(self):
        self.folder_name = str(date.today())
        self.txt_name = 'discriptor.txt'
        self.init = self.init()
       
    def init(self):
        if not os.path.exists(self.folder_name):
            os.mkdir(str(self.folder_name))
        file_txt = os.path.join(self.folder_name, self.txt_name)
        if not os.path.isfile(file_txt):
            open(file_txt,'a').close()

    def readfiles(self, folder):
        files = []
        for filename in os.listdir(folder):
            diriect = os.path.join(folder, filename)
            files.append(diriect)
        return files

    def write_txt(self, file_txt, line):
        with open(file_txt, 'a') as writer:
            writer.write(line)

    def read_txt(self, file_txt):
        lst = []
        with open(file_txt, 'r') as reader:
            line = reader.readline()
            while line:            
                data, shape = line.rstrip('\n').split(';')  
                data = data.replace('[','').replace(']','')
                data = data.split(',')
                data = np.array(data, dtype=np.uint8)
                shape = shape.strip().replace('(', '').replace(')', '').split(', ')
                shape = tuple(map(int, shape))
                data = data.reshape(shape)     
                lst.append(data)
                line = reader.readline()
        return lst
    
    def id_generate(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for i in range(10))
    
    def write_image(self, image):
        name = self.id_generate() +'.jpg'
        path = os.path.join(self.folder_name, name)
        while(os.path.isfile(path)):
            name = self.id_generate() +'.jpg'
            path = os.path.join(self.folder_name, name)
        cv2.imwrite(path, image)

def main():
    helper = Helper()
    img = cv2.imread('/home/tu/Pictures/demo.png')
    helper.write_image(img)
    
if __name__ == '__main__':
    main()
    