# WebStockPredict
此project是基于django的web app。它能给出指定范围内公司(此处为10个)的历史股票数据与未来某段时间的预测数据以及对该股票的一些评价指标。
股票预测模型是使用[jaungiers](https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction)提出的一种LSTM Neural Network模型。
并使用以tensorflow作为backend的keras来搭建、训练模型

## 运行项目
### 环境要求
如果只运行web项目，则只需安装如下：
+ python 3.6.x
+ django 2.1.4
+ pandas 0.23.4
+ numpy 1.15.2

如果需要训练模型或者使用模型来预测(注：需要保证本机拥有 NVIDIA GPU以及显卡驱动)，则还需要安装：
+ tensorflow-gpu 1.10.0
+ cudnn 7.1.4
+ cudatoolkit 9.0 
+ keras 2.2.2
+ matplotlib 2.2.2 

### 使用django自带的服务器在本地运行
首先你需要将此项目clone或者download到本地。然后在控制台，进入项目根目录即WebStockPredict(包含有manage.py的目录)，输入如下面命令，启动Web应用：

`python manage.py runserver`

当控制台输出如下内容时，证明Web项目已成功启动:
```
Using TensorFlow backend.
System check identified no issues (0 silenced).
December 24, 2018 - 19:57:52
Django version 2.1.4, using settings 'WebStockPredict.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
此时在浏览器中输入：`http://http://127.0.0.1:8000/stock_predict/home/`即可访问应用，可以选择。
![home page](/display_img/home.png "股票预测系统首页")

## 数据说明
本项目为了演示方便，只使用了10个公司的股票数据来进行模型训练，实际上可以依据个人需求，训练成百上千个公司的数据。
获取国内上市公司历史股票数据来源于网易的API：'http://quotes.money.163.com/service/chddata.html'，
详细使用请参考[数据接口-免费版（股票数据API）](https://blog.csdn.net/llingmiao/article/details/79941066)

