#encoding: utf8

import datasource
import model
import util
import account
import json

from bottle import app, route, run, template, request

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
    return template('index', option=chart)

app = app()
if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8081)

def test():
    stock = datasource.EastMoney().load_one('sh000001')
    ctxs = render_stock(stock)
    print(ctxs)
