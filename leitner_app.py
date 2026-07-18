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

engine = pyttsx3.init()
engine.setProperty('rate', 170)
basic_csv = 'basic.csv' # csv of word
time_csv = 'time.csv' # csv of time
setting_csv = "setting_data.csv"
enable_click = False
en_question = ""
fr_question = ""
Answer = "s"
sure = "null"
questionToday_list = list()
generator = None
number_question = 0
font_size = 15
flashcard_font_size = 15
                                                                                                    # main
window = CTk()
fr_font = CTkFont(family="vazir",size=15)
en_font = CTkFont(family="Arial",size=15)
flashcard_fr_font = CTkFont(family="vazir",size=15)
flashcard_en_font = CTkFont(family="Arial",size=15)
                                                                                                    # wight of row & column for main
window.grid_columnconfigure([0],weight=0)
window.grid_columnconfigure([1],weight=4)
window.grid_columnconfigure([2],weight=2)
window.grid_rowconfigure([0],weight=1)
                                                                                                    # create left tab
my_tabs = CTkTabview(window,)                                   
my_tabs.add("Leitner")                                 
my_tabs.add("Input Word")
my_tabs.add("Status")
my_tabs.grid(column=1,row=0,sticky='nsew',padx=10,pady=10)
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
myframe2.grid(column=2,row=0,sticky='nsew',padx=10,pady=10)

myframe2.grid_columnconfigure(0, weight=1)

                                                                                                    # setting
settings_frame = CTkFrame(
    window,
    corner_radius=15,
    border_width=2,
    fg_color="#2B2B2B"
)

num_setting = 0
def show_settings():
    global num_setting
    if num_setting % 2 == 0:
        settings_frame.place(
            relx=0,
            rely=0,
            relwidth=0.24,
            relheight=1,
            anchor="nw"
        )
        num_setting +=1
    else:
        settings_frame.place_forget()
        num_setting +=1
        save_setting_func()

settings_btn = CTkButton(
    window,
    text="Settings",
    font=en_font,
    command=show_settings
)
settings_btn.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)
                                                                                                    # setting Theme
def theme_func():
    global Theme_text
    if theme_switch.get() == "on":
        set_appearance_mode("dark")
        theme_switch.configure(text="dark mode")
        settings_frame.configure(fg_color="#2B2B2B")
    else:
        set_appearance_mode("light")
        theme_switch.configure(text="light mode")
        settings_frame.configure(fg_color="#F2F2F2")

settings_frame.grid_columnconfigure(0, weight=1)

theme_switch = CTkSwitch(settings_frame,
                        text="dark mode",
                        font=en_font,
                        onvalue="on",
                        offvalue="off",
                        variable=StringVar(value="on"),
                        command=theme_func)
theme_switch.grid(
    row=0,
    column=0,
    padx=20,
    pady=20,
    sticky="e"
)
                                                                                                    # setting read data
def read_setting():
    global font_size
    with open(setting_csv) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == "theme":
                if row[1] == "dark":
                    theme_switch.select()
                    set_appearance_mode("dark")
                    theme_switch.configure(text="dark mode")
                    settings_frame.configure(fg_color="#2B2B2B")
                else:
                    theme_switch.deselect()
                    set_appearance_mode("light")
                    theme_switch.configure(text="light mode")
                    settings_frame.configure(fg_color="#F2F2F2")
            elif row[0] == "font_size":
                font_size = int(row[1])
                en_font.configure(size=font_size)
                fr_font.configure(size=font_size)
            elif row[0] == "font_size_flashcard":
                flashcard_font_size = int(row[1])
                flashcard_en_font.configure(size=flashcard_font_size)
                flashcard_fr_font.configure(size=flashcard_font_size)

read_setting()
                                                                                                    # setting save data
def save_setting_func():
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

    with open(setting_csv, 'r', newline='') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')

        for row in reader:
            if row[0] == "theme":
                if theme_switch.get() == "on":
                    row[1] = "dark"
                else:
                    row[1] = "light"
            elif row[0] == "font_size":
                row[1] = str(font_size)
            elif row[0] == "font_size_flashcard":
                row[1] = str(flashcard_font_size)


            writer.writerow(row)

    shutil.move(tempfile.name, setting_csv)
                                                                                                    # setting font size
font_size_label = CTkLabel(settings_frame,
                           text = "font size",
                           font=CTkFont(size=15)
                        #    font=en_font,      #TODO
                           )
font_size_label.grid(row=1,column=0,padx=35,sticky="e")

def set_font_size(value):
    global font_size
    font_size = int(value)
    font_size_label.configure(text=f"font size : {font_size}")
    en_font.configure(size=font_size)
    fr_font.configure(size=font_size)

font_size_slider = CTkSlider(settings_frame,
                      from_=10,                                  # کمترین مقدار
                      to=32,                                     # بیشترین مقدار
                      variable=IntVar(value=font_size),     
                      command=set_font_size,
                      number_of_steps=11,width=130)                      # به چند بخش تقسیم بشه
font_size_slider.grid(row=2,column=0,padx=10,pady=10,sticky="e")
                                                                                                    # setting flashcard font size
flashcard_font_size_label = CTkLabel(settings_frame,
                           text = "flashcard font size",
                           font=CTkFont(size=18)
                        #    font=en_font,      #TODO
                           )
flashcard_font_size_label.grid(row=3,column=0,padx=35,sticky="e")

def set_font_size(value):
    global flashcard_font_size
    flashcard_font_size = int(value)
    flashcard_font_size_label.configure(text=f"flashcard font size: {flashcard_font_size}")
    flashcard_en_font.configure(size=flashcard_font_size)
    flashcard_fr_font.configure(size=flashcard_font_size)

flashcard_font_size_slider = CTkSlider(settings_frame,
                      from_=10,                                  # کمترین مقدار
                      to=36,                                     # بیشترین مقدار
                      variable=IntVar(value=flashcard_font_size),     
                      command=set_font_size,
                      number_of_steps=13,
                      width=130)                      # به چند بخش تقسیم بشه
flashcard_font_size_slider.grid(row=4,column=0,padx=10,pady=10,sticky="e")

settings_save_btn = CTkButton(
    settings_frame,
    text="Save Setting",
    font=en_font,
    command=save_setting_func,
)
settings_save_btn.grid(padx=10,pady=10,sticky="se")

                                                                                                    # tab Leitner

def leitner_func(): # question words
    global en_question
    global fr_question
    global Answer
    global questionToday_list
    global list_another
    # sure = 'null'
    for item in questionToday_list:
        if item[4] == 'on':
            # print(item[1])
            en_question = item[1]
            Flash_card_label.configure(text=en_question)
            Question_label.configure(text="click the flash card!")
            # engine.say(en_question)
            # engine.runAndWait()
            # Question_label.configure(text="click the flash card!")
            # engine.say(en_question)
            # engine.runAndWait()
            fr_question = item[2]
            # temp = input(' you want continue? (y/n): ')
            yield item
            # if temp == 'n' or temp == 'N':
            #     sure = input('are you sure? (y/n): ')
            #     if sure == 'n' or sure == 'N':
            #         temp = 'y' # TODO
            #     elif sure == 'y' or sure == 'Y' or sure == '':
            #         print('leitner is off!')
            #         break
            
            # if temp == 'y' or temp == 'Y' or temp == '':
            # print('[%s] meant [%s]' % (item[1] , item[2]))
            # Flash_card_label.configure(text=item[2])
            # javab = input('your hads is true? (y/n): ')
            # while True:
            # print("now",Answer)
            if Answer == 'n' or Answer == 'N':
                item[3] , item[4] = '1' , 'off'
                # i +=1
                # print(Answer)
                Answer = ""
            elif Answer == 'y' or Answer == 'Y':
                item[3] , item[4] = str(int(item[3]) + 1) , 'off'
                # print(Answer)
                # i +=1
                Answer = ""
    # return sure
    # if sure != 'y' or sure != 'Y' or sure != '':
    #     for row in list_another:
    #         if (row[0] == '1' or row[0] == '3' or row[0] == '7' or row[0] == '15' or row[0] == '30') and row[4] == 'off':
    #             leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],'on')
                
    #         elif row[0] != '0' or row[0] != '1' or row[0] != '3' or row[0] != '7' or row[0] != '15' or row[0] != '30':
    #         # TODO elif or else
    #             leitner.edit_csv(basic_csv,row[0],row[1],row[2],str(int(row[3]) +1),row[4]) # TODO (row[4] or 'off')
    
    
    # questionToday_list.sort() # TODO
    # print(questionToday_list)
    # for row in questionToday_list: # TODO
    #     edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])

def Run_Leitner():
    global generator
    global questionToday_list
    global list_another
    global number_question
    with open(basic_csv) as f:
        reader = csv.reader(f)
        id_0 = list() # list Ids in CSV
        questionToday_list = list() # list word of question day
        list_another = list() # list word of does't question day
        questionToday_list = []
        with open(time_csv) as time_tomorrow:
            reader = csv.reader(time_tomorrow)
            for row in reader:
                tomorrow_year , tomorrow_month , tomorrow_day = int(row[0]) , int(row[1]) , int(row[2])
            e = datetime.datetime.now()
            if e.year > tomorrow_year or (e.year == tomorrow_year and e.month > tomorrow_month) or (e.year == tomorrow_year and e.month == tomorrow_month and e.day >= tomorrow_day):
                leitner.check(basic_csv,'30',id_0,questionToday_list)
                leitner.check(basic_csv,'15',id_0,questionToday_list)
                leitner.check(basic_csv,'7',id_0,questionToday_list)
                leitner.check(basic_csv,'3',id_0,questionToday_list)
                leitner.check(basic_csv,'1',id_0,questionToday_list)
                leitner.check(basic_csv,'another',id_0,list_another)
                try:
                    generator = leitner_func()
                    sure = next(generator)
                except:
                    if len(questionToday_list) == 0:
                        text = "The Leitner is empty, but if you want, you can add a new word or add one of our ready-made words to your Leitner."
                        text_box = CTkTextbox(
                                    myframe2,
                                    wrap="word",
                                    height=50,
                                    font=en_font
                                )
                        text_box.insert("0.0", text)
                        text_box.configure(state="disabled")
                        text_box.grid(row=0, column=0, sticky="ew")
                        Exit_Leitner_btn.invoke()
                        # print('len list is zero (0).')
                # if sure != 'y' or sure != 'Y' or sure != '':
                #     for row in list_another:
                #         if (row[0] == '1' or row[0] == '3' or row[0] == '7' or row[0] == '15' or row[0] == '30') and row[4] == 'off':
                #             leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],'on')
                            
                #         elif row[0] != '0' or row[0] != '1' or row[0] != '3' or row[0] != '7' or row[0] != '15' or row[0] != '30':
                #         # TODO elif or else
                #             leitner.edit_csv(basic_csv,row[0],row[1],row[2],str(int(row[3]) +1),row[4]) # TODO (row[4] or 'off')
                # tomorrow = datetime.date.today() + datetime.timedelta(days=1) # TODO
                # leitner.edit_time_csv(time_csv,tomorrow.year,tomorrow.month,tomorrow.day)
                
                # if len(questionToday_list) == 0:
                #     print('len list is zero (0).')
                # # questionToday_list.sort() # TODO
                # # print(questionToday_list)
                
                # for row in questionToday_list:
                #     leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
            else:
                number_question = 0
                questionToday_list = []
                leitner.check_again(basic_csv,'30',questionToday_list)
                leitner.check_again(basic_csv,'15',questionToday_list)
                leitner.check_again(basic_csv,'7',questionToday_list)
                leitner.check_again(basic_csv,'3',questionToday_list)
                leitner.check_again(basic_csv,'1',questionToday_list)
                leitner.check_again(basic_csv,'0',questionToday_list)
                try:
                    generator = leitner_func()
                    sure = next(generator)
                except:
                    if len(questionToday_list) == 0:
                        text = "The Leitner is empty, but if you want, you can add a new word or add one of our ready-made words to your Leitner."
                        text_box = CTkTextbox(
                                    myframe2,
                                    wrap="word",
                                    height=50,
                                    font=en_font
                                )
                        text_box.insert("0.0", text)
                        text_box.configure(state="disabled")
                        text_box.grid(row=0, column=0, sticky="ew")
                        Exit_Leitner_btn.invoke()
                # if len(questionToday_list) == 0:
            #         print("you can'n use leitner now")
            #         temp = input('but you can insert new word\n you want continue? (y/n): ')
            #         if temp == 'y' or temp == 'Y' or temp == '':
            #             check(basic_csv,'0',id_0,questionToday_list)
            #             sure = leitner(questionToday_list) # TODO (sure = or not)
            #             for row in questionToday_list:
            #                 leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
            #     else:
            #         print("you can just continue leitner now")
            #         sure = leitner(questionToday_list) # TODO (sure = or not)
            #         for row in questionToday_list:
            #             leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
            #         # print(questionToday_list)
            #         if len(questionToday_list) == 0:
            #             print('len list is zero (0). ')

def Start_Leitner():
    Run_Leitner_btn.configure(state="disabled")
    Exit_Leitner_btn.configure(state="normal")
    global enable_click
    enable_click = True
    # Flash_card_label.configure(text="en")
    Question_label.configure(text="click the flash card!")
    number_new_word_input.configure(state="disabled")
    number_new_word_btn.configure(state="disabled")
    Run_Leitner()

Leitner_frame.grid_rowconfigure(0, weight=1)  # Start
Leitner_frame.grid_rowconfigure(1, weight=7)  # Flash card
Leitner_frame.grid_rowconfigure(2, weight=1)  # Question
Leitner_frame.grid_rowconfigure(3, weight=2)  # Radio
Leitner_frame.grid_rowconfigure(4, weight=1)  # Apply
Leitner_frame.grid_rowconfigure(5, weight=1)  # Exitّ

Leitner_frame.grid_columnconfigure(0, weight=1)


Run_Leitner_btn = CTkButton(Leitner_frame,
                text="Start Leitner",
                font=en_font,
                command=Start_Leitner)
Run_Leitner_btn.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)


def flash_card_func(event):
    global number_question
    global en_question
    global fr_question
    number_question +=1
    if enable_click == True:    
        if number_question % 2 == 0:
            Flash_card_label.configure(text=en_question)
            Question_label.configure(text="click the flash card!")
        else:
            engine.say(en_question)
            engine.runAndWait()
            Flash_card_label.configure(text=fr_question)
            Question_label.configure(text="your quess is true?")
            True_Rbtn.configure(state="normal")
            False_Rbtn.configure(state="normal")
            check_btn.configure(state="normal")
    

Flash_card_label = CTkLabel(Leitner_frame,
                text="start the Leitner to show the flash card!",
                font=flashcard_fr_font,
                border_color="black",
                border_width=2,
                corner_radius=10)
Flash_card_label.grid(column=0,row=1,sticky='nsew',padx=10,pady=10) # TODO
Flash_card_label.bind("<Button-1>", flash_card_func)

Question_label = CTkLabel(Leitner_frame,
                text="",
                font=en_font,)
Question_label.grid(column=0,row=2,sticky='nsew',padx=10,pady=10) # TODO

Radio_frame = CTkFrame(Leitner_frame,)
Radio_frame.grid(column=0,row=3,sticky='nsew',padx=10,pady=10)
Radio_frame.grid_rowconfigure(0,weight=1)
Radio_frame.grid_columnconfigure([0,1],weight=1)

controller_var = IntVar(value=2)

True_Rbtn = CTkRadioButton(Radio_frame,
                           text="Yes",
                           font=en_font,
                           variable=controller_var,
                           value=1,state="disabled")
True_Rbtn.grid(column=0,row=0,sticky='nsew',padx=10, pady=10)       # TODO                

False_Rbtn = CTkRadioButton(Radio_frame,
                            text="No",
                            font=en_font,
                            variable=controller_var,
                            value=0,state="disabled")
False_Rbtn.grid(column=1,row=0,sticky='nsew',padx=10, pady=10)      # TODO

def check_btn_func():
    global Answer
    global en_question
    global fr_question
    global generator
    global number_question
    if controller_var.get() != 2:
        # text = ""
        if controller_var.get() == 0:
            Answer = "n"
            text = f"[No] I didn't know [{en_question}] meant [{fr_question}]"
        elif controller_var.get() == 1:
            Answer = "y"
            text = f"[Yes] I did know [{en_question}] meant [{fr_question}]"
        lbl = CTkLabel(myframe2,text=text,
                    font=fr_font)
        lbl.grid(sticky='nw', padx=5, pady=2)
        controller_var.set(2)
        # generator = leitner_func()
        number_question = 0
        try:
            s = next(generator)
        except:
            Exit_Leitner_btn.invoke()
        # Flash_card_label.configure(text="en")
        # Question_label.configure(text="click the flash card!")
    else:
        messagebox.showwarning("هشدار","لطفا یک دکمه را انتخاب کنید")

check_btn = CTkButton(Leitner_frame,
                      text="Apply the guess",
                      font=en_font,
                      state="disabled",
                      command=check_btn_func,)
check_btn.grid(column=0,row=4,sticky='nsew',padx=10,pady=10) # TODO

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
    if len(questionToday_list) != 0:
        with open(time_csv) as time_tomorrow:
            reader = csv.reader(time_tomorrow)
            for row in reader:
                tomorrow_year , tomorrow_month , tomorrow_day = int(row[0]) , int(row[1]) , int(row[2])
            e = datetime.datetime.now()
            if e.year > tomorrow_year or (e.year == tomorrow_year and e.month > tomorrow_month) or (e.year == tomorrow_year and e.month == tomorrow_month and e.day >= tomorrow_day):    
                tomorrow = datetime.date.today() + datetime.timedelta(days=1) # TODO
                leitner.edit_time_csv(time_csv,tomorrow.year,tomorrow.month,tomorrow.day)
                for row in questionToday_list:
                    leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])
            else:
                for row in questionToday_list:
                    leitner.edit_csv(basic_csv,row[0],row[1],row[2],row[3],row[4])

Exit_Leitner_btn = CTkButton(Leitner_frame,
                             text="exit Leitner",
                             font=en_font,
                             state="disabled",
                             command=Exit_Leitner)
Exit_Leitner_btn.grid(column=0,row=5,sticky='nsew',padx=10,pady=10)

                                                                                                    # new word

input_new_word.grid_columnconfigure(0, weight=1)

input_new_word.grid_rowconfigure(0, weight=1)
input_new_word.grid_rowconfigure(1, weight=1)
input_new_word.grid_rowconfigure(2, weight=1)

new_word_babel = CTkLabel(input_new_word,
                    text="We have some words already prepared.\n how many would you like to add?",
                    font=en_font)
new_word_babel.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)

def turn_on_numlock(event=None):
    VK_NUMLOCK = 0x90

                        # وضعیت فعلی Num Lock
    if not ctypes.windll.user32.GetKeyState(VK_NUMLOCK) & 1:
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 2, 0)

number_new_word_input = CTkEntry(input_new_word,                          
                      placeholder_text="give me the number: ",
                      font=en_font,justify="center")
number_new_word_input.grid(sticky='nsew',column=0,row=1,pady=10)
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
                                       text=text,
                                       font=en_font,)
        number_new_word_lbl.grid(sticky='nw', padx=5, pady=2)
        number_new_word_input.delete(0,END)
    except:
        messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید")
        number_new_word_input.delete(0,END)


number_new_word_btn = CTkButton(input_new_word,
                         text="add the word",
                         font=en_font,
                         command=get_number_new_word)
number_new_word_btn.grid(column=0,row=2,sticky='nsew',padx=10,pady=10)

                                                                                                    # tab Input Word
tab = my_tabs.tab("Input Word")

tab.grid_columnconfigure(0, weight=1)

tab.grid_rowconfigure(0, weight=1)
tab.grid_rowconfigure(1, weight=1)
tab.grid_rowconfigure(2, weight=1)
tab.grid_rowconfigure(3, weight=8)


def focus_en(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04090409, 0)


en_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="english: ",
                      font=en_font,
                      justify="center",)
en_input.grid(sticky='nsew',column=0,row=0, pady=10)
en_input.bind("<FocusIn>", focus_en)

def focus_fr(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

fr_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text=" :فارسی",
                      font=fr_font,
                      justify="center",)
fr_input.grid(sticky='nsew',column=0,row=1,pady=10)
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
                    font=fr_font,)
        lbl.grid(sticky='nw', padx=5, pady=2)
        en_input.delete(0,END)
        fr_input.delete(0,END)
    else:
        messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

add_word_btn = CTkButton(my_tabs.tab("Input Word"),
                         text="add the word",
                         font=en_font,
                         command=add_the_word)
add_word_btn.grid(column=0,row=2,sticky='nsew',padx=10,pady=10)

                                                                                                    # Tab Status
status_tab = my_tabs.tab("Status")

status_tab.grid_columnconfigure(0, weight=1)
# status_tab.grid_rowconfigure(1, weight=1)

status_labels = []  # بیرون تابع تعریف کن
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
            # text = 'value words [%s] day house is [%i]' % (i, show_list[i])
            text = "[%i] flashcards in the [%s]-day box" % (show_list[i], i)

            lbl = CTkLabel(
                my_tabs.tab("Status"),
                text=text,
                font=en_font,
            )

            lbl.grid(row=row, column=0, sticky='nw', padx=10, pady=2)

            status_labels.append(lbl)
            row += 1


Show_status_btn = CTkButton(
    my_tabs.tab("Status"),
    text="Show status",
    font=en_font,
    command=Show_status
)

Show_status_btn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)



window.after(0, lambda: window.state('zoomed'))
window.mainloop()