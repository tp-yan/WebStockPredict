import json

from django.db import models


# Create your models here.
class Company(models.Model):
    stock_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

class HistoryData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    data = models.TextField() # 字符串类型
    start_date = models.DateField()

    def set_data(self,list_data):   # 将list类型数据，转为字符串存储
        self.start_date = list_data[0][0]   # 记录第一条数据的日期
        self.data = json.dumps(list_data)   # 可以将list或dict类型 转为字符串

    def get_data(self):
        return json.loads(self.data)    # 可以将字符串 转为list或dict类型

class PredictData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    data = models.TextField()  # 字符串类型
    start_date = models.DateField()

    def set_data(self, list_data):  # 将list类型数据，转为字符串存储
        self.start_date = list_data[0][0]  # 记录第一条数据的日期
        self.data = json.dumps(list_data)  # 可以将list或dict类型 转为字符串

    def get_data(self):
        return json.loads(self.data)  # 可以将字符串 转为list或dict类型
