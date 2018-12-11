import json

from django.http import HttpResponse
from django.shortcuts import render
from LSTMPredictStock import run

# Create your views here.

def get_hist_predict_data(stock_code):
    recent_data = run.get_hist_data(stock_code)
    predict_data = run.prediction(stock_code)
    return recent_data,predict_data

def home(request):
    recent_data,predict_data = get_hist_predict_data("600718")
    data = {"recent_data":recent_data,"stock_code":"600718","predict_data":predict_data}
    return render(request,"stock_predict/home.html",{"data":json.dumps(data)}) # json.dumps(list)

def predict_stock_action(request):
    stock_code = request.POST.get('stock_code',None)
    print("stock_code:\n",stock_code)
    recent_data, predict_data = get_hist_predict_data(stock_code)
    data = {"recent_data": recent_data, "stock_code": stock_code, "predict_data": predict_data}
    return render(request, "stock_predict/home.html", {"data": json.dumps(data)})  # json.dumps(list)