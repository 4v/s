//current time main funds  http://s1.dfcfw.com/js/index.js
//上深指数 http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/cache.aspx?Type=c1
// current day main funds http://s1.dfcfw.com/allXML/index.xml
$(document).ready(function(){
  var webMethod = "/zlzj";//主力资金流入
  var ssindex = "/ssindex"; //上深指数
  //var webMethod = "/mainfunds-part.data";
  var dom = document.getElementById("container");
  var myChart = echarts.init(dom);
  var latestDay = null;
  var app = {};
  var option = null;
  // var data = [];
  var fillData = {};
  var spanCache = '<b>{dqzs}</b>{zdqs}<b>{zdzs}</b>{zdqs}<b>{zdf}&nbsp;&nbsp;{cje}</b>';
  var loadclass = function (g, a) {
    var f;
    if (isNaN(g) || isNaN(a)) {  return "-"  }
    if (parseFloat(g) > a) { f = "red" }
    else {
      if (parseFloat(g) < a) { f = "green" }
      else { f = "" + g + "" }
    }
  return f
  };

  function loadData(){
    fillData = {};
    fillData.legend = ['主力净流入','超大单净流入','大单净流入','中单净流入','小单净流入'];//主
    fillData.xAxis = [];//time
    fillData.series = []; // legend item data
    //data.splice(0,data.length);
    //delete arr;
    $.ajax({
        url : webMethod,
        dataType:"text",
        success:function(responseData)
        {
          console.log(responseData);
          var arr= responseData.split('\n');
          //console.log(arr);
          var lastupdate = arr[0]; //2016-06-17 15:01:30
          var lastActual = arr[1];//2016-06-17 15:00:00
          var currentDateTime = lastActual.split(' ');
          latestDay = currentDateTime[0];
          for (var i = 0; i < fillData.legend.length; i++) {
            fillData.series.push({
                name: fillData.legend[i],
                type:'line',
                line: '总量',
                data:[]
            });
          }
          if(arr.length>3){
            for (var i = 2; i < arr.length; i++) {
              var linedata = arr[i].split(";"); //9:30;-0.4543;0.2638;-0.7180;0.0249;0.4294

                //linedata[0];//时间 9:30
                //linedata[1];//主
                // linedata[2];//超大super big
                // linedata[3];//big
                // linedata[4];//middle
                // linedata[5];//small
                fillData.xAxis.push(linedata[0]);
                for (var j = 0; j < fillData.legend.length; j++) {
                  if(linedata.length>1){
                    fillData.series[j].data.push(linedata[j+1]);
                  }
                }
            }
            console.log(fillData);
          }
          setOption();
        },
        timeout:30000,
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          console.log(errorThrown);
        }
    });
    function setOption(){
      option = {
          tooltip : {
              trigger: 'axis'
          },
          legend: {
              data: fillData.legend
          },
          toolbox: {
              show : true,
              feature : {
                  mark : {show: true},
                  dataView : {show: true, readOnly: false},
                  magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                  restore : {show: true},
                  saveAsImage : {show: true}
              }
          },
          calculable : true,
          xAxis : [
              {
                  type : 'category',
                  boundaryGap : false,
                  name : 'Time',
                  axisLabel:{
                    rotate: 60,
                    show : true
                  },
                  data : fillData.xAxis
              }
          ],
          yAxis : [
              {
                  type : 'value'
              }
          ],
          series : fillData.series
      };
      myChart.setOption(option);
    }
  };

  function loadIndex(){
      if (!(typeof C1Cache == "undefined" || C1Cache == null)) {
          var c = C1Cache.quotation[0].split(",");
          if (c.length < 8) {
              c = ["-", "-", "-", "-", "-", "-", "-"]
          }
          var type = loadclass(c[5], 0);
          var d = spanCache.replace(/{dqzs}/ig, c[2]);
          d = d.replace(/{zdqs}/ig, type == "green" ? " <span class=\"arr\">↓</span>" : " <span class=\"arr\">↑</span>");
          d = d.replace(/{zdzs}/ig, c[5]);
          d = d.replace(/{zdf}/ig, c[6]);
          d = d.replace(/{cje}/ig, !isNaN(c[3]) ? (parseFloat(c[3]) / 10000).toFixed(2) : c[3]);
          $("#shhq").addClass(type);
          $("#shhq").html(d);
          $("#shz").html(C1Cache.record[0].split(",")[0]);
          $("#shp").html(C1Cache.record[0].split(",")[1]);
          $("#shd").html(C1Cache.record[0].split(",")[2]);

          c = C1Cache.quotation[1].split(",");
          if (c.length < 8) {
              c = ["-", "-", "-", "-", "-", "-", "-"]
          }
          type = loadclass(c[5], 0);
          d = spanCache.replace(/{dqzs}/ig, c[2]);
          d = d.replace(/{zdqs}/ig, type == "green" ? " <span class=\"arr\">↓</span>" : " <span class=\"arr\">↑</span>");
          d = d.replace(/{zdzs}/ig, c[5]);
          d = d.replace(/{zdf}/ig, c[6]);
          d = d.replace(/{cje}/ig, !isNaN(c[3]) ? (parseFloat(c[3]) / 10000).toFixed(2) : c[3]);
          $("#szhq").addClass(type);
          $("#szhq").html(d);
          $("#szz").html(C1Cache.record[1].split(",")[0]);
          $("#szp").html(C1Cache.record[1].split(",")[1]);
          $("#szd").html(C1Cache.record[1].split(",")[2]);
      }
  }

  loadData();
  loadIndex();
  app.timeTicket = setInterval(function () {
      loadData();
      loadIndex();
  }, 40000);;

  //v_ff_sh600519="sh600519~329807.20~286575.00~43232.20~11.03~62191.34~105423.61~-43232.27~-11.03~391998.54~692375.6~656491.3~贵州茅台~20171026~20171025^76947.70^77916.50~20171024^98570.90^107125.60~20171023^80590.50^86211.80~20171020^106459.30^98662.40";
  //document.write(v_ff_sh600519.split("~"));
});
