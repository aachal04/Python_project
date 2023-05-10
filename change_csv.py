#import pandas as pd
#df = pd.read_csv('example.db' )
#df.to_csv('example.csv',index=None)
#df.to_sql('demo',connection,if_exists='append', index = False)
import csv
import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("select * from EMPLOYEE;")
with open("example.csv", 'w',newline='') as csv_file: 
   csv_writer = csv.writer(csv_file)
   csv_writer.writerow([i[0] for i in cursor.description]) 
   csv_writer.writerows(cursor)
   conn.close()
