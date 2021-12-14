import csv
import mysql.connector
import tkinter.messagebox
from tkinter import *
from config_file import config

def getDiseaseFromSymptoms(sym1, sym2, sym3):
    predicted_diseases = ["", "", ""]
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    if sym2 == "":
        sym2 = 'NULL'
    if sym3 == "":
        sym3 = 'NULL'
    query = "SELECT disease FROM diseasetb\
    WHERE %s IN (symptom1, symptom2, symptom3) \
    AND %s IN (symptom1, symptom2, symptom3, 'NULL') \
    AND %s IN (symptom1, symptom2, symptom3, 'NULL')"

    args = (sym1, sym2, sym3)
    cur.execute(query, args)
    myDiseases = cur.fetchall()
    for index in range(0, min(3, len(myDiseases))):
        predicted_diseases[index] = myDiseases[index][0]
    cur.close()
    db.close()
    return predicted_diseases

def manageUser(window, username, password):
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "SELECT password FROM user_history WHERE username = %s"
    args = (username,)
    cur.execute(query, args)
    data = cur.fetchall()

    if len(data) != 0: # username exists in table
        if data[0][0] == password: # password matches username
            return 0
        else:
            return 1 # return nonzero code
    else: # username does not exist
        addUser(username, password)
        return 0

    db.commit()
    cur.close()
    db.close()

def addUser(username, password):
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = 'INSERT INTO user_history(username, password)' \
        'VALUES(%s, %s)'
    args = (username, password)
    cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

def addUserDetails(username, name, age, gender, blood_group):
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "UPDATE user_history \
        SET name = %s, age = %s, gender = %s, blood_group = %s \
        WHERE username = %s"
    args = (name, age, gender, blood_group, username)
    cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

def getAllSymptoms():
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "SELECT symptom FROM symptomtb"
    cur.execute(query)
    mySymptoms = cur.fetchall()
    all_symptoms = []
    for s in mySymptoms:
        all_symptoms.append(s[0])
    cur.close()
    db.close()
    return all_symptoms

def getAllDiseases():
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "SELECT disease FROM diseasetb"
    cur.execute(query)
    myDiseases = cur.fetchall()
    all_diseases = []
    for d in myDiseases:
        all_diseases.append(d[0])
    cur.close()
    db.close()
    return all_diseases

def addDiseasesToUserTable(username, predicted_diseases):
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()

    query = "UPDATE user_history \
        SET pre_disease1 = %s, \
        pre_disease2 = %s, \
        pre_disease3 = %s \
        WHERE username = %s"
    args = (predicted_diseases[0], predicted_diseases[1], predicted_diseases[2], username)
    cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

def getUserHistory(username):

    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor(dictionary=True)
    query = "SELECT * FROM user_history WHERE username = %s"
    args = (username,)
    cur.execute(query, args)
    data = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return data[0]

def addModifyDisease(window, disease, symptom1, symptom2, symptom3):
    dis = disease.get()
    sym1 = symptom1.get()
    sym2 = symptom2.get()
    sym3 = symptom3.get()

    if dis == "":
        showErrorText(window, "error: enter disease.", 25, 280, 220)
        return
    if sym1 == "":
        showErrorText(window, "error: enter symptom.",25, 280, 220)
        return

    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "SELECT * FROM diseasetb WHERE disease = %s"
    args = (dis,)
    cur.execute(query, args)
    data = cur.fetchall()
    if len(data) == 0:
        query = 'INSERT INTO diseasetb(disease, symptom1, symptom2, symptom3)' \
            'VALUES(%s, %s, %s, %s)'
        args = (dis, sym1, sym2, sym3)
        cur.execute(query, args)
    else:
        query = "UPDATE diseasetb \
            SET symptom1 = %s, \
            symptom2 = %s, \
            symptom3 = %s \
            WHERE disease = %s"
        args = (sym1, sym2, sym3, dis)
        cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

    disease.delete(0, 'end')
    symptom1.set('')
    symptom2.set('')
    symptom3.set('')
    text_1 = Text(window, height = 1, width = 20)
    text_1.insert(END, "Changes applied!")
    text_1.place(x=280,y=220)


def deleteDisease(window, disease):
    dis = disease.get()
    if dis == "":
        showErrorText(window, "error: enter disease.", 25, 280, 450)
        return
    
    db = mysql.connector.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'])
    cur = db.cursor()
    query = "SELECT * FROM diseasetb WHERE disease = %s"
    args = (dis,)
    cur.execute(query, args)
    data = cur.fetchall()
    if len(data) == 0:
        showErrorText(window, "error: enter existing disease.", 30, 280, 450)
        return
    
    query = "DELETE FROM diseasetb WHERE disease = %s"
    args = (dis,)
    cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

    disease.set('')
    text_1 = Text(window, height = 1, width = 20)
    text_1.insert(END, "Changes applied!")
    text_1.place(x=280,y=450)

def showErrorText(window, text, width, x, y):
    text_1 = Text(window, height = 1, width = width)
    text_1.insert(END, text)
    text_1.place(x=x,y=y)