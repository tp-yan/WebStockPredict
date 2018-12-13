import json

from django.http import HttpResponse
from django.shortcuts import render
from LSTMPredictStock import run
from stock_predict import models
from datetime import datetime as dt
# Create your views here.

def get_hist_predict_data(stock_code):
    recent_data,predict_data = None,None

    company = models.Company.objects.get(stock_code=stock_code)

    # recent_data = run.get_hist_data(stock_code)

    if company.historydata_set.count() <= 0:
        history_data = models.HistoryData()
        history_data.company = company
        history_data.set_data(run.get_hist_data(stock_code))
        history_data.save()
        recent_data = history_data.get_data()
    else:
        all_data = company.historydata_set.all()
        for single in all_data:
            now = dt.now()
            start_date = dt.strptime(single.start_date,"%Y-%m-%d")
            if now.date() > start_date.date():  # 更新预测数据
                single.set_data(run.get_hist_data(stock_code))
                single.save()

            recent_data = single.get_data()
            break

    if company.predictdata_set.count() <= 0:
        predict_data = models.PredictData()
        predict_data.company = company
        predict_data.set_data(run.prediction(stock_code,pre_len=10))
        predict_data.save()
        predict_data = predict_data.get_data()
    else:
        all_data = company.predictdata_set.all()
        for single in all_data:
            now = dt.now()
            start_date = dt.strptime(single.start_date,"%Y-%m-%d")
            if now.date() > start_date.date():  # 更新预测数据
                single.set_data(run.prediction(stock_code, pre_len=10))
                single.save()

            predict_data = single.get_data()
            break

    return recent_data,predict_data

def home(request):
    recent_data,predict_data = get_hist_predict_data("600718")
    data = {"recent_data":recent_data,"stock_code":"600718","predict_data":predict_data}
    print(recent_data)
    return render(request,"stock_predict/home.html",{"data":json.dumps(data)}) # json.dumps(list)

def predict_stock_action(request):
    stock_code = request.POST.get('stock_code',None)
    print("stock_code:\n",stock_code)
    recent_data, predict_data = get_hist_predict_data(stock_code)
    data = {"recent_data": recent_data, "stock_code": stock_code, "predict_data": predict_data}
    return render(request, "stock_predict/home.html", {"data": json.dumps(data)})  # json.dumps(list)