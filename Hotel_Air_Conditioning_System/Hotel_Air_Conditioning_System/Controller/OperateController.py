## 对应角色：顾客
from Hotel_Air_Conditioning_System.impl import gDict
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

