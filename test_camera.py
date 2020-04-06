import cv2
import os
import findBook 
import argparse

def is_valid_img(img):
    '''
    kiem tra hinh anh co du tieu chuan hay khong
    '''
def main():
    book = findBook.find_book(name='book')
    cap = cv2.VideoCapture(0)
    cv2.waitKey(10)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('can not open camera')
            exit()
        img = cv2.resize(frame,(800,600))
        '''
        check image is_valid_img
        code bala bala
        '''
        crop_book = book.crop_book(frame)
        cv2.imshow('crop book',crop_book)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == "__main__":
    main()