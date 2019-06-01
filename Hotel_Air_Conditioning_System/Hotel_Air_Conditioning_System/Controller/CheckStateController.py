## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl.CheckStateHandler import CheckStateHandler
from Hotel_Air_Conditioning_System.impl import gDict
import json
class CheckStateController(object):
    def CheckRoomState(self):
        csh = CheckStateHandler()
        res = []
        rooms = gDict["rooms"]
        for room in rooms.list_room:
            state = csh.CheckRoomState(room.room_id)
            res.append(state)
        return json.dumps(res)

