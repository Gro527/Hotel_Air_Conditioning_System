from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.dao.mapper import *

class iRecordDAO(object):
    def GetRecord(self,invoice_id):
        ret = session.query(iRecord).filter_by(invoice_id=invoice_id).all()
        # ???可以直接返回ret吗
        return ret


