import sqlite3
import csv
from datetime import datetime
timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
db_file_name = f"example_{timestr}.db"
conn = sqlite3.connect(db_file_name)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS EMP_1(ID, EMP_Name, City, Timestamp)")
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
c.execute("INSERT INTO EMP_1(ID, EMP_Name, City, Timestamp) VALUES(?, ?, ?, ?)", (1, 'John', 'NewYork', formatted_date))
c.execute("INSERT INTO EMP_1(ID, EMP_Name, City, Timestamp) VALUES(?, ?, ?, ?)", (2, 'Martin', 'Paris', formatted_date))
c.execute("INSERT INTO EMP_1(ID, EMP_Name, City, Timestamp) VALUES(?, ?, ?, ?)", (3, 'Bob', 'Sweden', formatted_date))

conn.commit()
csv_file_name = f"example_{timestr}.csv"
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    c.execute("SELECT * FROM EMP_1")
    csv_writer.writerow([i[0] for i in c.description])
    csv_writer.writerows(c.fetchall())

conn.close()
