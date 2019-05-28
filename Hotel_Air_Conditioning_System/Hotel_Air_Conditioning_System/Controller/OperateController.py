## 对应角色：顾客
from Hotel_Air_Conditioning_System.impl import gDict
class OperateController(object):
    def RequestOn(self, room_id):
        gDict["schedule"].OnRequest(room_id, "on")
    def Set(self, service_number):
        pass
    def ChangeTargetTemp(self, room_id, target_temp):
        pass
    def ChangeFanSpeed(self, room_id, fan_speed):
        pass
    def RequestOff(self, room_id):
        pass
    def RequestFee(self, room_id):
        pass

