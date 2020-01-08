import cv2
import os
import time
import json
import numpy as np
from PIL import Image
from config import ocrPath,GPU
def read_characters():
    p= ocrPath.replace('.weights','.json')
    if os.path.exists(p):
        with open(p)  as f:
            characters = json.loads(f.read())
        return characters
    else:
        return ''


charactersPred = ' '+read_characters()+'｜ '
if 1:
    from dnn.darknet import  load_net,predict_image,array_to_image
    ocrNet = load_net(ocrPath.replace('.weights','.cfg').encode(),ocrPath.encode(), 0)
else:
    ocrNet = cv2.dnn.readNetFromDarknet(ocrPath.replace('.weights','.cfg'),ocrPath)

def predict_cpu(image):
       """
       cnn ctc model  
       same errors, fix opencv dnn  to use
       """
       scale = image.size[1]*1.0 / 32
       w = image.size[0] / scale
       w = int(w)
       image   = image.resize((w,32),Image.BILINEAR)
       image = (np.array(image.convert('L'))/255.0-0.5)/0.5
       image = np.array([[image]])
       ocrNet.setInput(image)
       y_pred = ocrNet.forward(ocrNet.getUnconnectedOutLayersNames())
       y_pred = y_pred[0][0,:,-1,:]
       out    = decode(y_pred)##
       return out
   
def predict_darknet(image):
    scale = image.size[1]*1.0 / 32
    w = image.size[0] / scale
    w = int(w)
    image   = image.resize((w,32),Image.BILINEAR)
    image = (np.array(image.convert('L'))/255.0-0.5)/0.5
    h,w = image.shape
    if w<8:
        return ''
    tmp = np.zeros((h,w,1))
    tmp[:,:,0] = image
    
    im = array_to_image(image)
    res=predict_image(ocrNet,im)
    outW = int(np.ceil(w/4)-3)
    nchars = len(charactersPred)
    out = [ res[i] for i in range(outW*nchars)] 
    out = np.array(out).reshape((nchars,outW))
    out = out.transpose((1,0))
    return decode(out)
   
   
def decode(pred):
        t = pred.argmax(axis=1)
        length = len(t)
        char_list = []
        n = len(charactersPred)
        for i in range(length):
           if t[i] not in [n-1,n-1] and (not (i > 0 and t[i - 1] == t[i])):
                        char_list.append(charactersPred[t[i]])
        return ''.join(char_list)
    


if __name__=='__main__':
    t =time.time()
    img=Image.open('./test/test.png')
    res = predict_darknet(img)
    print(time.time()-t,res)
