from django.test import TestCase
from .models import Company,HistoryData,PredictData
# Create your tests here.

def create_company(stock_code,name):
    """
    :param stock_code:股票代码
    :param name: 公司名字
    :return: 临时数据库中的一个Company对象
    """
    return Company.objects.create(stock_code=stock_code,name=name)

def create_history_data(company,data):
    """

    :param company: 外键
    :param data: 要保存的历史数据
    :return:
    """
    hd = HistoryData()
    hd.company = company
    hd.data = data

    return HistoryData.objects.create(company=company,data=data)

class HistoryDataModelTests(TestCase):
    def test_set_data_with_not_list(self):
        """
        使用非list类型传入set_data
        """
        data = {'data':'aa'}
        hd = HistoryData()
        self.assertRaises(KeyError,hd.set_data(data))