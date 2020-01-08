function getValue(value,that){
        //勾选需要识别的票据类型
        var divStyle = document.getElementsByClassName("billname");
        for(var i=0;i<divStyle.length;i++){
            divStyle[i].style.background = 'white';
    }
    that.style.background = 'pink';
    imgJson.billModel = value;
} 

function resizeImg(width,height){
         rate = height/imgJson.height;
         newW = width/rate;
         newH = height/rate;
         if(newW>imgJson.width){
            rate = width/imgJson.width;
            newW = width/rate;
            newH = height/rate;
         }
         return [newW,newH];
         
}


function imgUploadPreview() {
                //预览图像
                jQuery("#imageButton").change(function () {
                var obj=jQuery("#imageButton")[0].files[0];
                imgJson.filename = obj.name;
                var fr=new FileReader();
                fr.readAsDataURL(obj);
                fr.onload=function () {
                      jQuery("#imgimg").attr('src',this.result);
                      imgJson.imgString = this.result;
                      imgJson.url = null;
                      document.getElementById("texturl").value=""
                      var image = new Image();
                      image.onload=function(){
                                      var width = image.width;
                                      var height = image.height;
                                      imgJson.W = width;
                                      imgJson.H = height;
                                      var tmp = resizeImg(width,height);
                                      width=tmp[0];
                                      height=tmp[1];
                                      
                                      jQuery("#imgimg").attr('width',width);
                                      jQuery("#imgimg").attr('height',height);
                                      jQuery("#imgcanvas").attr('width',width);
                                      jQuery("#imgcanvas").attr('height',height);
                                       postBill('text');
                                      };
                      image.src= this.result;
                      
                };
               
                })
 }
 
 
function urlPreview() {
                //预览图像
                jQuery("#texturl").change(function () {
                var url=jQuery("#texturl").val();
                imgJson.url = url;
                imgJson.imgString =null;
                imgJson.filename=null;
                jQuery("#imgimg").attr('src',url); 
                 var image = new Image(); //创建一个image对象
                 image.src=url;
                 image.onerror = function(){
                                   alert(" 图片url错误");
                                };
                                
                 image.onload = function(){
                     var width = image.width;
                     var height = image.height;
                     imgJson.W = width;
                     imgJson.H = height;
                     var tmp = resizeImg(width,height);
                     width=tmp[0];
                     height=tmp[1];
                     
                     jQuery("#imgimg").attr('width',width);
                     jQuery("#imgimg").attr('height',height);
                     jQuery("#imgcanvas").attr('width',width);
                     jQuery("#imgcanvas").attr('height',height);
                 }
                
                })//jQuery("#"+avatarSlect)
 }
 




    
function postBill(url){
         //识别请求
          if(imgJson.url || imgJson.imgString){
              
              loadingGif();
              
              jQuery.ajax({
                type: "post",
                url: url,
                data:JSON.stringify(imgJson),
                success:function(d){
                  
                  imgJson['num']=0;//防止重复提交
                  imgJson["data"] = JSON.parse(d);//返回识别结果
                  if(imgJson.data.data){
                       if(imgJson.data.data.length>0){
                           plotBox(imgJson.data.data);//绘制切图坐标
                       }
                      else if(imgJson.data.errCode==3){
                          alert("图像错误");
                          }
                  
                  }
                 loadingGif(); 
              },
              error: function (XMLHttpRequest, textStatus, errorThrown) {
                    // 状态码
                    console.log(XMLHttpRequest.status);
                    // 状态
                    console.log(XMLHttpRequest.readyState);
                    // 错误信息   
                    console.log(textStatus);
                    loadingGif(); 
                    alert("识别异常!");
                    
                }
            })}
            else{
             alert("上传图片或者URL,再提交！");
            }
        
}



function clearCan(){
    //清除myCanvas容器
               var canvas = document.getElementById('imgcanvas');
                canvas.width=canvas.width;
                canvas.height=canvas.height;
           }




function plotBox(boxes){
            /*根据box 绘制box
            W,H:原始图像尺寸
            */
            var W = imgJson['W'];
            var H = imgJson['H'];
            var canvas = document.getElementById('imgcanvas');
            canvas.width=canvas.width;
            canvas.height=canvas.height;
            if(canvas.getContext){
                //获取对应的CanvasRenderingContext2D对象(画笔)
                var ctx = canvas.getContext("2d");
                ctx.beginPath();
                //设置线条颜色为蓝色
                ctx.strokeStyle = "blue";
                for(var i=0;i<boxes.length;i++){
                        var x1 = parseInt(boxes[i]['box'][0])/W*(parseInt(canvas.width));
                        var y1 = parseInt(boxes[i]['box'][1])/H*(parseInt(canvas.height));
                        var x2 = parseInt(boxes[i]['box'][2])/W*(parseInt(canvas.width));
                        var y2 = parseInt(boxes[i]['box'][3])/H*(parseInt(canvas.height));
                        var x3 = parseInt(boxes[i]['box'][4])/W*(parseInt(canvas.width));
                        var y3 = parseInt(boxes[i]['box'][5])/H*(parseInt(canvas.height));
                        var x4 = parseInt(boxes[i]['box'][6])/W*(parseInt(canvas.width));
                        var y4 = parseInt(boxes[i]['box'][7])/H*(parseInt(canvas.height));
                        ctx.moveTo(x1, y1);
                        ctx.lineTo(x2, y2);
                        ctx.moveTo(x2, y2);
                        ctx.lineTo(x3, y3);
                        ctx.moveTo(x3, y3);
                        ctx.lineTo(x4, y4);
                        ctx.moveTo(x4, y4);
                        ctx.lineTo(x1, y1);
                        ctx.fillText('prob:'+boxes[i]['prob']+' text:'+boxes[i]['text'], x1-5, y1-5);
                }
                ctx.stroke();
                ctx.closePath();
                
            } 

            }



function loadingGif(){
        //加载请求时旋转动态图片
        var imgId=document.getElementById('loadingGif');
        if(imgId.style.display=="block")
            {imgId.style.display="none";}
        else
            {imgId.style.display="block";}
            
}
