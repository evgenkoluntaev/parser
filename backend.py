import sqlite3
conn = sqlite3.connect("vac.db")
cursor = conn.cursor()


def create_db(name, city):
    cursor.execute("CREATE TABLE " + name + "_" + city + "(date text, speciality text, company text, salary text, skills text, location text, href text)")


def active_insert(name, city,  date, speciality, company, salary, skills, location, href):
    cursor.execute("INSERT INTO " + name + "_" + city + " VALUES(?, ?,?, ?,?,?,?)", (date, speciality, company, salary, skills, location, href))
    conn.commit()
   

def selector(name, city):
    cursor.execute("SELECT * FROM " + name + "_" + city)
    for i in cursor.fetchall():
        print(i)


def delete(name):

    sql = "DELETE FROM" + name
    cursor.execute(sql)
    conn.commit()


def sort():
    for row in cursor.execute("SELECT rowid, * FROM albums ORDER BY date"):
        print(row)


def update_db(*some_parameters):
    cursor.execute("blah blah blah")


def reopen_connect():  
    conn = sqlite3.connect("vac.db")  
    cursor = conn.cursor()
