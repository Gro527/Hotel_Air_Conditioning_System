from Hotel_Air_Conditioning_System.dao import *

uname = "root"
pw = "root"
address = "localhost"
port = 3306
db = "hacs_db1"

engine = create_engine("mysql+pymysql://" + uname + ":" + pw + "@" + address + ":" + str(port) + "/" + db, max_overflow = 5)

base = declarative_base()
