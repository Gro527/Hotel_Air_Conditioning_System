from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.dao.mapper import *
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
from Hotel_Air_Conditioning_System.impl import gDict
import datetime
import enum
class iRecordDAO(object):
    def GetRecord(self,invoice_id):
        ret = session.query(iRecord).filter_by(invoice_id=invoice_id).all()
        # ???可以直接返回ret吗
        return ret
    # 插入记录
    def AddRecord(self, room_id, speed, action_type):
        room = gDict["rooms"].get_room(room_id)
        # 获取房间信息和计价情况
        trg_tmp = room.trg_tmp
        fee_rate = 0
        # 只有在房间空调运转情况下才计费
        if room.state == "R":
            if speed == "L":
                fee_rate = gDict["settings"].get("feeRate_L",1.2)
            elif speed == "M":
                fee_rate = gDict["settings"].get("feeRate_M",1.4)
            elif speed == "H":
                fee_rate = gDict["settings"].get("feeRate_H",1.6)
        invoice_id = iInvoiceDAO().GetLastInvoiceId(room_id)
        session.add(iRecord(invoice_id = invoice_id, start_time = datetime.datetime.now(), trg_tmp = trg_tmp, speed = speed, action_type = action_type, fee_rate = fee_rate))
        session.commit()

