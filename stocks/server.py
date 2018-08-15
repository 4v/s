#encoding: utf8

import datasource
import model
import util
import account
import json

from bottle import route, run, template, request

@route('/')
def indexrt():
    stock = datasource.EastMoney().load_one('sh000001')
    return render_stock(stock)

@route('/s/<code>')
def index(code):
    stock = datasource.EastMoney().load_one(code)
    return render_stock(stock)

@route('/f/<code>')
def indexf(code):
    stock = datasource.DayDayFund().load(code)
    return render_stock(stock)
#/code/huobi
@route('/ch/<code>')
def coin_huobi(code):
    stock = datasource.Huobi().load(code, '5min')
    return render_stock(stock)

def render_stock(stock):
    parameter = request.query.get('parameter', None)
    if parameter: parameter = int(parameter)
    m = model.SlopeModel(stock['prices'][-1000:],
                         stock['name'], parameter=parameter)
    m.run()
    chart = m.get_chart()
    #print(chart)
    return html_chart(chart)

def html_chart(chart):
    return template('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>爱量化</title>
    <script src="https://cdn.bootcss.com/echarts/4.1.0/echarts.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <script type="text/javascript">
        function getUrlSCode(){
            var localurl=window.location.href;  //取得整个地址栏
            return localurl.substring(localurl.lastIndexOf("/")+1,localurl.length);
        }
        var stockCode = getUrlSCode();
    </script>
    <style type="text/css">
        body { margin: 30px; font-family:Didot,"Microsoft YaHei","微软雅黑","Times New Roman",Georgia,Serif }
        .wt { width:808px;font-size: 13px;}
    </style>
</head>
<body>
    <div id="sname" align="right" style="border-bottom:solid 1px grey" class="wt">
    <input id="parameter" type="input" onkeydown="show();"/> 
    <button id="applyButton">修改</button></div>
    <div id="main" style="width:808px;height:400px;"></div>
    <script type="text/javascript">
        var myChart = echarts.init(document.getElementById('main'));
        var option = %s;
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
                console.log(scode);
                window.location.href="/s/"+scode; 
            }
        }
        function show() {
            var e=window.event||arguments.callee.caller.arguments[0];
            if(e.keyCode==13){
                applyButton.onclick();
            }
        }
    </script>
    <div align="center" class="wt"> Q群:243755300 </div>
</body>
</html>
''' % chart)

run(host='127.0.0.1', port=8081)
