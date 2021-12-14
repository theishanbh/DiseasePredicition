from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
from sql_backend import *
import difflib


def showDisease(window, predicted_diseases):
    label_1 = Label(window, font=("Calibri", 13), text="Predicted diseases based on the above symptoms:")
    label_1.place(x=200,y=350)
    text_1 = Text(window, height = 3, width = 40)
    diseases_str = ""
    for d in predicted_diseases:
        diseases_str = diseases_str + d + "\n"
    text_1.insert(END, diseases_str)
    text_1.place(x=200,y=380)

    text_2 = Text(window, height = 1, width = 42)
    text_2.insert(END, "Disease predicted based on given symptoms.")
    text_2.place(x=240,y=530)


def submitCallback(window, username, name, age, gender, blood_group, sym1, sym2, sym3):
    all_symptoms = getAllSymptoms()
    if (name=="" or age=="" or gender=="" or blood_group==""):
        showErrorText(window, "error: enter required information.", 35, 280, 530)
        return
    addUserDetails(username, name, age, gender, blood_group) 
    if sym1 == "":
        showErrorText(window, "error: enter atleast one symptom.", 35, 280, 530)
        return
    elif all(x not in all_symptoms for x in [sym1,sym2,sym3]):
        showErrorText(window, "error: enter existing symptom.", 35, 280, 530)
        return
    predicted_diseases = getDiseaseFromSymptoms(sym1, sym2, sym3)
    showDisease(window, predicted_diseases)
    addDiseasesToUserTable(username, predicted_diseases)

def loginCallback(window, username, password):
    if username == "":
        showErrorText(window, "Enter username.", 20, 90, 150)
        return
    if password == "":
        showErrorText(window, "Enter password.", 20, 90, 150)
        return
    retval = manageUser (window, username, password)  
    if retval == 0:
        if username == "admin":
            win3()
        else:
            win1(username)
    else:
        showErrorText(window, "Incorrect password.", 20, 90, 150)


def dropdown(entry, options, all_list):
    text = entry.get()
    if (text != ""):
        options["values"] = difflib.get_close_matches(text, all_list, n=10, cutoff=0.1)
    else:
        options["values"] = all_list

def win1(username):

    window = Tk()
    window.title('Disease prediction window')
    window.geometry("800x800")

    all_symptoms = getAllSymptoms()
    userdata = getUserHistory(username)

    label_1 = Label(window, text="Previous predicted diseases")
    label_1.place(x=90,y=45)

    text_1 = Text(window, height = 3, width = 35)
    diseases_str = ""
    diseases_str = str(userdata['pre_disease1']) + "\n" + str(userdata['pre_disease2']) + "\n" + str(userdata['pre_disease3'])
    text_1.insert(END, diseases_str)
    text_1.place(x=250,y=30)

    label_2 = Label(window, text="Name*")
    entry_2 = Entry(window)
    label_2.place(x=90,y=100)
    entry_2.place(x=200,y=100)

    label_3 = Label(window, text="Age*")
    entry_3 = Entry(window)
    label_3.place(x=90,y=140)
    entry_3.place(x=200,y=140)

    label_4 = Label(window, text="Gender*")
    entry_4 = StringVar(window)
    male_4 = Radiobutton(window, text='Male', value='male', variable=entry_4, tristatevalue=0)
    female_4 = Radiobutton(window, text='Female', value='female', variable=entry_4, tristatevalue=0)
    label_4.place(x=90,y=180)
    male_4.place(x=200,y=180)
    female_4.place(x=300, y=180)

    label_5 = Label(window, text="Blood group*")
    entry_5 = StringVar(window)
    bg_options = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    bg_dropdown = Combobox(window, textvariable=entry_5, width=10, values=bg_options)
    label_5.place(x=90,y=220)
    bg_dropdown.place(x=200, y=220)

    label_6 = Label(window, text="Symptom 1*")
    entry_6 = StringVar(window)
    sym1_options = all_symptoms
    # sym1_dropdown = Combobox(window, textvariable=entry_6, width=20, values=sym1_options)
    sym1_dropdown = Combobox(window, textvariable=entry_6, width=20, values=sym1_options, postcommand= lambda: 
                            dropdown(entry_6, sym1_dropdown, all_symptoms))
    label_6.place(x=90, y=260)
    sym1_dropdown.place(x=90, y=280)

    label_7 = Label(window, text="Symptom 2")
    entry_7 = StringVar(window)
    sym2_options = all_symptoms
    sym2_dropdown = Combobox(window, textvariable=entry_7, width=20, values=sym2_options, postcommand= lambda:
                            dropdown(entry_7, sym2_dropdown, all_symptoms))
    label_7.place(x=290, y=260)
    sym2_dropdown.place(x=290, y=280)

    label_8 = Label(window, text="Symptom 3")
    entry_8 = StringVar(window)
    sym3_options = all_symptoms
    sym3_dropdown = Combobox(window, textvariable=entry_8, width=20, values=sym3_options, postcommand= lambda:
                            dropdown(entry_8, sym3_dropdown, all_symptoms))
    label_8.place(x=490, y=260)
    sym3_dropdown.place(x=490, y=280)

    # btn1=Button(window, text="Get History", command= lambda: historyCallback(entry_1.get()))

    btn2=Button(window, text=" SUBMIT ", command= lambda:
                submitCallback(window, username, entry_2.get(), entry_3.get(), entry_4.get(),
                entry_5.get(), entry_6.get(), entry_7.get(), entry_8.get()))

    btn2.place(x=350, y=500)

    window.mainloop()


def win2():
    window = Tk()
    window.title('Login window')
    window.geometry("400x400")

    label_1 = Label(window, text="Username*")
    entry_1 = Entry(window)
    label_1.place(x=90,y=60)
    entry_1.place(x=200,y=60)

    label_2 = Label(window, text="Password*")
    entry_2 = Entry(window)
    label_2.place(x=90,y=100)
    entry_2.place(x=200,y=100)

    btn=Button(window, text="Login", command= lambda:
                loginCallback(window, entry_1.get(), entry_2.get()))

    btn.place(x=150, y=200)

    window.mainloop()


def win3():
    window = Tk()
    window.title('Admin access window')
    window.geometry("800x800")

    all_symptoms = getAllSymptoms()

    label_1 = Label(window, font=("Calibri", 13), text="Add/modify disease")
    label_1.place(x=90,y=60)

    label_2 = Label(window, text="Disease*")
    entry_2 = Entry(window)
    label_2.place(x=40, y=140)
    entry_2.place(x=40, y=160)

    label_3 = Label(window, text="Symptom 1*")
    entry_3 = StringVar(window)
    sym1_options = all_symptoms
    sym1_dropdown = Combobox(window, textvariable=entry_3, width=20, values=sym1_options, postcommand= lambda: 
                            dropdown(entry_3, sym1_dropdown, all_symptoms))
    label_3.place(x=190, y=140)
    sym1_dropdown.place(x=190, y=160)

    label_4 = Label(window, text="Symptom 2")
    entry_4 = StringVar(window)
    sym2_options = all_symptoms
    sym2_dropdown = Combobox(window, textvariable=entry_4, width=20, values=sym2_options, postcommand= lambda:
                            dropdown(entry_4, sym2_dropdown, all_symptoms))
    label_4.place(x=360, y=140)
    sym2_dropdown.place(x=360, y=160)

    label_5 = Label(window, text="Symptom 3")
    entry_5 = StringVar(window)
    sym3_options = all_symptoms
    sym3_dropdown = Combobox(window, textvariable=entry_5, width=20, values=sym3_options, postcommand= lambda:
                            dropdown(entry_5, sym3_dropdown, all_symptoms))
    label_5.place(x=530, y=140)
    sym3_dropdown.place(x=530, y=160)

    btn1=Button(window, text="Apply changes", command= lambda:
                addModifyDisease(window, entry_2, entry_3, entry_4, entry_5))
    btn1.place(x=300, y=200)

    label_6 = Label(window, font=("Calibri", 13), text="Delete disease")
    label_6.place(x=90,y=300)

    label_7 = Label(window, text="Disease*")
    entry_7 = StringVar(window)
    all_diseases = getAllDiseases()
    disease_options = all_diseases
    disease_dropdown = Combobox(window, textvariable=entry_7, width=20, values=disease_options, postcommand= lambda:
                                dropdown(entry_7, disease_dropdown, all_diseases))
    label_7.place(x=280, y=380)
    disease_dropdown.place(x=280, y=400)

    btn2=Button(window, text="Apply changes", command= lambda:
                deleteDisease(window, entry_7))
    btn2.place(x=300, y=430)

    window.mainloop()

win2()
