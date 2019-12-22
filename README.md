## 本项目基于darknet(https://github.com/pjreddie/darknet.git)框架实现CTPN版本自然场景文字检测 与CNN+CTCOCR文字识别

# 实现功能
- [x]  CPU版本最短边608时，检测速度小于1秒；
- [x]  支持GPU
- [ ]  支持darknet直接训练CTPN（整理中）；
- [ ]  支持darknet直接训练CNN+CTC ocr（整理中）;
 
 
## 下载text.weights模型文件   
模型文件地址:
* http://www.chineseocr.com:9990/static/models/darknet-ocr/text.weights 


拷贝text.weights文件到models目录

## 编译对GPU的支持  
`
sh make-gpu.sh
`

## web服务启动(支持文件上传及URL图像)
``` Bash
cd darknet-ocr
python3 app.py 8080
```

## 访问服务
http://127.0.0.1:8080/text


## 识别结果展示

<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/img-demo.png"/>  
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/text.png"/>   
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/song.png"/>   
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/dinge.png"/>   
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/ocr.png"/>   
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/sh.png"/>  
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/bank.png"/>  

## 参考
1. yolo3 https://github.com/pjreddie/darknet.git               
2. ctpn  https://github.com/eragonruan/text-detection-ctpn    
3. CTPN  https://github.com/tianzhi0549/CTPN       
