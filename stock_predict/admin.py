from django.contrib import admin
from .models import Company,HistoryData,PredictData
# Register your models here.

admin.site.register(Company)
admin.site.register(HistoryData)
admin.site.register(PredictData)