import numpy as np
import cv2
import os
from module import DNNPreprocessingImgage

class FindBook:
  def __init__(self, name):
    self.name = name
    self.net = cv2.dnn_registerLayer('Crop',DNNPreprocessingImgage.CropLayer)
    self.net = cv2.dnn.readNet(os.path.join("./module",'deploy.prototxt'),os.path.join("./module",'./hed_pretrained_bsds.caffemodel'))

  def preprocessImg(self,img):
    inp = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(500, 500),mean=(104.00698793, 116.66876762, 122.67891434), swapRB=False, crop=False)
    self.net.setInput(inp)
    out = self.net.forward()
    out = out[0, 0]
    out = cv2.resize(out, (img.shape[1], img.shape[0]))
    return out

  def four_corners_sort(self,pts):
    diff = np.diff(pts, axis=1)
    summ = pts.sum(axis=1)
    return np.array([pts[np.argmin(summ)], pts[np.argmax(diff)], pts[np.argmax(summ)], pts[np.argmin(diff)]])

  def warp_perspective_image(self,old_img, page_contour, ratio):
    source_point = page_contour.dot(old_img.shape[0] / ratio)
    height = max(np.linalg.norm(source_point[0] - source_point[1]),
                np.linalg.norm(source_point[2] - source_point[3]))
    width = max(np.linalg.norm(source_point[1] - source_point[2]),
                np.linalg.norm(source_point[3] - source_point[0]))
    target_point = np.array([[0, 0], [0, height], [width, height], [width, 0]], np.float32)
    source_point = source_point.astype(np.float32)
    M = cv2.getPerspectiveTransform(source_point, target_point)
    new_image = cv2.warpPerspective(old_img, M, (int(width), int(height)))
    return new_image

  def find_four_point_corners(self,img):
    img = self.preprocessImg(img)
    img = (255*img).astype('uint8')
    if len(img.shape) >= 3:
      img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, threshed_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    _,contours, hier = cv2.findContours(threshed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    maxApproxpoly = None
    maxHull = None
    maxRect = None
    maxArea = 0
    isConvex = False

    for cnt in contours:
      epsilon = 0.01 * cv2.arcLength(cnt, True)
      approx = cv2.approxPolyDP(cnt, epsilon, True)
      hull = cv2.convexHull(cnt)

      rect = cv2.minAreaRect(hull)
      box = cv2.boxPoints(rect)
      if box is not None:
        box = np.int0(box)
        area = cv2.contourArea(cnt)
        if area > maxArea:
          isConvex = cv2.isContourConvex(hull)
          maxApproxpoly = approx
          maxHull = hull
          maxBox = box
          maxArea = area
    return (maxApproxpoly,maxBox,maxHull,isConvex)
    
  def crop_book(self,img):
    maxApproxpoly,maxBox,maxHull,isConvex = self.find_four_point_corners(img)
    cutimg = None
    if len(maxApproxpoly) == 4:
      maxApproxpoly = np.reshape(maxApproxpoly, (4, 2))
      maxApproxpoly = self.four_corners_sort(maxApproxpoly)
      cutimg = self.warp_perspective_image(img, maxApproxpoly, img.shape[0])
    else:
        if isConvex:
          maxHull = np.reshape(maxHull,(maxHull.shape[0]*maxHull.shape[1],maxHull.shape[2]))
          maxHull = self.four_corners_sort(maxHull)
          cutimg = self.warp_perspective_image(img, maxHull, img.shape[0])
        else:
          maxBox = self.four_corners_sort(maxBox)
          cutimg = self.warp_perspective_image(img, maxBox, img.shape[0])
    if cutimg is not None:
      return  cutimg
    else:
      return  None

def main():
  img = cv2.imread('./BookImages/13.jpg')
  if img is None:
    print('can not read image')
  #img = cv2.resize(img,(600,800))
  book = find_book(name='find book')
  img_preprocess = book.preprocessImg(img)
  cv2.imshow('prepreocess img',img_preprocess)
  cropbook = book.crop_book(img)
  cv2.imshow('crop book',cropbook)
  cv2.waitKey()
if __name__ == '__main__':
  main()
    