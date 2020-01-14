#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
text detect
@author: chineseocr
"""
import cv2
import numpy as np
from config import textPath,anchors,GPU
from helper.image import resize_img,get_origin_box,soft_max,reshape
from helper.detectors import TextDetector
if GPU:
     from dnn.darknet import  load_net,predict_image,array_to_image
     textNet = load_net(textPath.replace('.weights','.cfg').encode(),textPath.encode(), 0)
else:
    textNet   =  cv2.dnn.readNetFromDarknet(textPath.replace('weights','cfg'),textPath)  
    

def detect_box(image,scale=600,maxScale=900):
        H,W = image.shape[:2]
        image,rate = resize_img(image,scale,maxScale=maxScale)
        h,w = image.shape[:2]
        if GPU:
            im = array_to_image(image)
            res=predict_image(textNet,im)
            scale=16
            iw = int(np.ceil(im.w/scale))
            ih = int(np.ceil(im.h/scale))
            h,w = image.shape[:2] 
            out = [ res[i] for i in range(40*ih*iw)] 
            out=np.array(out).reshape((1,40,ih,iw))
        else:
            inputBlob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(w,h),swapRB=False ,crop=False);
            outputName = textNet.getUnconnectedOutLayersNames()
            textNet.setInput(inputBlob)
            out  = textNet.forward(outputName)[0]
        clsOut  = reshape(out[:,:20,...])
        boxOut  = reshape(out[:,20:,...])
        boxes  = get_origin_box((w,h),anchors,boxOut[0])        
        scores = soft_max(clsOut[0])
        boxes[:, 0:4][boxes[:, 0:4]<0] = 0
        boxes[:, 0][boxes[:, 0]>=w] = w-1
        boxes[:, 1][boxes[:, 1]>=h] = h-1
        boxes[:, 2][boxes[:, 2]>=w] = w-1
        boxes[:, 3][boxes[:, 3]>=h] = h-1
        
        return scores,boxes,rate,w,h
    
    
def detect_lines(image,scale=600,
                 maxScale=900,
                 MAX_HORIZONTAL_GAP=30,
                 MIN_V_OVERLAPS=0.6,
                 MIN_SIZE_SIM=0.6,
                 TEXT_PROPOSALS_MIN_SCORE=0.7,
                 TEXT_PROPOSALS_NMS_THRESH=0.3,
                 TEXT_LINE_NMS_THRESH = 0.9,
                 TEXT_LINE_SCORE=0.9
                ):
    MAX_HORIZONTAL_GAP = max(16,MAX_HORIZONTAL_GAP)
    detectors = TextDetector(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)
    scores,boxes,rate,w,h = detect_box(image,scale,maxScale)
    size = (h,w)
    text_lines, scores =detectors.detect( boxes,scores,size,\
           TEXT_PROPOSALS_MIN_SCORE,TEXT_PROPOSALS_NMS_THRESH,TEXT_LINE_NMS_THRESH,TEXT_LINE_SCORE)
    if len(text_lines)>0:
        text_lines = text_lines/rate
    return text_lines, scores

    
    
    

