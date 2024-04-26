def create_table_student(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS Student(id_student INT AUTO_INCREMENT PRIMARY KEY, \
                     first_name VARCHAR(255),second_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255))")
    print("Table created")
# Таблица учителя
def create_table_teacher(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS Teacher(id_teacher INT AUTO_INCREMENT PRIMARY KEY, \
                     first_name VARCHAR(255),second_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255))")
    print("Table created")
# Таблица результаты
def create_results(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS results(id_result INT AUTO_INCREMENT PRIMARY KEY, \
                     content_recommend VARCHAR(255),teacher_recommend VARCHAR(255),organization_recommend VARCHAR(255), \
                     positive_moment VARCHAR(255),negative_moment VARCHAR(255))")
# Таблица вебинары
def create_table_vebinar(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS vebinar(id_vebinar INT AUTO_INCREMENT PRIMARY KEY, \
                     name_vebinar VARCHAR(255),date_vebinar DATETIME, id_result INT, \
                     FOREIGN KEY (id_result) REFERENCES results(id_result))")
def create_student_vebinar(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS student_vebinar(id_student_vebinar INT AUTO_INCREMENT PRIMARY KEY,\
                      id_student INT, id_vebinar INT, FOREIGN KEY (id_student) REFERENCES Student(id_student), \
                     FOREIGN KEY (id_vebinar) REFERENCES vebinar(id_vebinar))")
    print("Table created")
def create_teacher_vebinar(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS teacher_vebinar(id_teacher_vebinar INT \
                      AUTO_INCREMENT PRIMARY KEY, id_teacher INT, id_vebinar INT, \
                     FOREIGN KEY (id_teacher) REFERENCES Teacher(id_teacher), FOREIGN KEY (id_vebinar) REFERENCES vebinar(id_vebinar))")
    print("Table created")
def create_teacher_vebinar(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS teacher_vebinar(id_teacher_vebinar INT \
                     AUTO_INCREMENT PRIMARY KEY, id_teacher INT, id_vebinar INT, \
                     FOREIGN KEY (id_teacher) REFERENCES Teacher(id_teacher), FOREIGN KEY (id_vebinar) REFERENCES vebinar(id_vebinar))")
    print("Table created")
def create_Survey(mycursor):
    mycursor.execute("CREATE TABLE IF NOT EXISTS Survey(id_survey INT AUTO_INCREMENT PRIMARY KEY, \
                      id_student INT, id_vebinar INT, is_ready INT,Timestamp DATETIME,\
                      Question1 VARCHAR(255),Question2 VARCHAR(255), \
                      Question3 VARCHAR(255),Question4 VARCHAR(255),\
                      Question5 VARCHAR(255),Hash INT,Is_relevant BOOL,\
                      Object INT, Is_Positive BOOL,\
                     FOREIGN KEY (id_vebinar) REFERENCES vebinar(id_vebinar),\
                      FOREIGN KEY (id_student) REFERENCES Student(id_student))")
    print("Table created")
