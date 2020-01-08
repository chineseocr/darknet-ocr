## 本项目基于darknet(https://github.com/pjreddie/darknet.git)框架实现CTPN版本自然场景文字检测 与CNN+CTCOCR文字识别

##  实现功能    
- [x]  文字检测；  
- [x]  文字识别；  
- [x]  支持GPU/CPU，CPU优化（opencv dnn）；  
- [ ]  支持PDF文档识别；
- [ ]  文字检测训练；  
- [ ]  CNN+CTC ocr训练;
- [ ]  多语言（ 藏语、蒙古语、 朝鲜语、 日本语、 韩语）;
 
 
##  模型文件（参考models目录）  
下载地址:http://www.chineseocr.com:9990/static/models/darknet-ocr/   

## 编译对GPU的支持  
``` Bash
## cpu 
cd darknet && cp  Makefile-cpu Makefile && make
## GPU
cd darknet && cp  Makefile-GPU Makefile && make
```

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
1. darknet https://github.com/pjreddie/darknet.git               
2. ctpn  https://github.com/eragonruan/text-detection-ctpn    
3. CTPN  https://github.com/tianzhi0549/CTPN       
4. chineseocr https://github.com/chineseocr/chineseocr

## 技术支持合作  
mail:chineseocr@hotmail.com     
  
