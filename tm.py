import csv
from tkinter import *
from tkinter import messagebox
import datetime
import logging
import json
import sqlite3
from sqlite3 import Error
import os.path

logfile = 'csvtlogs.log'
dbfile = 'tasks.db'
jsonfile = 'database.json'
plist = []


# Settings for Logging
logging.basicConfig(filename=logfile, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# try to connect to the sql database, will show error in case of any problem
try:

    if not os.path.isfile(dbfile):
        conn = sqlite3.connect(dbfile)
        # the creation of the table in first running:
        c = conn.cursor()
        c.execute("""CREATE TABLE tasks (
                title text,
                course_name text,
                course_num int,
                edate text
             )""")

        conn.commit()

    conn = sqlite3.connect(dbfile)

    logging.info('Connection to SQL Database: {}'.format(sqlite3.version))

    # print(sqlite3.version)

except Error as e:

    messagebox.showinfo('Error', e)

c = conn.cursor()


def checkForJson():
    if not os.path.isfile(jsonfile):
        with open(jsonfile, 'w') as db:
            json.dump([], db)



# return the num of selected item in listbox(lb)
def whisel():
    if len(lb.curselection()) <= 0:
        return
    return int(lb.curselection()[0])


# adding employee to the listbox and tp the json and SQL db and write logg:
def addemp():
    checkForJson()
    with open(jsonfile, 'w') as db:
        row = ([titlevar.get(), namevar.get(), numvar.get(), datevar.get()])
        plist.append(row)
        json.dump(plist, db)
    setselect()
    logging.info('Add: {}  {} {} {}'.format(titlevar.get(), namevar.get(), numvar.get(), datevar.get()))
    db.close()
    with conn:
        c.execute("INSERT INTO tasks VALUES (:title, :course_name, :course_num, :edate)",
                  {'title': titlevar.get(), 'course_name': namevar.get(), 'course_num': numvar.get(), 'edate': datevar.get()})



# loading the value from json by which selected item in listbox and write logg
def load():
    checkForJson()    
    with open(jsonfile) as db:
    
        jsc = json.load(db)
        plist = []
        for i in jsc:
            plist.append(i)
        if whisel() == None:
            return
        name, course_name, pay, pos = plist[whisel()]
        titlevar.set(name)
        namevar.set(course_name)
        numvar.set(pay)
        datevar.set(pos)
    logging.info('Load: {} {} {} {}'.format(name, course_name, pay, pos))
    db.close()


#Function that load the db to list(plist) and delete the selected
#item (using whicsel func) from the list and then Dump the list to
#db (without the deleted item)
def dele():

    checkForJson()
    with open(jsonfile) as db:
        jsc = json.load(db)
        plist = []
        for i in jsc:
            plist.append(i)
        db.close()
        if whisel() != None:
            logging.info('Delete: {} {} {} {}'.format(plist[whisel()][0], plist[whisel()][1], plist[whisel()][2], plist[whisel()][3]))
            tempd = plist[whisel()][0]
            del plist[whisel()]

            with open(jsonfile, 'w') as dbb:
                json.dump(plist, dbb)
                setselect()
                dbb.close()
                with conn:
                    c.execute("DELETE from tasks WHERE title = :title",
                    {'title': tempd})



# use class arttibute for Frames (fr1, fr2...)
class main:

    def __init__(self, fr0, fr1, fr2, fr3, fr4, fr5, fr6):

        self.fr0 = fr0
        self.fr1 = fr1
        self.fr2 = fr2
        self.fr3 = fr3
        self.fr4 = fr4
        self.fr5 = fr5
        self.fr6 = fr6

        # setting the fr Variables to a tk Frames
        self.fr0 = Frame(tek)
        self.fr1 = Frame(tek)
        self.fr2 = Frame(tek)
        self.fr3 = Frame(tek)
        self.fr4 = Frame(tek)
        self.fr5 = Frame(tek)
        self.fr6 = Frame(tek)
        global titlevar, namevar, numvar, datevar
        

        #Frame 0:
        fk = ('david', 20, 'bold')
        tit = Label(self.fr0, text="tasks Manager")
        #tit.config(font=fk, bg='lightgrey')
        tit.pack(side=BOTTOM)


        #Frame 1:
        Label(self.fr1, text="Task Title: ").pack()
        titlevar = StringVar()
        titleent = Entry(self.fr1, textvariable=titlevar)
        titleent.pack()
        Label(self.fr1, text="Course Name: ").pack()
        namevar = StringVar()
        nameent = Entry(self.fr1, textvariable=namevar)
        nameent.pack()


        #Frame 2:
        Label(self.fr2, text="Course Number: ").pack()
        numvar = StringVar()
        nument = Entry(self.fr2, textvariable=numvar)
        nument.pack()
        Label(self.fr2, text="Submission Date: ").pack()
        datevar = StringVar()
        dateent = Entry(self.fr2, textvariable=datevar)
        dateent.pack()


        #Frame 3:
        Button(self.fr3, text="Add", command=addemp).pack(side=LEFT)
        Button(self.fr3, text="Delete", command=dele).pack(side=LEFT)
        Button(self.fr3, text="Show", command=load).pack(side=LEFT)


        #Frame 4:
        global lb
        lb = Listbox(self.fr4, width=40, height=18)
        lb.pack(side='left', fill='y')
        scb = Scrollbar(self.fr4,orient='vertical', command=lb.yview)
        scb.pack(side='right', fill='y')
        lb.config(yscrollcommand=scb.set)


        #Frame 5:

        #Statistics for the EM
        def totsal():
        
            checkForJson()

            totemp = 0

            with open(jsonfile, 'r') as db:
                jsc = json.load(db)
                for i in jsc:
                    totemp += 1
                totempp = StringVar()
                totempp.set("     Total Tasks: {}".format(totemp))


                #Label Counting the All tasks
                tote = Label(self.fr5, textvariable=totempp)
                tote.pack(side=LEFT)
            db.close()
            setselect()


            #Function that  removing the existing Statistic label and Create Updated ones
            def dstat():
                bb.pack_forget()
                tote.pack_forget()
                totsal()


            bb = Button(self.fr6, text='Update Statistics', command=dstat)
            bb.pack()


        # Packing the Frames (Changing the order will cause bugs in the GUI)
        self.fr0.pack(side=TOP)
        self.fr6.pack(side=BOTTOM)
        self.fr5.pack(side=BOTTOM)
        self.fr4.pack(side=BOTTOM)
        self.fr3.pack(side=BOTTOM)
        self.fr1.pack(side=LEFT)
        self.fr2.pack(side=RIGHT)
        totsal()



# Func that inserting the Plist to the Listbox(lb)
def setselect():

    lb.delete(0, END)
    checkForJson()


    with open(jsonfile, 'r') as db:
        jsc = json.load(db)
        plist = []
        for i in jsc:
            plist.append(i)
        for n in plist:
            lb.insert(END, n[0])


# manuly value for db(s)
# emp0 = ('Almog Ben', '0528784977', 25000, 'CEO')
# emp1 = ('Matan Peretz', '05487787448', 2000, 'Dev')
# emp2 = ('Ben Jako', '05256547898', 3000, 'Desigener')
# emp3 = ('Samir Tol', '05697555665', 2350, 'Dev')
# emp4 = ('Tamir Shalom', '0521488955', 7650, 'CTO')
# emp5 = ('Dani Loriel', '0923283899', 4000, 'Head of Devs')
# emp6 = ('Liron Rotman', '053580285', 2000, 'Dev')
# insert_emp(emp0)
# insert_emp(emp1)
# insert_emp(emp2)
# insert_emp(emp3)
# insert_emp(emp4)
# insert_emp(emp5)
# insert_emp(emp6)


# The starter of the Script
if __name__ == '__main__':

    tek = Tk()
    tek.title("Task Manager")
    tek.geometry("400x600")
    main(fr0=tek, fr1=tek, fr2=tek, fr3=tek, fr4=tek, fr5=tek, fr6=tek)
    setselect()
    tek.mainloop()
