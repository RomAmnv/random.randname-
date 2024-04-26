import mysql.connector
from app.database import create_table_student, create_table_teacher, create_results, create_table_vebinar, create_student_vebinar, create_teacher_vebinar,create_Survey
list_tables = ['student','teacher','results','vebinar','student_vebinar','teacher_vebinar']
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = mydb.cursor()

# Check if the database exists
cursor.execute("SHOW DATABASES")
databases = [row[0] for row in cursor.fetchall()]

if "mydatabase" not in databases:
    # Create the database
    cursor.execute("CREATE DATABASE mydatabase")
    print("Database created")
else:
    print("Database already exists")
cursor.close()
mydb.close()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydatabase"
)
cursor = mydb.cursor()
# Таблица студенты

create_table_student(cursor)
create_table_teacher(cursor)
create_results(cursor)
create_table_vebinar(cursor)
create_student_vebinar(cursor)
create_teacher_vebinar(cursor)
create_Survey(cursor)
cursor.close()
mydb.close()
