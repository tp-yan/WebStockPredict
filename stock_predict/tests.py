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


class HistoryDataModelTests(TestCase):
    def test_set_data_with_not_list(self):
        """
        使用非list类型传入set_data
        """
        hd = HistoryData()
        # 测试函数hd.set_data（list_data=data）Raises Exception，并且包含指定报错msg
        try:
            hd.set_data(list_data={'data':'aa'})
        except Exception as e:
            self.assertEquals(e.args[0],"list_data must be 2 dimensions list.") # e.args:tuple
        try:
            hd.set_data(list_data=123)
        except Exception as e:
            self.assertEquals(e.args[0],"list_data must be 2 dimensions list.") # e.args:tuple
        try:
            hd.set_data(list_data='data')
        except Exception as e:
            self.assertEquals(e.args[0],"list_data must be 2 dimensions list.") # e.args:tuple
        try:
            hd.set_data(list_data=["2018-01-12",90])
        except Exception as e:
            self.assertEquals(e.args[0],"list_data must be 2 dimensions list.") # e.args:tuple


    def test_set_data(self):
        """
        正常调用set_data方法，验证HistoryData对象的data与start_date
        """
        hd = HistoryData()
        list_data = [['2018-02-03',1.2],['2019-01-01',10]]
        hd.set_data(list_data)
        self.assertEquals(hd.start_date,"2018-02-03")
        self.assertEquals(hd.data.replace(' ',''),'[["2018-02-03",1.2],["2019-01-01",10]]')

    def test_get_data(self):
        """
        测试test_get_data返回 list对象
        """
        hd = HistoryData()
        list_data = [['2018-02-03', 1.2], ['2019-01-01', 10]]
        hd.set_data(list_data)
