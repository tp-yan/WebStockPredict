from django.http import HttpResponse
from django.shortcuts import render
from LSTMPredictStock import run

# Create your views here.

def home(request):
    # data = run.get_hist_data("000063")
    # print("最近30天股票数据：\n",data)
    # print("未来30天预测数据：\n",run.prediction("000063"))
    return render(request,"stock_predict/home.html",{"data":None})

def predict_stock_action(request):
    stock_code = request.POST.get('stock_code',None)
    print("stock_code:\n",stock_code)
    return HttpResponse(stock_code)