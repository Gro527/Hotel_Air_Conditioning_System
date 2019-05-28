from Hotel_Air_Conditioning_System.impl import gDict
from datetime import datetime
class Service(object):
    def __init__(self, service_id):
        self.service_id = service_id
        self.is_working = False
        self.room_id = 0
        self.speed = 0
        self.trg_tmp = 0
        print("服务对象",service_id,"已创建")

    # 设置目标温度
    def SetTemp(self, temp):
        self.trg_tmp = temp
    def ShowBill(self):
        pass
    def ShowDetailBill(self):
        pass
    def ShowReport(self):
        pass
    def SetState(self, state):
        self.state = state

    # 绑定房间
    def BindRoom(self, room_id, speed):
        self.room_id = room_id
        gDict["rooms"].new_room(room_id)
        self.is_working = True
        self.trg_tmp = gDict["settings"].get("default_targetTemp", 24)
        self.speed = speed
        #### 数据库记录
        

    # 更改风速(需在数据库中记录)
    def SpdChange(self, speed):
        self.speed = speed
        #### 数据库记录
    
    # 释放服务
    def ReleaseRoom(self):
        self.room_id = 0
        self.is_working = False
        self.speed = 0
        self.trg_tmp = 0
    
    # 获取当前温度
    def GetCurTmp(self):
        room = gDict["rooms"].get_room(self.room_id)
        if room == None:
            return None
        # 计算温度，每工作1秒改变温度0.01度
        if self.is_working == True:
            if gDict["settings"].get("mode") == "cold":
                return room.tmp_dec((datetime.now() - room.last_op_time).second * 0.01)
            else:
                return room.tmp_up((datetime.now() - room.last_op_time).second * 0.01)
        else:
            return room.ref_tmp()
    
    # 获取目标温度
    def GetTrgTmp(self):
        pass

