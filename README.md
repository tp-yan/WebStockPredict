# WebStockPredict
此project是基于django的web app。它能给出指定范围内公司(此处为10个)的历史股票数据与未来某段时间的预测数据以及对该股票的一些评价指标。
股票预测模型是使用[jaungiers](https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction)提出的一种LSTM Neural Network模型。
并使用以tensorflow作为backend的keras来搭建、训练模型。

## 目录说明
+ display_img:保存演示图片
+ htmlcov:使用coverage.py集成测试，自动生成的文件夹
+ LSTMPredictStock:包含了有关模型的一切，包括训练数据及其获取代码，模型搭建、训练的代码、训练好的模型以及关于该python包的配置文件config.json
+ stock_predict:基于django开发框架的Web app，包含了一个web应用的相关内容。
+ WebStockPredict:包含了对django project进行管理、配置的程序
+ db.sqlite3:此Web应用所需的数据就存放在sqlite3数据库中
+ manage.py:管理django project的快捷API

## 运行项目
### 环境要求
如果只运行web项目，则只需安装如下包：
+ python 3.6.x
+ django >= 2.1.4 （或者使用conda安装最新版）
+ pandas >= 0.23.4 （或者使用conda安装最新版）
+ numpy >= 1.15.2 （或者使用conda安装最新版）
+ apscheduler = 2.1.2 （请用pip install apscheduler==2.1.2 安装，conda装的版本不兼容）

如果需要训练模型或者使用模型来预测(注：需要保证本机拥有 NVIDIA GPU以及显卡驱动)，则还需要安装：
+ tensorflow-gpu >= 1.10.0 （可以使用conda安装最新版。如用conda安装，cudatoolkit和cudnn会被自动安装）
+ cudatoolkit >= 9.0 （根据自己本机的显卡型号决定，请去NVIDIA官网查看）
+ cudnn >= 7.1.4 （版本与cudatoolkit9.0对应的，其他版本请去NVIDIA官网查看对应的cudatoolkit版本）
+ keras >= 2.2.2 （可以使用conda安装最新版）
+ matplotlib >=  2.2.2  （可以使用conda安装最新版）

或者可以通过控制台在根目录路径下输入：`pip install -r requirements.txt`安装上述所有包（注意修改cudatoolkit和cudnn的版本与自己电脑的GPU型号一致）。
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
此时在浏览器中输入：`http://http://127.0.0.1:8000/stock_predict/home/`即可访问应用，通过下拉框选择查看某个公司过去20天的历史股票数据和未来10天的预测数据。
![home page](/display_img/home.png "股票预测系统首页")

**注：在Web app中绘制的10天预测数据，大多都是朝着一个方向变化。这是因为股票数据是一个随机过程，无法使用既有的模型去准确预测未来一段时间的数据，只能给出股票未来变化的趋势。
在我们使用[jaungiers](https://www.altumintelligence.com/articles/a/Time-Series-Prediction-Using-LSTM-Deep-Neural-Networks)提出的模型中他详细阐述了这个问题。
我们预测输出符合他给出的实验图，如下：**
![multi-sequence](/display_img/multi-sequence.png "多段预测输出")

## 数据
本项目为了演示方便，只使用了10个公司的股票数据来进行模型训练，实际上可以依据个人需求，训练成百上千个公司的数据。
*注：这个项目只是用来演示，并不保证预测的真实性，请勿用于真实炒股*

### 数据来源
+ #### 训练数据
训练模型的数据，即10个公司的历史股票数据。获取国内上市公司历史股票数据来源于网易的API：'http://quotes.money.163.com/service/chddata.html'，
详细使用请参考[数据接口-免费版（股票数据API）](https://blog.csdn.net/llingmiao/article/details/79941066)。
在LSTMPredictStock/core/get_domestic_hist_stock.py 中`get_domestic_stock(sticker_code, start_date, end_date):`
函数用于获取10个公司起始至终止日期的股票数据，并以csv格式保存在 LSTMPredictStock/data下。csv格式方便用pandas读取，输入到LSTM神经网络模型，
用于训练模型以及预测股票数据。
+ #### 股票指标数据
我们的Web app，还给出了每个公司的股票评价指标。这些数据是从[数据猫](http://www.gpdatacat.com/)的网站上爬取的，在数据猫的网站上给出了股票的很多项评价指标（如下图），
而我们只选择了其中几个评价指标来展示。爬虫程序：stock_predict/get_stock_index.py，调用`main(stockcode)`方法可以获得指定股票代码的评价指标数据，
它会在stock_predict下创建stock_index文件夹，以csv格式保存爬取的数据。另外，需要注意的是，因为数据猫需要用户登录以后才能查看相应的股票数据，所以在
运行get_stock_index.py时，需要自己先在浏览器登录数据猫后，得到cookie中的参数（按F12，选择Application选项卡即可看到，如下图），
然后在get_stock_index.py中修改下面代码块中对应的字符串变量‘+’后面的值

![cookie](/display_img/cookie.png "获取cookie参数")
```
UM_distinctid = "UM_distinctid=" + "167d4244a665d3-0bc7b9a22f42f1-4313362-144000-167d4244a67440;"
PHPSESSID = "PHPSESSID=" + "4j67ed7bo6ogs6ntjmo3fb62n4;"
CNZZDATA1256448133 = "CNZZDATA1256448133=" + "1846506456-1545449269-%7C1545479258;"
amvid = "amvid=" + "6447ffafff063060f1a560d94128a33f"
cookie={'Cookie':UM_distinctid+PHPSESSID+CNZZDATA1256448133+amvid}
```
![data_cat](/display_img/data_cat.png "股票评价指标")

### 训练模型
1. 调用run.py中的`train_all_stock`，它首先会调用`get_all_last_data(start_date="2010-01-01")`方法获得10个公司从2010年至今年的历史数据
2. 接着调用的`train_model(stock_code, predict=False)`方法基于上述数据来训练模型，若predict=True，则在训练完后会进行模型正确性的验证，
主要是通过绘图方式来对比预测数据与真实数据之间的吻合度
3. 并分别将10个公司的训练好的模型保存于LSTMPredictStock/saved_models下（'xxx.h5'格式），用于后续恢复模型来预测数据

### 预测股票数据
1. 调用run.py中的`predict_all_stock(pre_len=10)`来对10个公司的股票进行预测，pre_len指定预测的天数，默认是10天
2. 上一步调用的函数实际上调用了`prediction(stock_code, real=True, pre_len=30, plot=False)`来完成预测。
在` model.load_model(file_path)`这里恢复了模型。它默认使用每个公司近30天的历史数据作为模型输入来得到pre_len天的预测数据


### 项目测试
#### 单元测试
使用django自带的测试工具来实现单元测试，测试程序位于stock_predict/test.py，在控制台根目录下使用命令`python manage.py test stock_predict'
来运行test.py。
#### 集成测试
如果想完成集成测试，则需要借助第三方库：coverage.py，可以通过`pip install coverage`安装，详情使用参考[coverage.py](https://pypi.org/project/coverage/)。
1. 控制台在根目录WebStockPredict下，输入命令`coverage run --source='.' manage.py test stock_predict`来执行test.py
2. 下一步输入`coverage report`命令，可以生成简易的测试报告
3. 为了获得更详细的测试报告，可输入`coverage html`命令，其会在根目录下生成htmlcov文件夹，里面包含自动生成的html页面，点击index.html可查看整个项目以及各个文件的测试覆盖率，如下图：
![coverage_index](/display_img/coverage_index.png "集成测试")


### 本机硬软件环境
+ win10-64bit
+ NVIDIA GeForce GTX1060
+ NVIDIA显卡驱动版本：391.24

### 参考
[LSTM-Neural-Network-for-Time-Series-Prediction](https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction)

[数据接口-免费版（股票数据API）](https://blog.csdn.net/llingmiao/article/details/79941066)
