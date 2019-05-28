tmp_today = 28
from datetime import datetime
class room(object):
    def __init__(self, room_id):
        self.room_id = room_id
        self.cur_tmp = tmp_today
        self.last_op_time = datetime.now()
    def ref_tmp(self):
        ## 模拟回温, 每1秒回温0.005度
        if self.cur_tmp < tmp_today:
            self.cur_tmp += (datetime.now() - self.last_op_time).second * 0.005
            if self.cur_tmp > tmp_today:
                self.cur_tmp = tmp_today
        if self.cur_tmp > tmp_today:
            self.cur_tmp -= (datetime.now() - self.last_op_time).second * 0.005
            if self.cur_tmp < tmp_today:
                self.cur_tmp = tmp_today
        self.last_op_time = datetime.now()
        return self.cur_tmp
    # 温度下降，参数：差值
    def tmp_dec(self, dif):
        self.cur_tmp -= dif
        self.last_op_time = datetime.now()
        return self.cur_tmp
    # 温度上升，参数：差值
    def tmp_up(self, dif):
        self.cur_tmp += dif
        self.last_op_time =datetime.now()
        return self.cur_tmp

class RoomList(object):
    def __init__(self):
        self.list_room = []
    def new_room(self, room_id):
        curRoom = self.get_room(room_id)
        if curRoom != None:
            curRoom.ref_tmp()
            return curRoom
        nRoom = room(room_id)
        self.list_room.append(nRoom)
        return nRoom
    def get_room(self, room_id):
        for room in self.list_room:
            if room.room_id == room_id:
                return room
            return None