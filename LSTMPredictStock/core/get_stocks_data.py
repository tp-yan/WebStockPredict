import json
import pandas_datareader.data as pdr
import fix_yahoo_finance as fix
import time
fix.pdr_override()

def get_stock_data(ticker, start_date, end_date):
    """
    Gets historical stock data of given tickers between dates
    :param ticker: company, or companies whose data is to fetched
    :type ticker: string or list of strings
    :param start_date: starting date for stock prices
    :type start_date: string of date "YYYY-mm-dd"
    :param end_date: end date for stock prices
    :type end_date: string of date "YYYY-mm-dd"
    :return: stock_data.csv
    """
    i = 1
    try:
        all_data = pdr.get_data_yahoo(ticker, start_date, end_date) #数据列包括：Date	Open	High	Low	Close	Adj Close	Volume
    except ValueError:
        print("ValueError, trying again")
        i += 1
        if i < 5:
            time.sleep(10)
            get_stock_data(ticker, start_date, end_date)
        else:
            print("Tried 5 times, Yahoo error. Trying after 2 minutes")
            time.sleep(120)
            get_stock_data(ticker, start_date, end_date)
    # print("date:%s - %s" % (start_date,end_date))
    # print("all_data:\n",all_data)
    # all_data.to_csv("stock_all_prices.csv")
    # stock_data = all_data["Adj Close"]
    stock_data = all_data
    filename = "..\\data\\"+ticker.lower()+"_stock.csv"
    stock_data.to_csv(filename)
    # insert_date_close_col(filename)

def insert_date_close_col(filename):
    with open(filename,"r+") as f:  # r只读，r+读写，不创建。文件不存在则报错
        old = f.read()      # 读取原来所有内容
        f.seek(0)           # 将文件索引重定位到文件头
        f.write("Date,Close\n")
        f.write(old)


if __name__ == "__main__":
    start_date = "2014-04-25"
    end_date = "2018-05-25"
    config = json.load(open("..\\config.json","r"))
    companies_name = config["companies"]["name"]
    print(companies_name)
    for name in companies_name:
        get_stock_data(name,start_date,end_date)
    print("finish!\n")