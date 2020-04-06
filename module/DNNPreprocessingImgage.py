import cv2 as cv
import argparse
import os



parser = argparse.ArgumentParser(
description='This sample shows how to define custom OpenCV deep learning layers in Python. '
            'Holistically-Nested Edge Detection (https://arxiv.org/abs/1504.06375) neural network '
            'is used as an example model. Find a pre-trained model at https://github.com/s9xie/hed.')
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--prototxt',help='Path to deploy.prototxt',default='./deploy.prototxt')
parser.add_argument('--caffemodel', help='Path to hed_pretrained_bsds.caffemodel',default='./hed_pretrained_bsds.caffemodel')
parser.add_argument('--width', help='Resize input image to a specific width', default=500, type=int)
parser.add_argument('--height', help='Resize input image to a specific height', default=500, type=int)
args = parser.parse_args()

#! [CropLayer]
class CropLayer(object):
  def __init__(self, params, blobs):
      self.xstart = 0
      self.xend = 0
      self.ystart = 0
      self.yend = 0

  # Our layer receives two inputs. We need to crop the first input blob
  # to match a shape of the second one (keeping batch size and number of channels)
  def getMemoryShapes(self, inputs):
      inputShape, targetShape = inputs[0], inputs[1]
      batchSize, numChannels = inputShape[0], inputShape[1]
      height, width = targetShape[2], targetShape[3]

      self.ystart = (inputShape[2] - targetShape[2]) // 2
      self.xstart = (inputShape[3] - targetShape[3]) // 2
      self.yend = self.ystart + height
      self.xend = self.xstart + width

      return [[batchSize, numChannels, height, width]]

  def forward(self, inputs):
      return [inputs[0][:,:,self.ystart:self.yend,self.xstart:self.xend]]
#! [CropLayer]
def preprocessImg(img):
  #! [Register]
  #cv.dnn_registerLayer('Crop', CropLayer)
  #! [Register]

  net = cv.dnn.readNet(os.path.join("",args.prototxt), os.path.join("",args.caffemodel))

  inp = cv.dnn.blobFromImage(img, scalefactor=1.0, size=(args.width, args.height),mean=(104.00698793, 116.66876762, 122.67891434), swapRB=False, crop=False)
  net.setInput(inp)
  out = net.forward()
  out = out[0, 0]
  out = cv.resize(out, (img.shape[1], img.shape[0]))
  return out
def main():

  filename =args.input
  img = cv.imread(filename)
  cv.imshow('Input', img)

  outputImage= preprocessImg(img)
  outputImage = (255*outputImage).astype('uint8')
  cv.imshow('preprocess image',outputImage)

  cv.waitKey()
if __name__ == '__main__':
  main()