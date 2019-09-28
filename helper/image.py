#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image
@author: chineseocr
"""
import numpy as np
import cv2
import requests
import six
from PIL import Image
import traceback
import base64
import datetime as dt
def get_now():
    """
    获取当前时间
    """
    try:
        now = dt.datetime.now()
        nowString = now.strftime('%Y-%m-%d %H:%M:%S')
    except:
        nowString = '00-00-00 00:00:00'
    return nowString

def read_url_img(url):
    """
    爬取网页图片
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
    try:
        req = requests.get(url,headers=headers,timeout=5)##访问时间超过5s，则超时
        if req.status_code==200:
            imgString = req.content
            buf = six.BytesIO()
            buf.write(imgString)
            buf.seek(0)
            img = Image.open(buf).convert('RGB')
            return img
        else:
            return None
    except:
        #traceback.print_exc()
        return None
    
    
def base64_to_PIL(string):
    try:
            
            base64_data = base64.b64decode(string.split('base64,')[-1])
            buf = six.BytesIO()
            buf.write(base64_data)
            buf.seek(0)
            img = Image.open(buf).convert('RGB')
            return img
    except:
        return None
    

def soft_max(x):
    """numpy softmax"""
    expz = np.exp(x)
    sumz = np.sum(expz,axis=1)
    return expz[:,1]/sumz

def reshape(x):
    b = x.shape
    x = x.transpose(0, 2, 3, 1)
    b = x.shape
    x = np.reshape(x,[b[0],b[1]*b[2]*10,2])
    return x

def resize_img(image,scale,maxScale=None):
    """
    image :BGR array 
    """
    image = np.copy(image)
    vggMeans = [122.7717,102.9801, 115.9465 ]
    imageList = cv2.split(image.astype(np.float32))
    imageList[0] = imageList[0]-vggMeans[0]
    imageList[1] = imageList[1]-vggMeans[1]
    imageList[2] = imageList[2]-vggMeans[2]
    image = cv2.merge(imageList)
    h,w   = image.shape[:2]
    rate  = scale/min(h,w)
    if maxScale is not None:
        if rate*max(h,w)>maxScale:
            rate = maxScale/max(h,w)
            
    image = cv2.resize(image, None, None,fx=rate, fy=rate, interpolation=cv2.INTER_LINEAR)
    return image,rate

    
    
def get_origin_box(size,anchors,boxes, scale = 16):
    """
    size:(w,h) --h,w =img.shape[:2]//16 --- vggnet 8 maxpool 
    boxes.shape = iw*ih*len(anchors)
    """
   
    w,h = size 
    iw = int(np.ceil(w/scale))*scale
    ih = int(np.ceil(h/scale))*scale
    anchors = np.array(anchors.split(',')).astype(int)
    anchors = np.repeat(anchors,2,axis=0).reshape((-1,4))
    anchors[:,[1,2]] = anchors[:,[2,1]]
    anchors = anchors/2.0
    cscale = (scale-1)/2.0
    anchors[:,[0,1]]= cscale-anchors[:,[0,1]]
    anchors[:,[2,3]]= cscale+anchors[:,[2,3]]
    gridbox =[[[i,j,i,j]+anchors for i in range(0,iw,scale)] for j in range(0,ih,scale)]
    gridbox = np.array(gridbox)
    gridbox = gridbox.reshape((-1,4))   
    gridcy = (gridbox[:,1]+gridbox[:,3])/2.0
    gridh  = (gridbox[:,3]-gridbox[:,1]+1)
    cy     = boxes[:,0]*gridh+gridcy
    ch     = np.exp( boxes[:,1])*gridh
    ymin   =cy-ch/2
    ymax   = cy+ch/2
    gridbox[:,1] =  ymin
    gridbox[:,3] =ymax
    return gridbox



def nms(boxes, scores, score_threshold=0.5, nms_threshold=0.3):
    def box_to_center(box):
        xmin,ymin,xmax,ymax = box
        w = xmax-xmin
        h = ymax-ymin
        return [round(xmin,4),round(ymin,4),round(w,4),round(h,4)]
    
    newBoxes = [ box_to_center(box) for box in boxes]
    newscores = [ round(float(x),6) for x in scores]
    index = cv2.dnn.NMSBoxes(newBoxes, newscores, score_threshold=score_threshold, nms_threshold=nms_threshold)
    if len(index)>0:
        index = index.reshape((-1,))
        return boxes[index],scores[index]
    else:
        return [],[]

def solve(box):
     """
     绕 cx,cy点 w,h 旋转 angle 的坐标
     x = cx-w/2
     y = cy-h/2
     x1-cx = -w/2*cos(angle) +h/2*sin(angle)
     y1 -cy= -w/2*sin(angle) -h/2*cos(angle)
     
     h(x1-cx) = -wh/2*cos(angle) +hh/2*sin(angle)
     w(y1 -cy)= -ww/2*sin(angle) -hw/2*cos(angle)
     (hh+ww)/2sin(angle) = h(x1-cx)-w(y1 -cy)
     """
        
     x1,y1,x2,y2,x3,y3,x4,y4= box[:8]
     cx = (x1+x3+x2+x4)/4.0
     cy = (y1+y3+y4+y2)/4.0
     w = (np.sqrt((x2-x1)**2+(y2-y1)**2)+np.sqrt((x3-x4)**2+(y3-y4)**2))/2
     h = (np.sqrt((x2-x3)**2+(y2-y3)**2)+np.sqrt((x1-x4)**2+(y1-y4)**2))/2   
     sinA = (h*(x1-cx)-w*(y1 -cy))*1.0/(h*h+w*w)*2
     if abs(sinA)>1:
          angle = None
     else:
          angle = np.arcsin(sinA)
        
     return angle,w,h,cx,cy

def rotate_nms(boxes, scores, score_threshold=0.5, nms_threshold=0.3):
    """
    boxes.append((center, (w,h), angle * 180.0 / math.pi))
    
    """
    def rotate_box(box):
       angle,w,h,cx,cy =  solve(box)
       angle = round(angle,4)
       w = round(w,4)
       h = round(h,4)
       cx = round(cx,4)
       cy = round(cy,4)
       return ((cx,cy),(w,h),angle)

   
    if len(boxes)>0:
        newboxes = [rotate_box(box) for box in boxes]
        newscores = [ round(float(x),6) for x in scores]
        index = cv2.dnn.NMSBoxesRotated(newboxes, newscores, score_threshold=score_threshold, nms_threshold=nms_threshold)
        
        if len(index)>0:
           index = index.reshape((-1,))
           return boxes[index],scores[index]
        else:
           return [],[]
    else:
        return [],[]


def get_boxes(bboxes):
    """
        boxes: bounding boxes
    """
    text_recs=np.zeros((len(bboxes), 8), np.int)
    index = 0
    for box in bboxes:
        
        b1 = box[6] - box[7] / 2
        b2 = box[6] + box[7] / 2
        x1 = box[0]
        y1 = box[5] * box[0] + b1
        x2 = box[2]
        y2 = box[5] * box[2] + b1
        x3 = box[0]
        y3 = box[5] * box[0] + b2
        x4 = box[2]
        y4 = box[5] * box[2] + b2
        
        disX = x2 - x1
        disY = y2 - y1
        width = np.sqrt(disX*disX + disY*disY)
        fTmp0 = y3 - y1
        fTmp1 = fTmp0 * disY / width
        x = np.fabs(fTmp1*disX / width)
        y = np.fabs(fTmp1*disY / width)
        if box[5] < 0:
           x1 -= x
           y1 += y
           x4 += x
           y4 -= y
        else:
           x2 += x
           y2 += y
           x3 -= x
           y3 -= y

        text_recs[index, 0] = x1
        text_recs[index, 1] = y1
        text_recs[index, 2] = x2
        text_recs[index, 3] = y2
        text_recs[index, 4] = x3
        text_recs[index, 5] = y3
        text_recs[index, 6] = x4
        text_recs[index, 7] = y4
        index = index + 1
    
    boxes = []
    for box in text_recs:
           x1,y1 = (box[0],box[1])
           x2,y2 = (box[2],box[3])
           x3,y3 = (box[6],box[7])
           x4,y4 = (box[4],box[5])
           boxes.append([x1,y1,x2,y2,x3,y3,x4,y4])
    boxes = np.array(boxes)
    return boxes

    