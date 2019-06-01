from Hotel_Air_Conditioning_System.dao.mapper import iInvoice
from Hotel_Air_Conditioning_System.impl import *
from flask import current_app    
import json
class Invoice(object):
    def __init__(self, invoice_id, room_id, date_in, date_out, total):
        self.invoice_id = invoice_id
        self.room_id = room_id
        self.date_in = date_in
        self.date_out = date_out
        self.total = total
    def out_file(self):
        base_fname = "inv_"+str(self.room_id)+"_"+str(self.date_in)+"-"+str(self.date_out)
        f = open(current_app.root_path+"\\inv\\"+base_fname+"_json.json","w")
        content = {}
        content["invoice_id"] = self.invoice_id
        content["room_id"] = self.room_id
        content["date_in"] = str(self.date_in)
        content["date_out"] = str(self.date_out)
        content["total"] = self.total
        f.write(json.dumps(content))