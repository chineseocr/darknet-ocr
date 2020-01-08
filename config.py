#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config
@author: chineseocr
"""
ocrType = 'chinese'
ocrPath  = 'models/ocr/{}/ocr.weights'.format(ocrType)
textPath = 'models/text/text.weights'
darkRoot ='darknet/libdarknet.so' ##darknet 
TEXT_LINE_SCORE=0.85##text line prob
scale = 900##可动态修改 no care text.cfg height,width
maxScale = 1800
GPU=False ## gpu for darknet  or cpu for opencv.dnn 
anchors = '16,11, 16,16, 16,23, 16,33, 16,48, 16,68, 16,97, 16,139, 16,198, 16,283'
