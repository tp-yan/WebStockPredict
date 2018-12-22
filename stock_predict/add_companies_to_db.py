from stock_predict import models

def add_company():
    companies = {"600718":"东软集团","000651":"格力电器","600839":"四川长虹","600320":"振华重工","601988":"中国银行",
                 "000066": "中国长城","601766":"中国中车","601390":"中国中铁","000768":"中航飞机","000063":"中兴通讯"}

    for code,name in companies.items():
        company = models.Company()
        company.stock_code = code
        company.name = name
        company.save()

