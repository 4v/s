/**
 * @file 根据query获取股票代码
 * @author hades
 */

var q = require('q');
var request = require('request');

// 如请求hdgf，则url为http://suggest3.sinajs.cn/suggest/name=info&key=hdgf
var URL = 'http://suggest3.sinajs.cn/suggest/name=suggest&key=';

function suggest(key) {
    var deferred = q.defer();

    if (!key.length) {
        return q.resolve([]);
    }

    var arr = [];

    key.forEach(function (val) {
        arr.push(getSuggest(val));
    });

    q.all(arr).done(
        function (data) {
            data = data || [];

            var res = [];

            data.forEach(function (item) {
                item = item || [];

                if (item) {
                    res = res.concat(item.filter(isHuShen));
                }
            });

            deferred.resolve(res);
        }
    );

    return deferred.promise;
}

function getSuggest(key) {
    return q.Promise(
        function (resolve, reject) {
            request(URL + key, function (erroe, response, body) {
                body = body || '';
                eval(body);

                try {
                    var res = [];

                    var stocks = suggest.split(';');

                    stocks.forEach(function (item) {
                        if (item) {
                            res.push(item.split(',')[3]);
                        }
                    });

                    resolve(res);
                } catch (e) {
                    reject([]);
                }
            });
        }
    );
}

function isHuShen(key) {
    return /^(sh|sz)/.test(key);
}

module.exports = suggest;
