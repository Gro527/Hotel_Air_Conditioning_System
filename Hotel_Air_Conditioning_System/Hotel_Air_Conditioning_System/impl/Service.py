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
        gDict["rooms"].get_room(self.room_id).set_trgTmp(temp)
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
        self.is_working = True
        room = gDict["rooms"].get_room(room_id)
        if room == None:
            self.trg_tmp = gDict["settings"].get("default_targetTemp", 24)
            gDict["rooms"].new_room(room_id, self.trg_tmp)
        else:
            self.trg_tmp = room.trg_tmp
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
            sche = gDict["schedule"]
            if gDict["settings"].get("mode") == "cold":
                curtmp =  room.tmp_dec((datetime.now() - room.last_op_time).seconds * 0.01)
                # 当温度低于目标温度时，暂停服务进入等待序列
                if curtmp < self.trg_tmp:
                    waiting = sche.GetLongestWait()
                    sche.ReleaseService(self.service_id)
                    # 若等待队列不为空，则等待队列中等待时间最长的目标开始服务
                    if waiting != None:
                        sche.NewService(waiting.room_id, waiting.speed)
                return curtmp
            else:
                curtmp =  room.tmp_up((datetime.now() - room.last_op_time).seconds * 0.01)
                # 当温度高于目标温度时，暂停服务进入等待序列
                if curtmp > self.trg_tmp:
                    waiting = sche.GetLongestWait()
                    sche.ReleaseService(self.service_id)
                    if waiting != None:
                        sche.NewService(waiting.room_id, waiting.speed)
                return curtmp
        else:
            return room.ref_tmp()
    
    # 获取目标温度
    def GetTrgTmp(self):
        return self.trg_tmp

    # 获取当前风速
    def GetCurSpd(self):
        return self.speed
