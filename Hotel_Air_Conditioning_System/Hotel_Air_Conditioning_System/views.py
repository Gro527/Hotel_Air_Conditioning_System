"""
Routes and views for the flask application.
"""

import os

from datetime import datetime
from flask import request,send_from_directory, redirect, request
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.controller import *
from Hotel_Air_Conditioning_System import dao








## 资源文件下载
@app.route('/frontend/resource/<path:filename>')
def resource(filename):
    dirpath = os.path.join(app.root_path, "frontend/static") #定位至后台程序所在目录的static文件下
    return send_from_directory(dirpath, filename, as_attachment=True)




## 页面路由
# 主页
@app.route('/')
def root():
    return redirect('./frontend/home.html')

@app.route('/frontend/home.html')
def home_page():
    f = open(app.root_path+"\\frontend\\home.html", encoding='utf-8')
    return f.read()
# 顾客
@app.route('/frontend/client/client.html')
def client_page():
    f = open(app.root_path+"\\frontend\\client\\client.html", encoding='utf-8')
    return f.read()

# 前台
@app.route('/frontend/reception/reception.html')
def reception_page():
    f = open(app.root_path+"\\frontend\\reception\\reception.html", encoding='utf-8')
    return f.read()
# 管理员
@app.route('/frontend/supervisor/supervisor.html')
def supervisor_page():
    f = open(app.root_path+"\\frontend\\supervisor\\supervisor.html", encoding='utf-8')
    return f.read()
# 经理
@app.route('/frontend/manager/manager.html')
def manager_page():
    f = open(app.root_path+"\\frontend\\manager\\manager.html", encoding='utf-8')
    return f.read()


## 接口路由

## 管理员
@app.route('/api/supervisor/on')
def powerOn():
    suc = StartUPController.StartUPController()
    return suc.PowerOn()
@app.route('/api/supervisor/para', methods=['POST'])
def setPara():
    settings = request.get_json()
    mode = settings["mode"]
    temp_highLimit = settings["tmpH"]
    temp_lowLimit = settings["tmpL"]
    default_targetTemp = settings["tmpD"]
    feeRate_H = settings["rateH"]
    feeRate_M = settings["rateM"]
    feeRate_L = settings["rateL"]
    suc = StartUPController.StartUPController()
    return suc.SetPara(mode, temp_highLimit, temp_lowLimit, default_targetTemp, feeRate_H,feeRate_M,feeRate_L)
@app.route('/api/supervisor/start')
def StartUp():
    suc = StartUPController.StartUPController()
    return suc.StartUp()
@app.route('/api/supervisor/check', methods=['POST'])
def CheckRoomState():
    list_roomid = request.get_json()
    csc = CheckStateController.CheckStateController()
    return csc.CheckRoomState(list_roomid)

## 顾客
@app.route('/api/client/on', methods=['POST'])
def RequestOn():
    params = request.get_json()
    room_id = params["id"]
    cur_tmp = params["curTmp"]
    oc = OperateController.OperateController()
    return oc.RequestOn(room_id, cur_tmp)


# 获取订单信息
@app.route('/api/reception/invoice/<id>')
def invoice(id):
    from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
    idao = iInvoiceDAO()
    return str(idao.GetTotal(203, "2019-05-24", "2019-05-25"))
