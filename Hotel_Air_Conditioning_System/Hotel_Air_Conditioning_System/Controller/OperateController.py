## 对应角色：顾客
from Hotel_Air_Conditioning_System.impl import gDict,Service
from Hotel_Air_Conditioning_System.dao import iInvoiceDAO
import json
class OperateController(object):
    def RequestOn(self, room_id):
        return json.dumps(gDict["schedule"].OnRequest(room_id, {"req_type":"on"}))
    def Set(self, service_number):
        pass
    def ChangeTargetTemp(self, room_id, target_temp):
        return json.dumps(gDict["schedule"].OnRequest(room_id, {"req_type":"tmp", "trg":target_temp}))
    def ChangeFanSpeed(self, room_id, fan_speed):
        return json.dumps(gDict["schedule"].OnRequest(room_id, {"req_type":"spd", "trg":fan_speed}))
    def RequestOff(self, room_id):
        return json.dumps(gDict["schedule"].OnRequest(room_id, {"req_type":"off"}))
    def RequestFee(self, room_id):
        pass
    def Refresh(self, room_id):
        room = gDict["rooms"].get_room(room_id)
        if room == None:
            return json.dumps({"state":"error"})
        res = {}
        res["state"] = room.state
        if res["state"] == "R":
            service = gDict["serv_pool"].GetService(room_id)
            print("refresh: service_id = " , service.service_id)
            res["curTmp"] = service.GetCurTmp()
            ## 计算费用
            fee_serv = Service.Service(6666)
            res["total"] = fee_serv.ShowBill(iInvoiceDAO.iInvoiceDAO().GetLastInvoiceId(room_id))
            # 刷新温度后，需重新刷新房间状态
            res["state"] = room.state
            if res["state"] != "R":
                return json.dumps(res)
            res["spd"] = service.GetCurSpd()
            res["trgTmp"] = service.GetTrgTmp()
            ## 由服务对象计算温度
        else:
            res["curTmp"] = room.ref_tmp()
        ## 计算费用
        fee_serv = Service.Service(6666)
        res["total"] = fee_serv.ShowBill(iInvoiceDAO.iInvoiceDAO().GetLastInvoiceId(room_id))
            ## 模拟房间回温
        return json.dumps(res)