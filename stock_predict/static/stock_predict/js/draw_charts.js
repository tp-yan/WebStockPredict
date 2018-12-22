
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
        　　　　  fontSize:15
                }
            },
        tooltip : {
                    trigger: 'item'
                },
        xAxis: {
            type: 'category',
            data: [] // x轴名称
        },
        yAxis: {
            type: 'value',
            axisLabel : {
                formatter: '{value} 元'
            },
        },
        series: [
            {
            data: [],   // x坐标对应y值
            type: 'line',
            label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
            },
        ]
    };

    var min,max ;
    for(var i = 0 ; i < m_data.length; i++){
        var one_day = m_data[i];
        option['xAxis']['data'].push(one_day[0])
        option['series'][0]['data'].push(one_day[1].toFixed(2)) // toFixed(2)：保留两位小数（四舍五入）
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
            subtext:'综合评分' + (indexs[0]['zong_he']/11.0*10).toFixed(1),
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
                            formatter: (params)=>{
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
                            formatter: (params)=>{
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
                            formatter: (params)=>{
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


if(recent_data != null){
    draw_chart(recent_data,'history','过去20天股票数据');
}

if(predict_data != null){
    draw_chart(predict_data,'future','未来10天股票数据');
}

var ops = document.getElementById(stock_code);
ops.selected = true;

if(indexs != null){
    draw_radar();
}

/*
console.log(indexs[0]);
console.log(indexs[1]);
console.log(indexs[2]);
function test(){
    var test = echarts.init(document.getElementById('test'));
    var option = {
            title : {
                text: '罗纳尔多 vs 舍普琴科',
                subtext: '完全实况球员数据'
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                x : 'center',
                data:['罗纳尔多','舍普琴科']
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
                        {text : '进攻', max  : 100},
                        {text : '防守', max  : 100},
                        {text : '体能', max  : 100},
                        {text : '速度', max  : 100},
                        {text : '力量', max  : 100},
                        {text : '技巧', max  : 100}
                    ],
                    radius : 130
                }
            ],
            series : [
                {
                    name: '完全实况球员数据',
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
                            value : [97, 42, 88, 94, 90, 86],
                            name : '舍普琴科'
                        },
                        {
                            value : [97, 32, 74, 95, 88, 92],
                            name : '罗纳尔多'
                        }
                    ]
                }
            ]
        };
    test.setOption(option);
}
test();
*/

