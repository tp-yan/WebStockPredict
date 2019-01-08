
var companies = {"600718":"东软集团","000651":"格力电器","600839":"四川长虹","600320":"振华重工","601988":"中国银行",
                 "000066": "中国长城","601766":"中国中车","601390":"中国中铁","000768":"中航飞机","000063":"中兴通讯"};

function draw_chart(){
    //初始化echarts实例
    var myChart = echarts.init(document.getElementById("hist_futu"));

    // 指定图表的配置项和数据
     var option = {
        title: {
                text: companies[stock_code]+"("+stock_code+")" + "过去20天历史数据以及未来10天预测数据",
                textStyle:{
        　　　　  fontSize:15
                }
            },
        tooltip : {
                    trigger: 'item'
                },
        legend: {
                x : 'center',
                data:['过去20天','未来10天']
            },
        //工具框，可以选择
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            axisLabel: {
                rotate: 30,
                interval: 0
            },
            type: 'category',
            //boundaryGap: false,
            data: [] // x轴名称
        },
        yAxis: {
                type: 'value',
                axisLabel : {
                    formatter: '{value} 元'
                },
            }
        ,
        series: [
            {
            name:'过去20天',
            type: 'line',
            color:['#FF0000'],
            data: [],   // x坐标对应y值
            itemStyle : { normal: {label : {show: true}}},
            label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
            },
            {
            name:'未来10天',
            data: [],   // x坐标对应y值
            itemStyle : { normal: {label : {show: true}}},
            type: 'line',
            label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
            color:['#0000FF'],
            },
        ]
    };

    var min,max;
    for(var k=0; k <= 1; k++){
        if(k == 0){
            m_data = recent_data;
        }else{
            m_data = predict_data;
        }
        for(var i = 0 ; i < m_data.length; i++){
            var one_day = m_data[i];
            option['xAxis']['data'].push(one_day[0])
            if(k==0){
                option['series'][1]['data'].push(null);
            }
            option['series'][k]['data'].push(one_day[1].toFixed(2)) // toFixed(2)：保留两位小数（四舍五入）

            if(i == 0 && k == 0){
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
    }

    option['yAxis']['min'] = parseInt(min);
    option['yAxis']['max'] = parseInt(max)+1;

    myChart.setOption(option);
}


//绘制雷达图
function draw_radar(){
    var radar = echarts.init(document.getElementById('radar'));
    var option = {
        title : {
            text: '近3个交易日综合评分',
            subtext:'综合评分' + (indexs[0]['zong_he']/11.0*100).toFixed(1),
            subtextStyle : {
            color :'red',
            fontStyle :'normal',
            fontWeight :'bold',
            fontFamily :'sans-serif',
            fontSize :'16'
            },
            itemGap:20,
            padding:[0,15,15,15]
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:[indexs[0]['ri_qi'],indexs[1]['ri_qi'],indexs[2]['ri_qi']]  //此处为legend名字，须与series的data每个name相同
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                    {text : '资金', max  : 11},
                    {text : '强度', max  : 11},
                    {text : '风险', max  : 11},
                    {text : '转强', max  : 11},
                    {text : '长预', max  : 11},
                    {text : '近资', max  : 11}
                ],
                radius : 130
            }
        ],
        series : [
            {
                name: '各交易日数据对比',   //数据视图显示的标题
                type: 'radar',
                itemStyle: {
                    normal: {
                        areaStyle: {
                            type: 'default'
                        }
                    }
                },
                data : [
                    {
                        value : [9, 4, 8, 9, 9, 8],
                        name : '12-09',
                         //在拐点处显示数值
                        label: {
                            normal: {
                            show: true,
                            formatter: function(params){
                                return params.value
                               },
                            },
                        }
                    },
                    {
                        value : [9, 3, 7, 9, 8, 9],
                        name : '12-11',
                         label: {
                            normal: {
                            show: true,
                            formatter: function(params){
                                return params.value
                               },
                            },
                        }
                    },
                    {
                        value : [9, 3, 7, 9, 8, 9],
                        name : '12-12',
                         label: {
                            normal: {
                            show: true,
                            formatter: function(params){
                                return params.value
                               },
                            },
                        }
                    }
                ]
            }
        ]
    };

    for(var i = 0 ; i < 3;i++){
        option['series'][0]['data'][i]['value'] = [];
        option['series'][0]['data'][i]['value'].push(indexs[i]['zi_jin']);
        option['series'][0]['data'][i]['value'].push(indexs[i]['qiang_du']);
        option['series'][0]['data'][i]['value'].push(indexs[i]['feng_xian']);
        option['series'][0]['data'][i]['value'].push(indexs[i]['zhuan_qiang']);
        option['series'][0]['data'][i]['value'].push(indexs[i]['chang_yu']);
        option['series'][0]['data'][i]['value'].push(indexs[i]['jin_zi']);
        option['series'][0]['data'][i]['name'] = indexs[i]['ri_qi'];
    }
    radar.setOption(option);
}


if(recent_data != null && predict_data != null){
    draw_chart();
}

var ops = document.getElementById(stock_code);
ops.selected = true;

if(indexs != null){
    draw_radar();
}
