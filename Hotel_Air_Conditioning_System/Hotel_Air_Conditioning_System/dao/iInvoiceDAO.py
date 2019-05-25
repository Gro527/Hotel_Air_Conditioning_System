from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.dao.mapper import iInvoice,Session

class iInvoiceDAO(object):
    sess = Session()
    def GetTotal():
        ret = sess.query(iInvoice).filter_by(room_id = self.room_id, date_in = self.date_in, date_out = self.date_out).all
        return ret[0]

