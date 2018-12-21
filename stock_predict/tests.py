import json

from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from .models import Company, HistoryData, PredictData
from .views import get_hist_predict_data

# Create your tests here.

def create_company(stock_code, name):
    """
    :param stock_code:股票代码
    :param name: 公司名字
    :return: 临时数据库中的一个Company对象
    """
    return Company.objects.create(stock_code=stock_code, name=name)


class HistoryDataModelTests(TestCase):
    def test_set_data_with_not_list(self):
        """
        使用非list类型传入set_data
        """
        hd = HistoryData()
        # 测试函数hd.set_data（list_data=data）Raises Exception，并且包含指定报错msg
        try:
            hd.set_data(list_data={'data': 'aa'})
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            hd.set_data(list_data=123)
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            hd.set_data(list_data='data')
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            hd.set_data(list_data=["2018-01-12", 90])
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple

    def test_set_data(self):
        """
        正常调用set_data方法，验证HistoryData对象的data与start_date
        """
        hd = HistoryData()
        list_data = [['2018-02-03', 1.2], ['2019-01-01', 10]]
        hd.set_data(list_data)
        self.assertEquals(hd.start_date, "2018-02-03")
        self.assertEquals(hd.data.replace(' ', ''), '[["2018-02-03",1.2],["2019-01-01",10]]')

    def test_get_data(self):
        """
        测试test_get_data返回 list对象
        """
        hd = HistoryData()
        list_data = [['2018-02-03',1.2], ['2019-01-01',10]]
        hd.set_data(list_data)
        self.assertEquals(hd.get_data(),list_data)

class PredictDataModelTests(TestCase):
    def test_set_data_with_not_list(self):
        """
        使用非list类型传入set_data
        """
        pd = PredictData()
        # 测试函数hd.set_data（list_data=data）Raises Exception，并且包含指定报错msg
        try:
            pd.set_data(list_data={'data': 'aa'})
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            pd.set_data(list_data=123)
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            pd.set_data(list_data='data')
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple
        try:
            pd.set_data(list_data=["2018-01-12", 90])
        except Exception as e:
            self.assertEquals(e.args[0], "list_data must be 2 dimensions list.")  # e.args:tuple

    def test_set_data(self):
        """
        正常调用set_data方法，验证HistoryData对象的data与start_date
        """
        pd = PredictData()
        list_data = [['2018-02-03', 1.2], ['2019-01-01', 10]]
        pd.set_data(list_data)
        self.assertEquals(pd.start_date, "2018-02-03")
        self.assertEquals(pd.data.replace(' ', ''), '[["2018-02-03",1.2],["2019-01-01",10]]')

    def test_get_data(self):
        """
        测试test_get_data返回 list对象
        """
        pd = PredictData()
        list_data = [['2018-02-03',1.2], ['2019-01-01',10]]
        pd.set_data(list_data)
        self.assertEquals(pd.get_data(),list_data)


def create_company(stock_code,name):
    return Company.objects.create(stock_code=stock_code,name=name)

class HistPredictDataFun(TestCase):
    """
    测试get_hist_predict_data方法
    """
    def test_get_hist_predict_data_unknown_stock_code(self):
        """
        传入未知stock_code， 返回404错误
        """
        stock_code = "10000"
        try:
            get_hist_predict_data(stock_code=stock_code)
        except Http404 as e:
            self.assertEquals(e.args[0],"No Company matches the given query.")

    # def test_get_data_not_exist_in_db(self):
    #     """
    #     指定股票代码的历史数据和预测数据，在数据库中没有记录时，从API获取历史数据，并使用模型预测数据
    #     最后将它们存入数据库
    #     """
    #     c = create_company(stock_code="000063",name="中华")
    #     re_data,pre_data = get_hist_predict_data(stock_code=c.stock_code)
    #     self.assertNotEquals(re_data,None)
    #     self.assertNotEquals(pre_data,None)
    #     self.assertEquals(re_data,c.historydata_set.first().get_data())
    #     self.assertEquals(pre_data,c.predictdata_set.first().get_data())
    #     self.assertGreater(HistoryData.objects.count(),0)
    #     self.assertGreater(PredictData.objects.count(),0)

    def test_get_data_exist_in_db(self):
        """
        指定股票代码的历史数据和预测数据已保存在数据库，应该正常被读取
        """
        c = create_company(stock_code="000063", name="中华")
        data1 = r"[['2018-02-12',19],['2018-02-13',20.1]]"
        start_date1 = r'2018-02-12'
        data2 = r"[['2018-02-14',20.5],['2018-02-15',21.1]]"
        start_date2 = r'2018-02-14'
        hd = c.historydata_set.create(data=json.dumps(data1),start_date=start_date1)
        pd = c.predictdata_set.create(data=json.dumps(data2),start_date=start_date2)
        self.assertGreater(c.historydata_set.count(),0)
        self.assertGreater(c.predictdata_set.count(),0)
        re_data, pre_data = get_hist_predict_data(stock_code=c.stock_code)
        self.assertEquals(re_data,hd.get_data())
        self.assertEquals(pre_data,pd.get_data())


class HomeView(TestCase):
    def test_return_data(self):
        """
        测试正确返回历史与预测数据
        """
        c = create_company(stock_code="600718", name="东软集团")
        data1 = r"[['2018-02-12',19],['2018-02-13',20.1]]"
        start_date1 = r'2018-02-12'
        data2 = r"[['2018-02-14',20.5],['2018-02-15',21.1]]"
        start_date2 = r'2018-02-14'
        hd = c.historydata_set.create(data=json.dumps(data1), start_date=start_date1)
        pd = c.predictdata_set.create(data=json.dumps(data2), start_date=start_date2)
        response = self.client.get(reverse('stock_predict:home'))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,'data')
        self.assertContains(response,c.stock_code)
        self.assertContains(response,data1)
        self.assertContains(response,data2)

class PredictStockAction(TestCase):
    pass