from Hotel_Air_Conditioning_System.dao import *

uname = "root"
pw = "Yuker2019!"
address = "47.94.210.236"
port = 3306
db = "hacs_db"

engine = create_engine("mysql+pymysql://" + uname + ":" + pw + "@" + address + ":" + str(port) + "/" + db, max_overflow = 5)

base = declarative_base()

