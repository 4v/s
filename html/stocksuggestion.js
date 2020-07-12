
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
suggestion('725')

eleid = "suggestionText"
// autocomplete(document.getElementById(eleid), suggestion(val));
