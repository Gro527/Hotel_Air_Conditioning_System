"""
Routes and views for the flask application.
"""

import os

from datetime import datetime
from flask import request,send_from_directory
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.controller import *

## 资源文件下载
@app.route('/resource/<path:filename>')
def resource(filename):
    dirpath = os.path.join(app.root_path, "frontend/static") #定位至后台程序所在目录的static文件下
    return send_from_directory(dirpath, filename, as_attachment=True)




## 页面路由
# 主页
@app.route('/')
@app.route('/home')
def home_page():
    return "this is the home page"
# 顾客
@app.route('/client')
def client_page():
    return "this is the client page"
# 前台
@app.route('/reception')
def reception_page():
    return "this is the reception page"
# 管理员
@app.route('/supervisor')
def supervisor_page():
    f = open(app.root_path+"\\frontend\\supervisor\\supervisor.html", encoding='utf-8')
    return f.read()
# 经理
@app.route('/manager')
def manager_page():
    return "this is the manager page"


## 接口路由

# 获取订单信息
@app.route('/reception/api/invoice/<invoice_id>')
def invoice(id):
    from Hotel_Air_Conditioning_System.controller.CreateInvoiceController import cic
    cic.CreateInvoice()

