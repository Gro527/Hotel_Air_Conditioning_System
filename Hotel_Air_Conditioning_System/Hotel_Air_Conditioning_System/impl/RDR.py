import json
from flask import current_app
import datetime
class RDR(object):
    def __init__(self, invoice_id, room_id, date_in, date_out, total, rList):
        self.invoice_id = invoice_id
        self.room_id = room_id
        self.date_in = date_in
        self.date_out = date_out
        self.total = total
        self.rList = rList
    def out_file(self):
        base_fname = "rdr_"+str(self.room_id)+"_"+datetime.datetime.strftime(self.date_in,"%Y-%m-%d-%H%M%S")+"-"+datetime.datetime.strftime(self.date_out,"%Y-%m-%d-%H%M%S")
        f = open(current_app.root_path+"\\rdr\\"+base_fname+"_json.txt","w")
        content = {}
        content["invoice_id"] = self.invoice_id
        content["room_id"] = self.room_id
        content["date_in"] = str(self.date_in)
        content["date_out"] = str(self.date_out)
        content["total"] = self.total
        content["rList"] = self.rList
        f.write(json.dumps(content))

