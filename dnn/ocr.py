import cv2
import time
import numpy as np
from PIL import Image
from keys import characters 
from config import ocrPath,GPU
charactersPred = ' '+characters+'  '
if GPU:
    pass
else:
   net = cv2.dnn.readNetFromDarknet(ocrPath.replace('weights','cfg'),ocrPath)

def predict_cpu(image):
       """
       cnn ctc model 
       """
       scale = image.size[1]*1.0 / 32
       w = image.size[0] / scale
       w = int(w)
       image   = image.resize((w,32),Image.BILINEAR)
       image = (np.array(image.convert('L'))/255.0-0.5)/0.5
       image = np.array([[image]])
       net.setInput(image)
       y_pred = net.forward(net.getUnconnectedOutLayersNames())
       y_pred = y_pred[0][0,:,-1,:]
       out    = decode(y_pred)##
       return out
   
   
def decode(pred):
        t = pred.argmax(axis=0)
        length = len(t)
        char_list = []
        n = len(charactersPred)
        for i in range(length):
           if t[i] not in [n-1,n-2] and (not (i > 0 and t[i - 1] == t[i])):
                        char_list.append(charactersPred[t[i]])
        return ''.join(char_list)


if __name__=='__main__':
    t =time.time()
    img=Image.open('./13.jpg')
    res = predict(img)
    print(time.time()-t,res)
