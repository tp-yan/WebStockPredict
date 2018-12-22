import json
from datetime import datetime, timedelta

from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from LSTMPredictStock import run
from .models import Company, HistoryData, PredictData, StockIndex
from .views import get_hist_predict_data,get_crawl_save_data
from .add_companies_to_db import add_company
from apscheduler.scheduler import Scheduler

class HistoryDataModelTests(TestCase):
    def test_set_data_with_not_list(self):
        """
        测试使用非list类型传入set_data，应该抛出异常
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


    def test_set_data(self):
        """
        测试正确调用set_data方法，验证HistoryData对象的属性data与start_date被修改
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
        测试使用非list类型传入set_data，应该抛出异常
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


    def test_set_data(self):
        """
        测试正确调用set_data方法，验证HistoryData对象的属性data与start_date被正确修改
        """
        pd = PredictData()
        list_data = [['2018-02-03', 1.2], ['2019-01-01', 10]]
        pd.set_data(list_data)
        self.assertEquals(pd.start_date, "2018-02-03")
        self.assertEquals(pd.data.replace(' ', ''), '[["2018-02-03",1.2],["2019-01-01",10]]')

    def test_get_data(self):
        """
        测试test_get_data返回的是list对象
        """
        pd = PredictData()
        list_data = [['2018-02-03',1.2], ['2019-01-01',10]]
        pd.set_data(list_data)
        self.assertEquals(pd.get_data(),list_data)


def create_company(stock_code,name):
    return Company.objects.create(stock_code=stock_code,name=name)

class HistPredictDataFun(TestCase):
    """
    测试 get_hist_predict_data 方法
    """
    def test_input_unknown_stock_code(self):
        """
        传入未知的stock_code， 返回404错误
        """
        stock_code = "10000"
        try:
            get_hist_predict_data(stock_code=stock_code)
        except Http404 as e:
            self.assertEquals(e.args[0],"No Company matches the given query.")

    def test_data_exist_in_db(self):
        """
        当数据库存在数据且为最新数据时，返回数据库中的数据
        """
        code = "600715"
        cp = create_company(stock_code=code,name="格力集团")
        # 构造最新历史、预测数据
        now = datetime.now()
        hist_data = [['2018-12-20',10],[str(now.date()),10.2]]
        pred_data = [[str(now.date()),10],[str(now.date()+timedelta(days=1)),10.2]]

        cp.historydata_set.create(data=json.dumps((hist_data)),start_date=hist_data[0][0])
        cp.predictdata_set.create(data=json.dumps((pred_data)),start_date=pred_data[0][0])

        recent,predict = get_hist_predict_data(stock_code=code)
        self.assertEquals(hist_data,recent)
        self.assertEquals(pred_data,predict)

    def test_data_not_exist_in_db(self):
        """
        测试当指定股票代码的历史数据和预测数据，在数据库中没有记录时，则从API获取历史数据，使用模型预测数据，然后保存到数据库
        """
        c = create_company(stock_code="000063",name="中兴通讯")
        self.assertEquals(c.historydata_set.count(),0)
        self.assertEquals(c.predictdata_set.count(),0)
        get_hist_predict_data(stock_code=c.stock_code)
        self.assertGreater(c.historydata_set.count(),0)
        self.assertGreater(c.predictdata_set.count(),0)

        now = datetime.now()
        if now.isoweekday() == 6:
            now = now + timedelta(days=2)
        elif now.isoweekday() == 7:
            now = now + timedelta(days=1)

        self.assertEquals(c.predictdata_set.first().start_date,str(now.date()))


    def test_get_data_exist_in_db(self):
        """
        测试当数据库所存数据不是最新时，应该将数据更新
        """
        cp = create_company(stock_code="000063", name="中兴通讯")
        # 构造过时历史、预测数据
        hist_data = [['2018-12-12', 10], ['2018-12-13', 10.2]]
        pred_data = [['2018-12-19', 10], ['2018-12-20', 10.2]]

        cp.historydata_set.create(data=json.dumps((hist_data)), start_date=hist_data[0][0])
        cp.predictdata_set.create(data=json.dumps((pred_data)), start_date=pred_data[0][0])
        get_hist_predict_data(stock_code=cp.stock_code)

        hd_new = cp.historydata_set.last()
        hd_last_time = datetime.strptime(hd_new.get_data()[-1][0],"%Y-%m-%d")
        pd_new = cp.predictdata_set.last()
        pd_last_time = datetime.strptime(pd_new.start_date, "%Y-%m-%d")
        self.assertGreater(hd_last_time,datetime.strptime(hist_data[1][0],"%Y-%m-%d"))
        self.assertGreater(pd_last_time,datetime.strptime(pred_data[0][0],"%Y-%m-%d"))

class FuncAddCompany2DB(TestCase):
    def test_add_company(self):
        """
        测试调用该方法，数据库成功添加了股票公司数据
        """
        companies = Company.objects.all()
        self.assertQuerysetEqual(companies,[])
        add_company()
        self.assertEquals(Company.objects.count(),10)
        self.assertEquals(Company.objects.first().stock_code,'600718')
        self.assertEquals(Company.objects.first().name,'东软集团')

# 为公司创造指标数据
def create_stock_index(company):
    row = {'ri_qi': '2018-12-22', 'zi_jin': 8, 'qiang_du': 6, 'feng_xian': 8, 'zhuan_qiang': 5, 'chang_yu': 4,
           'jin_zi': 7,
           'zong_he': 9}
    row2 = {'ri_qi': '2018-12-22', 'zi_jin': 5, 'qiang_du': 7, 'feng_xian': 8, 'zhuan_qiang': 5, 'chang_yu': 7,
            'jin_zi': 6,
            'zong_he': 7}
    row3 = {'ri_qi': '2018-12-22', 'zi_jin': 8, 'qiang_du': 6, 'feng_xian': 5, 'zhuan_qiang': 4, 'chang_yu': 6,
            'jin_zi': 5,
            'zong_he': 8}
    stock_index = company.stockindex_set.create(ri_qi=row['ri_qi'], zi_jin=row['zi_jin'], qiang_du=row['qiang_du'],
                            feng_xian=row['feng_xian'],
                            zhuan_qiang=row['zhuan_qiang'], chang_yu=row['chang_yu'], jin_zi=row['jin_zi'],
                            zong_he=row['zong_he'])
    company.stockindex_set.create(ri_qi=row2['ri_qi'], zi_jin=row2['zi_jin'], qiang_du=row2['qiang_du'],
                            feng_xian=row2['feng_xian'],
                            zhuan_qiang=row2['zhuan_qiang'], chang_yu=row2['chang_yu'], jin_zi=row2['jin_zi'],
                            zong_he=row2['zong_he'])
    company.stockindex_set.create(ri_qi=row3['ri_qi'], zi_jin=row3['zi_jin'], qiang_du=row3['qiang_du'],
                            feng_xian=row3['feng_xian'],
                            zhuan_qiang=row3['zhuan_qiang'], chang_yu=row3['chang_yu'], jin_zi=row3['jin_zi'],
                            zong_he=row3['zong_he'])
    return stock_index

# 为股票创造最新的历史与预测数据
def create_last_hist_predict_data(company):
    now = datetime.now()
    hist_data = [[str(now.date() + timedelta(days=-1)), 10], [str(now.date()), 10.2]]
    pred_data = [[str(now.date()), 10], [str(now.date() + timedelta(days=1)), 10.2]]

    company.historydata_set.create(data=json.dumps(hist_data), start_date=hist_data[0][0])
    company.predictdata_set.create(data=json.dumps(pred_data), start_date=pred_data[0][0])

    return hist_data,pred_data
class HomeView(TestCase):
    def test_return_data(self):
        """
        测试访问主页时，返回股票代码为：600718的数据，包括：历史、预测和指标数据
        """
        # 构造最新历史、预测数据
        cp = create_company(stock_code="600718", name="东软集团")
        hist_data,pred_data = create_last_hist_predict_data(cp)
        stock_index = create_stock_index(cp)

        response = self.client.get(reverse('stock_predict:home'))
        self.assertEquals(response.status_code,200)
        self.assertContains(response,'data')
        self.assertContains(response,cp.stock_code)
        self.assertContains(response,str(hist_data[0][0]))
        self.assertContains(response,str(pred_data[0][0]))
        self.assertContains(response,stock_index.ri_qi)
        self.assertContains(response,stock_index.zi_jin)
        self.assertContains(response,stock_index.jin_zi)
        self.assertContains(response,stock_index.zong_he)


class PredictStockAction(TestCase):
    def test_predict_not_exist_stock(self):
        """
        预测不存在的股票代码，返回404
        """
        url = reverse('stock_predict:predict')
        response = self.client.post(url,data={"stock_code":"000000"})
        self.assertEquals(response.status_code,404)

    def test_predict_stock(self):
        """
        测试输入正确的股票代码时，应该返回该股票的历史、预测、指标数据
        """
        cp = create_company(stock_code="000651", name="格力电器")
        hist_data,pred_data = create_last_hist_predict_data(cp)
        stock_index = create_stock_index(cp)

        url = reverse('stock_predict:predict')
        response = self.client.post(url, data={"stock_code": cp.stock_code})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,str(hist_data[0][0]))
        self.assertContains(response,str(pred_data[0][0]))
        self.assertContains(response,stock_index.ri_qi)
        self.assertContains(response,stock_index.zi_jin)
        self.assertContains(response,stock_index.jin_zi)
        self.assertContains(response,stock_index.zong_he)


class FuncGetCrawlSaveData(TestCase):
    """
    测试方法 get_crawl_save_data
    """
    def test_get_crawl_save_data(self):
        """
        测试调用该方法，数据库增加了 StockIndex 数据
        """
        stock_codes = {"600718":"东软集团","000651":"格力电器","600839":"四川长虹","600320":"振华重工","601988":"中国银行",
                 "000066": "中国长城","601766":"中国中车","601390":"中国中铁","000768":"中航飞机","000063":"中兴通讯"}
        for code,name in stock_codes.items():
            create_company(stock_code=code,name=name)
        self.assertEquals(StockIndex.objects.count(),0)
        get_crawl_save_data()
        self.assertGreater(StockIndex.objects.count(),0)

class TrainAllModel(TestCase):
    def test_train_all_models(self):
        """
        测试训练所有的模型
        """
        self.assertEquals(run.train_all_stock(),0)

class PredictAllData(TestCase):
    def test_predict_all(self):
        """
        测试预测所有数据的方法
        """
        self.assertIsNotNone(run.predict_all_stock())

# sched = Scheduler()




