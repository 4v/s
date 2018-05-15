#encoding: utf8

import util
import json

def make_chart1(prices, buyLine, sellLine, actions):
    upColor = '#ec0000'
    downColor = '#00da3c'
    upBorderColor = '#8A0000'
    downBorderColor = '#008F28'
    kLine = [[e['open'], e['close'], e['low'], e['high']] for e in prices]
    actionTranslation = {'B':'{BUY}','S':'{SELL}'}
    actionColors = {'B':'#ec0000','S':'#00da3c'}
    actionMarks = [{
        'name': 'XX标点' + str(i),
        'coord': [util.format_datetime(prices[i]['time']), prices[i]['close']],
        'label': {
            'normal': {
                'formatter': actionTranslation[action],
            }
        },
        'itemStyle': {
            'normal': {'color': actionColors[action]}
        }
    } for i,action in enumerate(actions) if action is not None]
    dates = [util.format_datetime(price['time']) for price in prices]
    result = {
        'title': {
            'text': '标题',
            'left': 0
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross'
            }
        },
        'legend': {
            'data': ['日K', '买线', '卖线']
        },
        'grid': {
            'left': '10%',
            'right': '10%',
            'bottom': '15%'
        },
        'xAxis': {
            'type': 'category',
            'data': dates,
            'scale': True,
            'boundaryGap' : False,
            'axisLine': {'onZero': False},
            'splitLine': {'show': False},
            'min': 'dataMin',
            'max': 'dataMax'
        },
        'yAxis': {
            'scale': True,
            'splitArea': {
                'show': True
            }
        },
        'dataZoom': [
            {
                'type': 'inside',
                'start': (1-60/float(len(prices)))*100,
                'end': 100
            },
            {
                'show': True,
                'type': 'slider',
                'y': '90%',
                'start': 50,
                'end': 100
            }
        ],
        'series': [
            {
                'name': '日K',
                'type': 'candlestick',
                'data': kLine,
                'itemStyle': {
                    'normal': {
                        'color': upColor,
                        'color0': downColor,
                        'borderColor': upBorderColor,
                        'borderColor0': downBorderColor
                    }
                },
                'markPoint': {
                    'label': {
                        'normal': dict()
                    },
                    'data': actionMarks,
                },
            },
            {
                'name': '买线',
                'type': 'line',
                'data': buyLine,
                'smooth': False,
                'lineStyle': {
                    'normal': {'opacity': 0.5}
                }
            },
            {
                'name': '卖线',
                'type': 'line',
                'data': sellLine,
                'smooth': False,
                'lineStyle': {
                    'normal': {'opacity': 0.5}
                }
            }
        ]
    }
    result = json.dumps(result)
    result = result.replace('"{BUY}"','function(){return "买";}')
    result = result.replace('"{SELL}"','function(){return "卖";}')
    return result
