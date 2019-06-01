from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.dao.mapper import *
import datetime
class iInvoiceDAO(object):
    def GetTotal(self, room_id):
       ret = session.query(iInvoice).filter_by(room_id = room_id).all()
       return ret[0].total
    # def GetDateIn(self,room_id):
    #     ret=session.query(iInvoice).filter_by(room_id=room_id).all()
    #     ret=ret.reverse()
        # return ret[0].date_in
    def GetLastInvoiceId(self, room_id):
        last_invoice = session.query(iInvoice).filter_by(room_id = room_id).order_by(iInvoice.date_in.desc()).first()
        if last_invoice == None:
            return None
        return last_invoice.id
    def AddInvoice(self, room_id):
        date_in = datetime.date.today()
        exist_invoice = session.query(iInvoice).filter_by(room_id = room_id, date_in=date_in).all()
        if len(exist_invoice) != 0:
            return exist_invoice[0].id
        session.add(iInvoice(room_id=room_id, date_in=date_in,total=0))
        session.commit()
    def SetTotal(self, invoice_id, total):
        session.query(iInvoice).filter_by(id = invoice_id).update({"total":total})
        session.commit()
    def GetInvoiceById(self, invoice_id):
        return session.query(iInvoice).filter_by(id = invoice_id).all()[0]
    def SetDateOut(self, invoice_id, date_out):
        session.query(iInvoice).filter_by(id = invoice_id).update({"date_out":date_out})
        session.commit()
    def GetInvoiceByDate(self, start_date, end_date):
        ret = session.query(iInvoice).filter(iInvoice.date_in >= start_date, iInvoice.date_out <= end_date).all()
        return ret