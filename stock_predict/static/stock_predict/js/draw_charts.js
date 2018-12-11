
var companies = {"600718":"东软集团","000651":"格力电器","600839":"四川长虹","600320":"振华重工","601988":"中国银行",
                 "000066": "中国长城","601766":"中国中车","601390":"中国中铁","000768":"中航飞机","000063":"中兴通讯"};

function draw_chart(m_data,div_id,m_title){
    //初始化echarts实例
    var myChart = echarts.init(document.getElementById(div_id));
    // 指定图表的配置项和数据
     var option = {
       title: {
                text: companies[stock_code]+"("+stock_code+")" + m_title,
                textStyle:{
                //字体大小
        　　　　  fontSize:15
                }
            },
        xAxis: {
            type: 'category',
            data: [] // x轴名称
        },
        yAxis: {
            type: 'value',
            name:'单位：元'
        },
        series: [{
            name:'收盘价',
            data: [],   // x坐标对应y值
            type: 'line'
        }]
    };

    var min,max ;

    for(var i = 0 ; i < m_data.length; i++){
        var one_day = m_data[i];
        option['xAxis']['data'].push(one_day[0])
        option['series'][0]['data'].push(one_day[1])
        if(i == 0){
            min = max = one_day[1];
        }else{
            if(one_day[1] < min){
                min = one_day[1];
            }
            if(one_day[1] > max){
                max = one_day[1];
            }
        }

    }
    option['yAxis']['min'] = parseInt(min)-1;
    option['yAxis']['max'] = parseInt(max)+1;
    console.log(min);
    console.log(max);

    myChart.setOption(option);
}


if(recent_data != null){
    draw_chart(recent_data,'history','过去30天股票数据');
}

if(predict_data != null){
    draw_chart(predict_data,'future','未来30天股票数据');
}





