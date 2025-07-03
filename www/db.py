import sqlite3

conn = sqlite3.connect('chitti.db')

cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

# to insert values
#query = "INSERT INTO sys_command VALUES (null,'word', 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk')"
#cursor.execute(query)
#conn.commit()
#conn.close()  # Don't forget to close the connection when done

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

query = "UPDATE sys_command SET name = 'microsoft edge' WHERE path = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk'"
cursor.execute(query)
conn.commit()
conn.close()