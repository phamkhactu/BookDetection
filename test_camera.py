import cv2
import os
import findBook 

def is_valid_img(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()
    '''
    kiem tra hinh anh co du tieu chuan hay khong
    '''
def main():
    book = findBook.find_book(name='book')
    cap = cv2.VideoCapture(0)
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
    book = findBook.find_book(name='book')
    img = cv2.imread('imageBook/low_image/1.jpg')
    # img = cv2.resize(img,(img.shape[0]//5,img.shape[1]//5))

    img_preprocess = book.preprocessImg(img)
    cv2.imshow("img resize", img)
    cv2.waitKey()
    # cv2.destroyAllWindows()
    crop_book = book.crop_book(img)
    cv2.imshow("crop_book", crop_book)
    fm = is_valid_img(crop_book)
    text = "Not Blurry"
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < 100:
        text = "Blurry"
    # show the image
    cv2.putText(crop_book, "{}: {:.2f}".format(text, fm), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", crop_book)
    key = cv2.waitKey(0)
    # main()