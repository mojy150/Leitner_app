from random import choice
import pyttsx3
import sqlite3

conn = sqlite3.connect("Leitner_DB.db")
cursor = conn.cursor()

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def my_append(id_0,questionToday_list,temp): # append random word in questionToday_list
    while temp != 0:
        no_random = choice(id_0)
        questionToday_list.append(no_random)
        id_0.remove(no_random)
        temp -= 1
    return questionToday_list

def check(Table_name,number_day,id_0,questionToday_list,list_another): # check for new word or old word
    id_0 = []   
    temp = int(0)

    if number_day == 'another':
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day NOT IN ({0},{1},{3},{7},{15},{30},{31})")
        list_another.extend(cursor.fetchall())

    else:
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day = {number_day}")
        reader = cursor.fetchall()

        for row in reader:
            id_0.append([row[0],row[1],row[2],row[3],'on'])
        temp = len(id_0)

    questionToday_list = my_append(id_0,questionToday_list,temp)
    return questionToday_list

def check_again(Table_name,number_day,questionToday_list): # check again for new word or old word
    id_0 = []   
    temp = int(0)
    cursor.execute(f"SELECT * FROM {Table_name} WHERE on_off = ? AND day = ?"
                   ,("on",number_day))
    id_0.extend(cursor.fetchall())
    temp = len(id_0)
    questionToday_list = my_append(id_0,questionToday_list,temp)
    return questionToday_list

def last_id(Table_name): # give the last id
    cursor.execute(f"SELECT MAX(id) FROM {Table_name}")
    last_id = cursor.fetchone()[0]
    if last_id == None:
        last_id = 0
    return last_id

def append_list_as_row(Table_name,row): # send new word in database
    cursor.execute(f"""
            INSERT INTO {Table_name} VALUES (?, ?,?,?,?)
            """,
            (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
            ))
    conn.commit()
        
def edit_database(Table_name,line0,line1,line2,line3,line4): # edit batabase for Flashcards
    cursor.execute(f"UPDATE {Table_name} SET question=?,answer=?,day=?,on_off=? WHERE id = ?",
                   (line1,
                    line2,
                    line3,
                    line4,
                    line0
                    ))
    conn.commit()

def show(Table_name):
    show_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    cursor.execute(f"SELECT day FROM {Table_name}")
    Id_data = cursor.fetchall()

    for row in Id_data:
        # show_list[int(row[3])] += 1
        show_list[row[0]] += 1
    return show_list