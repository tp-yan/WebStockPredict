import json

from django.db import models


# Create your models here.
class Company(models.Model):
    stock_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

class StockIndex(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ri_qi = models.CharField(max_length=30)
    zi_jin = models.IntegerField(default=0)
    qiang_du = models.IntegerField(default=0)
    feng_xian = models.IntegerField(default=0)
    zhuan_qiang = models.IntegerField(default=0)
    chang_yu = models.IntegerField(default=0)
    jin_zi = models.IntegerField(default=0)
    zong_he = models.IntegerField(default=0)


class HistoryData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    data = models.TextField() # 字符串类型
    start_date = models.CharField(max_length=30)

    def set_data(self,list_data):   # 将list类型数据，转为字符串存储
        try:
            start_da = list_data[0][0]  # 记录第一条数据的日期
            data_json = json.dumps(list_data)  # 可以将list或dict类型 转为字符串
        except (KeyError,TypeError,IndexError):
            raise Exception("list_data must be 2 dimensions list.")
        else:
            self.start_date = start_da
            self.data = data_json

    def get_data(self):
        return json.loads(self.data)        # 可以将字符串 转为list或dict类型

class PredictData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    data = models.TextField()  # 字符串类型
    start_date = models.CharField(max_length=30)

    def set_data(self, list_data):  # 将list类型数据，转为字符串存储
        try:
            st_da = list_data[0][0]  # 记录第一条数据的日期
            data_json = json.dumps(list_data)  # 可以将list或dict类型 转为字符串
        except (KeyError,TypeError):
            raise Exception("list_data must be 2 dimensions list.")
        else:
            self.start_date = st_da
            self.data = data_json

    def get_data(self):
        return json.loads(self.data)  # 可以将字符串 转为list或dict类型
