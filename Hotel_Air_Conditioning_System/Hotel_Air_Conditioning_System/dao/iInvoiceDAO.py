from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.dao.mapper import *

class iInvoiceDAO(object):
    def GetTotal(self, room_id, date_in, date_out):
       ret = session.query(iInvoice).filter_by(room_id = room_id, date_in = date_in, date_out = date_out).all()
       return ret[0].total
   #...???
    def GetDateIn(self,room_id):
       ret=session.query(iInvoice).filter_by(room_id=room_id).all()
       ret=ret.reverse()
       return ret[0].date_in
    def GetLastInvoiceId(self, room_id):
        last_invoice = session.query(iInvoice).filter_by(room_id = room_id).order_by(iInvoice.date_in.desc()).first()
        return last_invoice.id