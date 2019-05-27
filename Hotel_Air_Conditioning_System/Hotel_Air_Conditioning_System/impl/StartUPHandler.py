## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl import gDict
import json

class StartUPHandler(object):
    def SetPara(self, mode, temp_highLimit, temp_lowLimit, default_targetTemp, feeRate_H, feeRate_M,feeRate_L):
        settings = {
            'mode' : mode,
            'temp_highLimit' : temp_highLimit,
            'temp_lowLimit' : temp_lowLimit,
            'default_targetTemp' : default_targetTemp,
            'feeRate_H' : feeRate_H,
            'feeRate_M' : feeRate_M,
            'feeRate_L' : feeRate_L
        }
        sf = open("settings.json",mode='w')
        sf.write(json.dumps(settings))
        gDict["settings"] = settings
    def StartUp(self):
        gDict["serv_pool"].setState("ready")