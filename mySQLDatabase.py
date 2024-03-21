import mysql.connector
from secrets import *
# Establishing connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=password,
    database="userPerson"
)

# Check if connection is successful
if conn.is_connected():
    print("MySQL connection established.")
else:
    print("MySQL connection failed.")

# # Closing the connection (not necessary here, since we want it to be open for the app's lifetime)
# # conn.close()
#
# # Creating cursor object
# objectCursor = conn.cursor()
#
# # Creating the 'userdata' table if it doesn't exist
# userRecords = """
# CREATE TABLE IF NOT EXISTS userdata (
#     UserID INT NOT NULL AUTO_INCREMENT,
#     Name VARCHAR(50) NOT NULL,
#     Username VARCHAR(50) NOT NULL,
#     Password VARCHAR(255) NOT NULL,
#     Salt VARCHAR(255) NOT NULL,
#     PRIMARY KEY (UserID)
# )
# """
# objectCursor.execute(userRecords)
#
# # Commit changes and close cursor and connection
# conn.commit()
# objectCursor.close()
# conn.close()