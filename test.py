import sqlite3
from datetime import datetime
timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
db_file_name = f"example_{timestr}.db"
conn = sqlite3.connect(db_file_name)
c = conn.cursor()
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
file_name = "demo"+timestr+".db"
print(file_name)
f=open(file_name,"w")
c.execute("INSERT INTO EMP(current, EMP_Name, City, Timestamp) VALUES(?, ?, ?, ?)", (3, 'Bob', 'Sweden', formatted_date))
conn.commit()
conn.close()