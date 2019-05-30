## 对应角色：前台
from Hotel_Air_Conditioning_System.impl import Service
import json

class CreateRDRController(object):
    def CreateRDR(self, room_id, date_out):
        #...???
        s=Service.Service()
        rdrList,total,date_in = s.ShowDetailBill(room_id)
        return json.dump({'dateIn':date_in,'dateOut':date_out,'rdrList':rdrList})

