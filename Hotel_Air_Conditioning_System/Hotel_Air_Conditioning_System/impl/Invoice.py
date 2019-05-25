from Hotel_Air_Conditioning_System.dao.mapper import iInvoice
from Hotel_Air_Conditioning_System.impl import *    
class Invoice(object):
    def __init__(self, room_id, date_in, date_out):
        self.room_id = room_id
        self.date_in = date_in
        self.date_out = date_out