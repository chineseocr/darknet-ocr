#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocr 
@author: chineseocr
@mail: chineseocr@hotmail.com
## add opencv dnn for relu and stride 
## add ocr prob for every char
"""
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
        with open(p,encoding='utf-8')  as f:
            characters = json.loads(f.read())
        return characters
    else:
        return ''


charactersPred = ' '+read_characters()+'｜ '
if GPU:
    from dnn.darknet import  load_net,predict_image,array_to_image
    ocrNet = load_net(ocrPath.replace('.weights','.cfg').encode(),ocrPath.encode(), 0)
else:
    ocrNet = cv2.dnn.readNetFromDarknet(ocrPath.replace('.weights','.cfg'),ocrPath)
    
    
def predict(image):
   if GPU:
       return predict_darknet(image)
   else:
       return predict_cpu(image)
   
def softmax(res):
    resMax = res.max(axis=1).reshape((-1,1))
    res    = res-resMax
    res    = np.exp(res)
    expSum = res.sum(axis=1).reshape((-1,1))
    return res/expSum
        
def predict_cpu(image):
       """
       cnn ctc model  
       same errors, fix opencv dnn  to use
       """
       scale = image.size[1]*1.0 / 32
       w = image.size[0] / scale
       w = int(w)
       if w<8:
           return {'chars':[],'text':'','prob':0}
       image   = image.resize((w,32),Image.BILINEAR)
       image = (np.array(image.convert('L'))/255.0-0.5)/0.5
       image = np.array([[image]])
       ocrNet.setInput(image)
       y_pred = ocrNet.forward()
       out = y_pred[0][:,0,:]
       
       out = out.transpose((1,0))
       out = softmax(out)
       out = decode(out)##
       
       return out
   
def predict_darknet(image):
    scale = image.size[1]*1.0 / 32
    w = image.size[0] / scale
    w = int(w)
    image   = image.resize((w,32),Image.BILINEAR)
    image = (np.array(image.convert('L'))/255.0-0.5)/0.5
    h,w = image.shape
    if w<8:
        return {'chars':[],'text':'','prob':0}
    tmp = np.zeros((h,w,1))
    tmp[:,:,0] = image
    
    im = array_to_image(image)
    res=predict_image(ocrNet,im)
    outW = int(np.ceil(w/4)-3)
    nchars = len(charactersPred)
    out = [ res[i] for i in range(outW*nchars)] 
    out = np.array(out).reshape((nchars,outW))
    out = out.transpose((1,0))
    out = softmax(out)
    
    return decode(out)
   

def decode(pred):
        t = pred.argmax(axis=1)
        prob  = [ pred[ind,pb] for ind,pb in enumerate(t)]
   
        length = len(t)
        charList = []
        probList = []
        n = len(charactersPred)
        for i in range(length):
           if t[i] not in [n-1,n-1] and (not (i > 0 and t[i - 1] == t[i])):
                        charList.append(charactersPred[t[i]])
                        probList.append(prob[i])
        res = {'text':''.join(charList),
               "prob":round(float(min(probList)),2) if len(probList)>0 else 0,
               "chars":[{'char':char,'prob':round(float(p),2)}for char ,p in zip(charList,probList)]}
        return res
    


if __name__=='__main__':
    t =time.time()
    img=Image.open('./test/dd.jpg')
    res = predict(img)
    print(time.time()-t,res)
