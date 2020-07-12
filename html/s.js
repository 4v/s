$(function () {
    idtxt = "#suggestionText"
    idv = "#suggestion_id"
    $(idtxt).autocomplete({
        minLength: 2,  //满足搜索的最小长度
        inputval = $(idtxt).val(),
        source: function (request, response) {
            var url = '/suggest/type=&name=suggestdata&key=' + encodeURI(val)
            $.ajax({
                url: url,
                xhrFields: { withCredentials: true },
                success: function (data) {
                    console.log(data)
                    var searchData = parseSearchData(data);
                    console.log(searchData)
                    // $("#searchResult").show().html("");
                    // for (var i = 0; i < searchData.length; i++) {
                    //     var item = searchData[i];
                    //     $("#searchResult").append('<div stockId="' + item.id + '">' + item.id + ' ' + item.name + '</div>');
                    // }
                    // $("#searchResult div").click(function () {
                    //     addStock($(this).attr("stockId"));
                    //     showPrice();
                    // });
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    // pass
                }
            });
            $.ajax({
                url: "/onWay/getCompanyName",
                type: "post",
                dataType: "json",
                data: {
                    companynm: $(idtxt).val()
                },
                success: function (data) {
                    response($.map(data.company, function (item) {
                        return {
                            label: item.name,
                            value: item.id
                        }
                    }));
                }
            });
        },
        select: function (event, ui) {
            //设置输入框值
            $(idtxt).val(ui.item.label);
            //设置id值
            $(idv).val(ui.item.value);
            return false;
        }
    });
});
function suggestion(val){
    // var url = 'http://suggest3.sinajs.cn/suggest/type=&name=suggestdata&key=' + encodeURI(val)
    var url = '/suggest/type=&name=suggestdata&key=' + encodeURI(val)
    $.ajax({
        url: url,
        xhrFields: { withCredentials: true },
        success: function (data) {
            console.log(data)
            var searchData = parseSearchData(data);
            console.log(searchData)
            // $("#searchResult").show().html("");
            // for (var i = 0; i < searchData.length; i++) {
            //     var item = searchData[i];
            //     $("#searchResult").append('<div stockId="' + item.id + '">' + item.id + ' ' + item.name + '</div>');
            // }
            // $("#searchResult div").click(function () {
            //     addStock($(this).attr("stockId"));
            //     showPrice();
            // });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // pass
        }
    });
    var parseSearchData = function (data) {
        var result = [];
        if (typeof data === "string" && data.length > 0) {
            var searchListarr = data.split(/"|;/);
            srlen = searchListarr.length
            if(srlen > 0){
                var searchList = searchListarr.slice(1,srlen-2)
                console.log(searchList)
                for (var i = 0; i < searchList.length; i++) {
                    var sSearchResult = parseSingleSearchData(searchList[i]);
                    if (sSearchResult !== null) {
                        result.push(sSearchResult);
                    }
                }
            }
        }
        return result;
    };
    var parseSingleSearchData = function (data) {
        var result = null;
        var values = data.split(/,/);
        if (values.length >= 6) {
            result = {
                id: values[3],
                name: values[4]
            };
        }
        return result;
    };
};
