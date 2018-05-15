#encoding: utf8

import datasource
import model
import util
import account
import json

from bottle import route, run, template, request

@route('/stock/<code>')
def index(code):
    stock = datasource.EastMoney().load_one(code)
    return render_stock(stock)

@route('/fund/<code>')
def index(code):
    stock = datasource.DayDayFund().load(code)
    return render_stock(stock)

@route('/coin/huobi/<code>')
def coin_huobi(code):
    stock = datasource.Huobi().load(code, '5min')
    return render_stock(stock)

def render_stock(stock):
    parameter = request.query.get('parameter', None)
    if parameter: parameter = int(parameter)
    m = model.SlopeModel(stock['prices'][-1000:], parameter=parameter)
    m.run()
    chart = m.get_chart()
    return html_chart(chart)

def html_chart(chart):
    return template('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.bootcss.com/echarts/3.8.5/echarts.min.js"></script>
</head>
<body>
    <input id="parameter" type="input"/>
    <button id="applyButton">修改</button>
    <div id="main" style="width: 100%%;height:600px;"></div>
    <script type="text/javascript">
        var myChart = echarts.init(document.getElementById('main'));
        var option = %s;
        myChart.setOption(option);
        var applyButton = document.getElementById('applyButton');
        var parameterInput = document.getElementById('parameter');
        applyButton.onclick = function() {
            console.log(parameterInput.value);
        }
    </script>
</body>
</html>
''' % chart)

run(host='127.0.0.1', port=8080)
