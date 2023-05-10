# import sqlite3
# import time  
# from datetime import datetime
# now = datetime.now()
# conn = sqlite3.connect("demo.db")
# # a = time.time()
# formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
# # print(a,type(a))
# print(formatted_date)
# c = conn.cursor()
# #c.execute("Create table EMP(ID, EMP_Name, City,Timestamp)")
# c.execute("INSERT INTO EMP(ID, EMP_Name, City, Timestamp) VALUES(3,'Bob','Sweden',now)")
# conn.commit()
# #c.execute('INSERT INTO myTable (Date) VALUES(%s)',(a))
# import sqlite3
# from datetime import datetime

# # create a connection to the database
# conn = sqlite3.connect("demo.db")

# # create a cursor object to execute SQL commands
# c = conn.cursor()

# # get the current date and time
# now = datetime.now()

# # format the date and time as a string
# formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

# # update the row with ID=3 and set the EMP_Name to 'Alice' and City to 'USA', and update the Timestamp column with the current timestamp
# c.execute("UPDATE EMP SET EMP_Name=?, City=?, Timestamp=? WHERE ID=?", ('Alice', 'USA', formatted_date, 3))

# # commit the changes to the database
# conn.commit()

# # select the row with ID=3 and print the values
# c.execute("SELECT * FROM EMP WHERE ID=?", (3,))
# row = c.fetchone()
# print(row)

# # close the connection to the database
# conn.close()
# def store_data_and_create_csv(current, pse_cor, pd_cor, ch4_adc):
#     # Create database connection
#     timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
#     db_file_name = f"example_{timestr}.db"
#     conn = sqlite3.connect(db_file_name)
#     c = conn.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS Power(ID INTEGER PRIMARY KEY, current TEXT, pse_cor TEXT, pd_cor TEXT, ch4_adc TEXT, Timestamp TEXT)")

#     # Insert data into database
#     now = datetime.now()
#     formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
#     for i in range(len(current)):
#         values = (i+1, str(current[i]), str(pse_cor[i]), str(pd_cor[i]), str(ch4_adc[i]), formatted_date)
#         conn.execute("INSERT INTO Power (ID, current, pse_cor, pd_cor, ch4_adc, Timestamp) VALUES (?, ?, ?, ?, ?, ?)", values)
#     conn.commit()

#     # Create CSV file from database data
#     csv_file_name = f"example_{timestr}.csv"
#     with open(csv_file_name, 'w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         c.execute("SELECT * FROM Power")
#         csv_writer.writerow([i[0] for i in c.description])
#         csv_writer.writerows(c.fetchall())

#     # Close database connection
#     conn.close()
