## 本项目基于darknet(https://github.com/pjreddie/darknet.git)框架实现CTPN版本自然场景文字检测 与CNN+CTCOCR文字识别
## 支持系统:mac/ubuntu python=3.6  
##  实现功能    
- [x]  文字检测；  
- [x]  文字识别；  
- [x]  支持GPU/CPU，CPU优化（opencv dnn）； 
- [ ]  文字方向检测（4分类模型）； 
- [ ]  支持PDF文档识别；
- [ ]  文字检测训练；  
- [ ]  CNN+CTC ocr训练;
- [ ]  多语言（ 藏语、蒙古语、 朝鲜语、 日本语、 韩语）;
 
 
##  模型文件（参考models目录）  
下载地址:http://www.chineseocr.com:9990/static/models/darknet-ocr/   

## 编译对GPU的支持  
``` Bash
## GPU
cd darknet && cp  Makefile-GPU Makefile && make
```
##  CPU优化
参考opencv版本编译 : https://github.com/chineseocr/opencv-for-darknet.git   

## docker镜像服务（CPU优化版本）
下载镜像 链接:https://pan.baidu.com/s/12F9AYVyBTz34UCXeWj3ATA  密码:5lyz
```
docker load -i darknet-ocr.tar
docker run -it -p 8080:8080 darknet-ocr:1.0 python app.py
````
## web服务启动(支持文件上传及URL图像)
``` Bash
cd darknet-ocr
python3 app.py 8080
```

## 访问服务
http://127.0.0.1:8080/text


## 识别结果展示

<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/demo-line.png"/>  
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/demo-rotate.png"/>   
<img width="500" height="300" src="https://github.com/chineseocr/darknet-ocr/blob/master/test/japanese-demo.png"/>   

## 参考
1. darknet https://github.com/pjreddie/darknet.git               
2. ctpn  https://github.com/eragonruan/text-detection-ctpn    
3. CTPN  https://github.com/tianzhi0549/CTPN       
4. chineseocr https://github.com/chineseocr/chineseocr

## 技术支持合作  
mail:chineseocr@hotmail.com     
  
