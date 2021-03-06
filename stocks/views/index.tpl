<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>爱量化</title>
    <script src="https://cdn.bootcss.com/echarts/4.1.0/echarts.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <style type="text/css">
        body { margin: 30px; font-family:Didot,"Microsoft YaHei","微软雅黑","Times New Roman",Georgia,Serif }
        .wt { width:808px;font-size: 13px;}
    </style>
</head>
<body>
    <div id="sname" align="right" style="border-bottom:solid 1px grey" class="wt">
    <input id="parameter" type="input" value="sh000001" onkeydown="show();"/> 
    <button id="applyButton">修改</button></div>
    <div id="main" style="width:808px;height:400px;"></div>
    <script type="text/javascript">

        var stockCode;
        var locurl;
        var urltp;
        function getUrlSCode(){
            var localurl=window.location.href;  //取得整个地址栏
            stockCode=localurl.substring(localurl.lastIndexOf("/")+1,localurl.length);
            locurl=localurl.substring(0,localurl.lastIndexOf("/"));
            if(locurl){
                urltp=locurl.substring(locurl.lastIndexOf("/"),locurl.length);
            }
        }
        getUrlSCode();
        var myChart = echarts.init(document.getElementById('main'));
        var option = {{!option}};
        myChart.setOption(option);
        var applyButton = document.getElementById('applyButton');
        var parameterInput = document.getElementById('parameter');
        parameterInput.value = stockCode;
        //var stockelem = getStockData(stockCode);
        //$("#sname").html() = stockelem[0];

        function getStockData(stockCodeNum){
            var param_string = "hq_str_" + stockCodeNum;  
            var param = eval(param_string);  
            var elements = param.split(",");
            return elements;
        }
        applyButton.onclick = function() {
            scode = parameterInput.value;
            if(scode){
                var perfix;
                if(urltp=="/s"||urltp=="/f"||urltp=="/ch"){
                    perfix = urltp;
                }else{
                    perfix="/s";
                }
                window.location.href=perfix+"/"+scode; 
            }
        }
        function show() {
            var e=window.event||arguments.callee.caller.arguments[0];
            if(e.keyCode==13){
                applyButton.onclick();
            }
        }
    </script>
    <!-- 
    <div align="center" class="wt"> Q群:243755300 </div>
    -->
    <br>
    <br>
    <hr>
    <div align="center" class="wt"> Author：乾朗Jonathan </div>
    <hr>
</body>
</html>