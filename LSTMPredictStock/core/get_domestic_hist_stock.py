# 获取国内股票历史数据
import json
import os
import requests
from datetime import datetime,timedelta

def get_domestic_stock(sticker_code, start_date, end_date):
    # 从网易接口获取数据
    api_adr = 'http://quotes.money.163.com/service/chddata.html'
    fields = "TOPEN;TCLOSE;HIGH;LOW;VOTURNOVER"
    # 注意：获取上海证券与深圳证券股票的数据，需要构造不同的URL
    tag = "0"       # 上海证券
    if sticker_code in ['000063','000066','000768','000651']:
        tag = "1"   # 深圳证券

    params = {'code': tag + sticker_code, 'start': start_date, 'end': end_date, 'fields': fields}
    r = requests.get(api_adr, params=params)

    print(r.url)
    txt_list = r.text.split('\n')   # r.content二进制数据    r.text 文本数据
    txt_list.reverse()
    txt_list[0] = txt_list[-1]  # 列名替换开头的空字符
    col_name = "Date,Code,Name,Open,Close,High,Low,Volume\n"
    txt_list[0] = col_name
    txt_list.pop(-1)

    root = os.path.dirname(os.path.dirname(__file__))
    dir_path = os.path.join(root,"data")
    filename = sticker_code + ".csv"
    print(os.path.join(dir_path,filename))
    with open(os.path.join(dir_path,filename), "w+", encoding='utf-8') as f:
        for line in txt_list:
            if line.split(',')[3] != '0.0':     # 去除无效数据
                f.write(line)


def get_all_last_data(start_date): # 得到从start_date至今日 所有最新数据
    root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(root,"config.json")

    configs = json.load(open(config_path, 'r'))
    companies = configs['companies']

    # start_date = '2010-06-21'  # 只能按整年获取至今日数据
    cur = datetime.now()
    year = timedelta(days=365)
    cur = cur + year    # 在当前日期上加一年
    end_date = cur.strftime("%Y-%m-%d")  # 获取今年最新数据

    for code, company_name in companies.items():
        get_domestic_stock(code, start_date, end_date)

def get_single_last_data(stock_code,start_date="2010-01-01"):
    # start_date = '2010-06-21'  # 只能按整年获取至今日数据
    cur = datetime.now()
    year = timedelta(days=365)
    cur = cur + year  # 在当前日期上加一年
    end_date = cur.strftime("%Y-%m-%d")  # 获取今年最新数据

    get_domestic_stock(stock_code, start_date, end_date)


if __name__ == '__main__':
    get_all_last_data("2010-01-01")
