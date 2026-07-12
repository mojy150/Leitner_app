from customtkinter import *
import leitner
import ctypes
from tkinter import messagebox
import csv
from random import choice
import datetime
from tempfile import NamedTemporaryFile
import shutil
import pyttsx3

basic_csv = 'basic.csv' # csv of word
time_csv = 'time.csv' # csv of t
enable_click = False
                                                                                                    # main
window = CTk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f'{width}x{height}+0+0')

                                                                                                    # wight of row & column for main
window.grid_columnconfigure([0],weight=3)
window.grid_columnconfigure([1],weight=1)
window.grid_rowconfigure([0],weight=1)
                                                                                                    # create left tab
my_tabs = CTkTabview(window,)                                   
my_tabs.add("Leitner")                                 
my_tabs.add("Input Word")
my_tabs.add("Status")
my_tabs.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)
                                                                                                    # create 2 frame in tab Leitner

my_tabs.tab("Leitner").grid_columnconfigure([0],weight=3)
my_tabs.tab("Leitner").grid_columnconfigure([1],weight=1)
my_tabs.tab("Leitner").grid_rowconfigure([0],weight=1)

Leitner_frame = CTkFrame(my_tabs.tab("Leitner"))
Leitner_frame.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)

input_new_word = CTkFrame(my_tabs.tab("Leitner"))
input_new_word.grid(column=1,row=0,sticky='nsew',padx=10,pady=10)
                                                                                                    # create right frame
myframe2 = CTkScrollableFrame(window)
myframe2.grid(column=1,row=0,sticky='nsew',padx=10,pady=10)


                                                                                                    # tab Leitner

def Start_Leitner():
    Run_Leitner_btn.configure(state="disabled")
    Exit_Leitner_btn.configure(state="normal")
    global enable_click
    enable_click = True
    Flash_card_label.configure(text="en")
    Question_label.configure(text="click the flash card!")
    number_new_word_input.configure(state="disabled")
    number_new_word_btn.configure(state="disabled")


Run_Leitner_btn = CTkButton(Leitner_frame,
                text="Start Leitner",
                command=Start_Leitner)
Run_Leitner_btn.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)

number_question = 0
def flash_card_func(event):
    global number_question
    number_question +=1
    if enable_click == True:    
        if number_question % 2 == 0:
            Flash_card_label.configure(text="en")
            Question_label.configure(text="click the flash card!")
        else:
            Flash_card_label.configure(text="fr")
            Question_label.configure(text="your quess is true?")
            True_Rbtn.configure(state="normal")
            False_Rbtn.configure(state="normal")
            check_btn.configure(state="normal")
    

Flash_card_label = CTkLabel(Leitner_frame,
                text="start the Leitner to show the flash card!",border_color="black",border_width=2,corner_radius=10)
Flash_card_label.grid(sticky='nsew',padx=10,pady=10) # TODO
Flash_card_label.bind("<Button-1>", flash_card_func)

Question_label = CTkLabel(Leitner_frame,
                text="")
Question_label.grid(sticky='nsew',padx=10,pady=10) # TODO


controller_var = IntVar(value=2)

True_Rbtn = CTkRadioButton(Leitner_frame,
                           text="Yes",
                           variable=controller_var,
                           value=1,state="disabled")
True_Rbtn.grid(sticky='nsew',padx=10,pady=10)       # TODO                

False_Rbtn = CTkRadioButton(Leitner_frame,
                            text="No",
                            variable=controller_var,
                            value=0,state="disabled")
False_Rbtn.grid(sticky='nsew',padx=10,pady=10)      # TODO

def check_btn_func():
    if controller_var.get() != 2:
        text = ""
        if controller_var.get() == 0:
            text = f"[No] I didn't know {"en"} meant {"fr"}"
        elif controller_var.get() == 1:
            text = f"[Yes] I did know {"en"} meant {"fr"}"
        lbl = CTkLabel(myframe2,text=text,
                    font=CTkFont(family="Vazir"))
        lbl.grid()
        controller_var.set(2)
        Flash_card_label.configure(text="en")
        Question_label.configure(text="click the flash card!")
    else:
        messagebox.showwarning("هشدار","لطفا یک دکمه را انتخاب کنید")

check_btn = CTkButton(Leitner_frame,
                      text="Apply the guess",
                      state="disabled",
                      command=check_btn_func,)
check_btn.grid(sticky='nsew',padx=10,pady=10) # TODO

def Exit_Leitner():
    Run_Leitner_btn.configure(state="normal")
    Exit_Leitner_btn.configure(state="disabled")
    global enable_click
    enable_click = False
    Flash_card_label.configure(text="start the Leitner to show the flash card!")
    Question_label.configure(text="")
    controller_var.set(2)
    False_Rbtn.configure(state="disabled",variable=controller_var)
    True_Rbtn.configure(state="disabled",variable=controller_var)
    number_new_word_input.configure(state="normal")
    number_new_word_btn.configure(state="normal")
    check_btn.configure(state="disabled")

Exit_Leitner_btn = CTkButton(Leitner_frame,
                             text="exit Leitner",
                             state="disabled",
                             command=Exit_Leitner)
Exit_Leitner_btn.grid(sticky='nsew',padx=10,pady=10)

                                                                                                    # new word


new_word_babel = CTkLabel(input_new_word,
                    text="We have some words already prepared.\n how many would you like to add?")
new_word_babel.grid(sticky='nsew',padx=10,pady=10)

def turn_on_numlock(event=None):
    VK_NUMLOCK = 0x90

                        # وضعیت فعلی Num Lock
    if not ctypes.windll.user32.GetKeyState(VK_NUMLOCK) & 1:
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 2, 0)

number_new_word_input = CTkEntry(input_new_word,                          
                      placeholder_text="give me the number: ")
number_new_word_input.grid(pady=10)
number_new_word_input.bind("<FocusIn>", turn_on_numlock)


def get_number_new_word():
    try:
        number_new_word = number_new_word_input.get().strip()
        number_new_word = int(number_new_word)
        text = (f"[{number_new_word}] new word added to your Leitner")
        id_0 = []
        number = "0"
        selected_new_word = []
        filename = basic_csv
        with open(filename) as f:
            reader = csv.reader(f)
            counter = int(0)
            if number == '0':
                for row in reader:
                    if row[3] == number:
                        id_0.append([row[0],row[1],row[2],1,'off'])
                        counter +=1
                if counter != 0:
                    if number_new_word > len(id_0):
                        number_new_word = len(id_0)
                        text = ('all new words in csv is [%i] and added to your Leitner' % (number_new_word))
        selected_new_word = leitner.my_append(id_0,selected_new_word,number_new_word)
        selected_new_word.sort(key=lambda x: int(x[0]))

        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

        with open(filename, 'r', newline='') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            writer = csv.writer(tempfile, delimiter=',', quotechar='"')

            def select_in_list(selected_new_word):
                try:
                    return selected_new_word.pop(0)
                except:
                    pass
            temp_list = select_in_list(selected_new_word)
            for row in reader:
                if temp_list == None:
                    pass
                elif temp_list[0] == row[0]:
                    row[0],row[1],row[2],row[3],row[4] = temp_list[0],temp_list[1],temp_list[2],temp_list[3],temp_list[4]
                    temp_list = select_in_list(selected_new_word)
                writer.writerow(row)

        shutil.move(tempfile.name, filename)
                
                
        number_new_word_lbl = CTkLabel(myframe2,
                                       text=text,)
        number_new_word_lbl.grid()
        number_new_word_input.delete(0,END)
    except:
        messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید")
        number_new_word_input.delete(0,END)


number_new_word_btn = CTkButton(input_new_word,
                         text="add the word",
                         command=get_number_new_word)
number_new_word_btn.grid(sticky='nsew',padx=10,pady=10)

                                                                                                    # tab Input Word

def focus_en(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04090409, 0)


en_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="english: ",)
en_input.grid(pady=10)
en_input.bind("<FocusIn>", focus_en)

def focus_fr(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

fr_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text=" :فارسی",
                      justify="right",
                      font=CTkFont(family="Vazir"))
fr_input.grid(pady=10)
fr_input.bind("<FocusIn>", focus_fr)


new_word = int(0)
def add_the_word():
    if en_input.get().strip() != "" and fr_input.get().strip() != "":
        global new_word
        text_en_input= en_input.get().strip()
        text_fr_input= fr_input.get().strip()
        leitner.append_list_as_row(leitner.basic_csv,
                                [str(leitner.last_id() +1),
                                    text_en_input,text_fr_input,'1','off'])
        new_word +=1
        text = '[%i]You add [%s] => [%s]' % (new_word,
                                             text_en_input,
                                             text_fr_input)
        lbl = CTkLabel(myframe2,text=text,
                    font=CTkFont(family="Vazir"))
        lbl.grid()
        en_input.delete(0,END)
        fr_input.delete(0,END)
    else:
        messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

add_word_btn = CTkButton(my_tabs.tab("Input Word"),
                         text="add the word",
                         command=add_the_word)
add_word_btn.grid(sticky='nsew',padx=10,pady=10)

                                                                                                    # Tab Status
status_labels = []                      # بیرون تابع تعریف کن
def Show_status():
    global status_labels

                        # حذف لیبل‌های قبلی
    for lbl in status_labels:
        lbl.destroy()

    status_labels.clear()

    show_list = leitner.show()

    row = 1
    for i in range(len(show_list)):
        if show_list[i] != 0:
            text = 'value words [%s] day house is [%i]' % (i, show_list[i])

            lbl = CTkLabel(
                my_tabs.tab("Status"),
                text=text,
                font=CTkFont(size=15)
            )

            lbl.grid(row=row, column=0, sticky='nw', padx=10, pady=2)

            status_labels.append(lbl)
            row += 1


Show_status_btn = CTkButton(
    my_tabs.tab("Status"),
    text="Show status",
    command=Show_status
)

Show_status_btn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)




window.mainloop()