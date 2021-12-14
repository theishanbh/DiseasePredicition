import csv
import mysql.connector
from config_file import config

mydb = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
cursor = mydb.cursor()
query = '''CREATE TABLE user_history (
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    age VARCHAR(100),
    gender VARCHAR(100),
    blood_group VARCHAR(100),
    pre_disease1 VARCHAR(100),
    pre_disease2 VARCHAR(100),
    pre_disease3 VARCHAR(100),
    PRIMARY KEY (username)
    )'''
cursor.execute(query)

query = '''CREATE TABLE diseasetb (
    disease VARCHAR(100) NOT NULL,
    symptom1 VARCHAR(100),
    symptom2 VARCHAR(100),
    symptom3 VARCHAR(100),
    PRIMARY KEY (disease)
    )'''
cursor.execute(query)

query = '''CREATE TABLE symptomtb (
    symptom VARCHAR(100) NOT NULL,
    weight INT,
    PRIMARY KEY (symptom)
    )'''
cursor.execute(query)

query = '''INSERT INTO user_history(username, password)
        VALUES('admin', '1234')'''
cursor.execute(query)

with open('clean_db.csv', 'r') as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',')
    csv_headings = next(csv_data)

    for row in csv_data:
        cursor.execute('INSERT INTO diseasetb (disease, \
              symptom1, symptom2, symptom3 )' \
              'VALUES(%s, %s, %s, %s)',
              row)

with open('Symptom-severity.csv', 'r') as csvfile:
    csv_data = csv.reader(csvfile)
    csv_headings = next(csv_data)

    for row in csv_data:
        cursor.execute('INSERT INTO symptomtb (symptom, weight)' \
              'VALUES(%s, %s)',
              row)

#close the connection to the database.
mydb.commit()
cursor.close()
print("Done")