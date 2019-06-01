## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl import gDict,ServicePool,Schedule,StartUPHandler
import json
from Hotel_Air_Conditioning_System.impl.room import RoomList

class StartUPController(object):


    ##发送系统事件
    def CreateServPool(self):
        gDict["serv_pool"] = ServicePool.ServicePool(max_service=3)
    def CreateSchedule(self):
        gDict["schedule"] = Schedule.Schedule()

    ##接受系统事件
    def PowerOn(self):
        if gDict["server_state"] != "off":
            return {"state":"Invalid Request"}
        # 初始化功能模块
        self.CreateServPool()
        self.CreateSchedule()
        #########不需要
        # 初始化设置
        gDict["settings"] = json.loads(
            open('settings.json').read()
        )
        # 初始化房间信息
        gDict["rooms"] = RoomList()
        gDict["server_state"] = "on"
        res = {"state":"set_Mode"}
        return json.dumps(res)

    def SetPara(self, mode, temp_highLimit, temp_lowLimit, default_targetTemp, feeRate_H, feeRate_M,feeRate_L):
        if gDict["server_state"] != "on":
            return {"state":"Invalid Request"}
        suh = StartUPHandler.StartUPHandler()
        suh.SetPara(mode, temp_highLimit, temp_lowLimit, default_targetTemp, feeRate_H, feeRate_M,feeRate_L)
        gDict["server_state"] = "para"
        return json.dumps({"state":"OK"})

    def StartUp(self):
        if gDict["server_state"] != "para":
            return {"state":"Invalid Request"}
        suh = StartUPHandler.StartUPHandler()
        suh.StartUp()
        gDict["server_state"] = "start"
        return json.dumps({"state":"ready"})

    




