"""
Routes and views for the flask application.
"""

import os

from datetime import datetime
from flask import request,send_from_directory, redirect, request
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.controller import *
from Hotel_Air_Conditioning_System import dao
import json



##兼容QT转发模块
@app.route('/', methods=['GET','POST'])
def re_route():
    if request.method == 'GET':
        return redirect('./frontend/home.html')
    else:
        params = request.get_json()
        print(params)
        if params.get("actorType", 0) == 0:
            return "actorType not found", 400
        if params.get("requestType", 0) == 0:
            return "requestType not found", 400
        actor = params["actorType"]
        req_type = params["requestType"]
        return redirect('./api/'+actor+'/'+req_type, code=307)



## 资源文件下载
@app.route('/frontend/resource/<path:filename>')
def resource(filename):
    dirpath = os.path.join(app.root_path, "frontend/static") #定位至后台程序所在目录的static文件下
    return send_from_directory(dirpath, filename, as_attachment=True)




## 页面路由

# 主页
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
# 开机
@app.route('/api/adm/on', methods=['POST'])
def powerOn():
    suc = StartUPController.StartUPController()
    return suc.PowerOn()

# 设置运行参数
@app.route('/api/adm/para', methods=['POST'])
def setPara():
    params = request.get_json()
    mode = params.get("mode", 0)
    temp_highLimit = params.get("tmpH", 0)
    temp_lowLimit = params.get("tmpL", 0)
    default_targetTemp = params.get("tmpD", 0)
    feeRate_H = params.get("rateH", 0)
    feeRate_M = params.get("rateM", 0)
    feeRate_L = params.get("rateL", 0)
    if mode == 0 | temp_highLimit ==0 | temp_lowLimit ==0 | default_targetTemp == 0 | feeRate_H == 0 | feeRate_L == 0 | feeRate_M ==0:
        return "wrong attr", 400
    suc = StartUPController.StartUPController()
    return suc.SetPara(mode, temp_highLimit, temp_lowLimit, default_targetTemp, feeRate_H,feeRate_M,feeRate_L)

# 启动
@app.route('/api/adm/start', methods=['POST'])
def StartUp():
    suc = StartUPController.StartUPController()
    return suc.StartUp()

# 查看房间状态
@app.route('/api/adm/check', methods=['POST'])
def CheckRoomState():
    params = request.get_json()
    list_roomid = params.get("idList", 0)
    if list_roomid == 0:
        return "wrong attr", 400
    csc = CheckStateController.CheckStateController()
    return csc.CheckRoomState(list_roomid)




## 顾客
# 显示数据刷新
@app.route('/api/cos/ref', methods=["POST"])
def refresh():
    params = request.get_json()
    if params.get("roomID", 0) == 0:
        return "roomID not found", 400
    roomID = params["roomID"]
    ## .....

# 开空调
@app.route('/api/cos/on', methods=['POST'])
def RequestOn():
    params = request.get_json()
    room_id = params.get("roomID",0)
    if room_id == 0:
        return "roomID not found", 400
    oc = OperateController.OperateController()
    return oc.RequestOn(room_id)

# 关空调
@app.route('/api/cos/off', methods=['POST'])
def RequestOff():
    params = request.get_json()
    room_id = params.get("roomID",0)
    if room_id == 0:
        return "roomID not found", 400
    ## 。。。。。

# 调目标温度
@app.route('/api/cos/tmp', methods=['POST'])
def ChangeTargetTemp():
    params = request.get_json()
    room_id = params.get("roomID",0)
    target_temp = params.get("trg",0)
    if room_id == 0 | target_temp == 0:
        return "roomID not found", 400
    ## .....

# 调风速
@app.route('/api/cos/spd', methods=['POST'])
def ChangeFanSpeed():
    params = request.get_json()
    room_id = params.get("roomID",0)
    target_spd = params.get("trg",0)
    if room_id == 0 | target_spd == 0:
        return "roomID not found", 400
    ## .....




## 前台
# 获取账单
@app.route('/api/inf/inv', methods=['POST'])
def create_invoice():
    params = request.get_json()
    if params.get("roomID", 0) == 0:
        return "roomID not found", 400
    roomID = params["roomID"]
    ## .....

# 获取详单
@app.route('/api/inf/rdr', methods=['POST'])
def create_rdr():
    params = request.get_json()
    if params.get("roomID", 0) == 0:
        return "roomID not found", 400
    roomID = params["roomID"]
    ## .....




## 经理
# 获取报表
@app.route('/api/mng/rep', methods=['POST'])
def QueryReport():
    params = request.get_json()
    idList = params.get("idList", 0)
    rep_type = params.get("type", 0)
    until = params.get("until", 0)
    if idList == 0 | rep_type == 0 | until == 0:
        return "wrong attr", 400
    ## ....






## 测试路由
@app.route('/api/inf/invoice/<id>')
def invoice(id):
    from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
    idao = iInvoiceDAO()
    return str(idao.GetTotal(203, "2019-05-24", "2019-05-25"))