# encoding: utf8

import echart

# 运行模型，输入价格，输出每个价格点对应的操作
# 输入：[{'open':开盘价,'close':收盘价},...]
# 输出：每天需要采取的行动。S表示卖出，B表示买入，None表示不动
def run(prices):
    return SlopeModel(prices).run()

class SlopeModel:
    def __init__(self, prices, parameter=None):
        if parameter is None: parameter = 21
        self.prices = prices
        self.parameter = parameter

    def run(self):
        buyLine = self.getBuyLine()
        sellLine = self.getSellLine()
        buy = self.isCross(buyLine, sellLine)
        sell = self.isCross(sellLine, buyLine)
        actions = self.takeAction(buy, sell)
        self.mBuyLine = buyLine
        self.mSellLine = sellLine
        self.mBuy = buy
        self.mSell = sell
        self.mActions = actions
    
    def get_actions(self):
        return self.mActions

    def get_chart(self):
        return echart.make_chart1(self.prices, self.mBuyLine, self.mSellLine, self.mActions)

    def print_line(self, values):
        dates = [e['time'] for e in self.prices]
        assert len(dates) == len(values)
        for date,v in zip(dates, values):
            print(date, v)

    def takeAction(self, buy, sell):
        assert len(buy) == len(sell)
        return [self.takeOneAction(a,b) for a,b in zip(buy, sell)]

    def takeOneAction(self, buy, sell):
        # 确保参数正确
        assert not(buy and sell)

        # 返回结果
        if buy: return 'B'
        if sell: return 'S'
        return None

    def getBuyLine(self):
        closePrices = self.getClosePrices()
        result = self.expMovingAverage(closePrices, 2)
        return result
    
    def getSellLine(self):
        closePrices = self.getClosePrices()
        p = self.parameter
        a = self.slope(closePrices, p)
        b = self.times(a, p)
        c = self.add(b, closePrices)
        return self.expMovingAverage(c, p*2)

    def getClosePrices(self):
        return [e['close'] for e in self.prices]

    def expMovingAverage(self, values, n):
        result = []
        alpha = 2.0 / (n+1)
        for i,e in enumerate(values):
            if i < n-1:
                result.append(None)
                continue
            window = values[i-n+1:i+1]
            if self.has_none(window):
                result.append(None)
                continue
            last = result[-1]
            if last is None: last = e
            result.append(e*alpha + (1-alpha)*last)
        return result

    def weightedAverage(self, values, weights):
        count = sum(weights)
        value = sum([a*b for a,b in zip(values,weights)])
        return value / float(count)

    def has_none(self, values):
        for e in values:
            if e is None:
                return True
        return False

    def slope(self, values, n):
        result = []
        for i,e in enumerate(values):
            if i < n-1:
                result.append(None)
                continue
            window = values[i-n+1:i+1]
            if self.has_none(window):
                result.append(None)
                continue
            xys = [(x,y) for x,y in enumerate(window)]
            xs = [x for x,y in xys]
            ys = [y for x,y in xys]
            a = sum([x*y for x,y in xys])
            b = n * self.average(xs) * self.average(ys)
            c = sum([x**2 for x in xs])
            r = (a-b)/(c-n*self.average(xs)**2)
            result.append(r)
        return result

    def average(self, values):
        count = len(values)
        assert count != 0
        s = sum(values)
        return s / float(count)
    
    def times(self, values, n):
        result = []
        for e in values:
            if e is None:
                result.append(None)
            else:
                result.append(e*n)
        return result
    
    def add(self, values1, values2):
        assert len(values1) == len(values2)
        result = []
        for a,b in zip(values1, values2):
            if a is None or b is None:
                result.append(None)
            else:
                result.append(a+b)
        return result

    def isCross(self, values1, values2):
        assert len(values1) == len(values2)
        n = len(values1)
        result = []
        for i in range(n):
            last1 = values1[i-1]
            last2 = values2[i-1]
            cur1 = values1[i]
            cur2 = values2[i]
            if self.has_none([last1, last2, cur1, cur2]):
                result.append(None)
                continue
            if last1 < last2 and cur1 > cur2:
                result.append(True)
            else:
                result.append(False)
        return result

'''
SlopeModel通达信原始公式如下：
buyLine:EMA(C,2),COLORRED,LINETHICK1;
sellLine:EMA(SLOPE(C,21)*21+C,42),POINTDOT,COLORYELLOW;
buy:=CROSS(buyLine,sellLine);
sell:=CROSS(sellLine,buyLine);
DRAWTEXT(buy,LOW-0.1,'◢Ｂ'),COLORF00FF0,LINETHICK5;
DRAWTEXT(sell,HIGH+0.1,'◥Ｓ'),COLORWHITE,LINETHICK5;
STICKLINE(buyLine>=sellLine,LOW,HIGH,0.1,1),COLORRED;
STICKLINE(buyLine>=sellLine,CLOSE,OPEN,2,1),COLORRED;
STICKLINE(buyLine<sellLine,CLOSE,OPEN,2,0),COLORGREEN;
STICKLINE(buyLine<sellLine,LOW,HIGH,0.1,1),COLORGREEN;
STICKLINE(CROSS(buyLine,sellLine)
OR CROSS(sellLine,buyLine),OPEN,CLOSE,2,0),COLORRED;
'''


# {
#     title: {
#         text: '上证指数',
#         left: 0
#     },
#     tooltip: {
#         trigger: 'axis',
#         axisPointer: {
#             type: 'cross'
#         }
#     },
#     legend: {
#         data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
#     },
#     grid: {
#         left: '10%',
#         right: '10%',
#         bottom: '15%'
#     },
#     xAxis: {
#         type: 'category',
#         data: data0.categoryData,
#         scale: true,
#         boundaryGap : false,
#         axisLine: {onZero: false},
#         splitLine: {show: false},
#         splitNumber: 20,
#         min: 'dataMin',
#         max: 'dataMax'
#     },
#     yAxis: {
#         scale: true,
#         splitArea: {
#             show: true
#         }
#     },
#     dataZoom: [
#         {
#             type: 'inside',
#             start: 50,
#             end: 100
#         },
#         {
#             show: true,
#             type: 'slider',
#             y: '90%',
#             start: 50,
#             end: 100
#         }
#     ],
#     series: [
#         {
#             name: '日K',
#             type: 'candlestick',
#             data: data0.values,
#             itemStyle: {
#                 normal: {
#                     color: upColor,
#                     color0: downColor,
#                     borderColor: upBorderColor,
#                     borderColor0: downBorderColor
#                 }
#             },
#             markPoint: {
#                 label: {
#                     normal: {
#                         formatter: function (param) {
#                             return param != null ? Math.round(param.value) : '';
#                         }
#                     }
#                 },
#                 data: [
#                     {
#                         name: 'XX标点',
#                         coord: ['2013/5/31', 2300],
#                         value: 2300,
#                         itemStyle: {
#                             normal: {color: 'rgb(41,60,85)'}
#                         }
#                     },
#                     {
#                         name: 'highest value',
#                         type: 'max',
#                         valueDim: 'highest'
#                     },
#                     {
#                         name: 'lowest value',
#                         type: 'min',
#                         valueDim: 'lowest'
#                     },
#                     {
#                         name: 'average value on close',
#                         type: 'average',
#                         valueDim: 'close'
#                     }
#                 ],
#                 tooltip: {
#                     formatter: function (param) {
#                         return param.name + '<br>' + (param.data.coord || '');
#                     }
#                 }
#             },
#             markLine: {
#                 symbol: ['none', 'none'],
#                 data: [
#                     [
#                         {
#                             name: 'from lowest to highest',
#                             type: 'min',
#                             valueDim: 'lowest',
#                             symbol: 'circle',
#                             symbolSize: 10,
#                             label: {
#                                 normal: {show: false},
#                                 emphasis: {show: false}
#                             }
#                         },
#                         {
#                             type: 'max',
#                             valueDim: 'highest',
#                             symbol: 'circle',
#                             symbolSize: 10,
#                             label: {
#                                 normal: {show: false},
#                                 emphasis: {show: false}
#                             }
#                         }
#                     ],
#                     {
#                         name: 'min line on close',
#                         type: 'min',
#                         valueDim: 'close'
#                     },
#                     {
#                         name: 'max line on close',
#                         type: 'max',
#                         valueDim: 'close'
#                     }
#                 ]
#             }
#         },
#         {
#             name: 'MA5',
#             type: 'line',
#             data: calculateMA(5),
#             smooth: true,
#             lineStyle: {
#                 normal: {opacity: 0.5}
#             }
#         },
#         {
#             name: 'MA10',
#             type: 'line',
#             data: calculateMA(10),
#             smooth: true,
#             lineStyle: {
#                 normal: {opacity: 0.5}
#             }
#         },
#         {
#             name: 'MA20',
#             type: 'line',
#             data: calculateMA(20),
#             smooth: true,
#             lineStyle: {
#                 normal: {opacity: 0.5}
#             }
#         },
#         {
#             name: 'MA30',
#             type: 'line',
#             data: calculateMA(30),
#             smooth: true,
#             lineStyle: {
#                 normal: {opacity: 0.5}
#             }
#         },
#     ]
# };


# 前复权：http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=6000041&TYPE=k&js=fsData1513510454864((x))&rtntype=5&isCR=false&authorityType=fa&fsData1513510454864=fsData1513510454864

# http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=6000041&TYPE=k&js=fsData1513510454864((x))&rtntype=5&isCR=false&authorityType=ba&fsData1513510454864=fsData1513510454864
# http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=6000041&TYPE=k&js=fsData1513510678588((x))&rtntype=5&isCR=false&fsData1513510678588=fsData1513510678588

# http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=6000041&TYPE=k&rtntype=5&isCR=false&authorityType=fa
