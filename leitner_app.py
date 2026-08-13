import leitner
from variable import *
import warning_app

                                                                                                    # functions
def count_of_Table(Table_name,search_day_temp,search_question_temp,search_answer_temp):
    if search_question_temp != "" and search_answer_temp != "" and search_day_temp != None:
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE day = ? AND question LIKE ? AND answer LIKE ?",
                                (
                                search_day_temp,
                                search_question_temp,
                                search_answer_temp,
                                ))
        count = cursor.fetchone()[0]

    elif search_question_temp != "" and search_answer_temp != "":
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE question LIKE ? AND answer LIKE ?",
                        (
                        search_question_temp,
                        search_answer_temp,
                        ))
        count = cursor.fetchone()[0]


    elif search_question_temp != "" and search_day_temp != None:
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE day = ? AND question LIKE ?",
                                (
                                search_day_temp,
                                search_question_temp,
                                ))
        count = cursor.fetchone()[0]

    elif search_answer_temp != "" and search_day_temp != None:
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE day = ? AND answer LIKE ?",
                                (
                                search_day_temp,
                                search_answer_temp,
                                ))
        count = cursor.fetchone()[0]

    elif search_question_temp != "":
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE question LIKE ?",
                        (
                        search_question_temp,
                        ))
        count = cursor.fetchone()[0]

    elif search_answer_temp != "":
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE answer LIKE ?",
                        (
                        search_answer_temp,
                        ))
        count = cursor.fetchone()[0]

    elif search_day_temp != None:
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name} WHERE day = ?",
                        (
                        search_day_temp,
                        ))
        count = cursor.fetchone()[0]

    else:
        cursor.execute(f"SELECT COUNT(*) FROM {Table_name}")
        count = cursor.fetchone()[0]
    return count

def max_of_page(Table_name,search_day_temp,search_question_temp,search_answer_temp):
    count = count_of_Table(Table_name,search_day_temp,search_question_temp,search_answer_temp)
    if count%50==0 and count!=0:
        max_count = count/50
    else:
        max_count = 1 + count//50
    return max_count
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
my_tabs.add("FlashCards")
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
def show_settings(event=None):
    global num_setting

    if num_setting % 2 == 0:

        x = settings_btn.winfo_x() + settings_btn.winfo_width()

        settings_frame.place(
            x=x,
            y=0,
            relwidth=0.17,
            relheight=1,
            anchor="nw"
        )

        num_setting += 1

    else:
        settings_frame.place_forget()
        num_setting += 1
        save_setting_func()

settings_btn = CTkButton(
    window,
    text="Settings",
    font=en_font,
    width=0,
    command=show_settings
)
settings_btn.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)
window.bind("<Escape>", show_settings)

                                                                                                    # setting Theme
def theme_func():
    global Theme_text
    if theme_switch.get() == "dark":
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
                        onvalue="dark",
                        offvalue="light",
                        variable=StringVar(value="on"),
                        command=theme_func)
theme_switch.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="ew"
)
                                                                                                    # setting read data
def read_setting():
    global font_size
    global flashcard_font_size
    cursor.execute("SELECT * FROM Setting")
    setting_data = cursor.fetchall()
    for row in setting_data:
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
    cursor.execute(f"UPDATE Setting SET Data = ? WHERE Title = ?",(theme_switch.get(),"theme"))
    cursor.execute(f"UPDATE Setting SET Data = ? WHERE Title = ?",(font_size,"font_size"))
    cursor.execute(f"UPDATE Setting SET Data = ? WHERE Title = ?",(flashcard_font_size,"font_size_flashcard"))
    conn.commit()

                                                                                                    # setting font size
font_size_label = CTkLabel(settings_frame,
                           text = "font size",
                           font=CTkFont(size=15)
                        #    font=en_font,      #TODO
                           )
font_size_label.grid(row=1,column=0,padx=5,sticky="ew")

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
font_size_slider.grid(row=2,column=0,padx=10,pady=10,sticky="ew")
                                                                                                    # setting flashcard font size
flashcard_font_size_label = CTkLabel(settings_frame,
                           text = "flashcard font size",
                           font=CTkFont(size=18)
                        #    font=en_font,      #TODO
                           )
flashcard_font_size_label.grid(row=3,column=0,padx=5,sticky="ew")

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
flashcard_font_size_slider.grid(row=4,column=0,padx=10,pady=10,sticky="ew")

settings_save_btn = CTkButton(
    settings_frame,
    text="Save Setting",
    font=en_font,
    height=50,
    command=save_setting_func,
)
settings_save_btn.grid(padx=10,pady=10,sticky="sew")

                                                                                                    # tutorial
cursor.execute("SELECT * FROM Tutorial")
Tutorial_data = cursor.fetchall()
for row in Tutorial_data:
    if row[0] == "don't understand":
        tutorial_frame = CTkFrame(
                            window,
                            fg_color="#2B2B2B"
                        )
        tutorial_frame.place(
                    relx=0,
                    rely=0,
                    relwidth=1,
                    relheight=1,
                    # anchor="nw"
                )

        tutorial_frame.grid_columnconfigure([0],weight=1)
        tutorial_frame.grid_columnconfigure([1],weight=6)
        tutorial_frame.grid_columnconfigure([2],weight=1)
        tutorial_frame.grid_rowconfigure([0],weight=6)

        i = 1

        def left_side_func():
            global i
            if i>1:
                i-=1
                tutorial_label.configure(image=CTkImage(Image.open(f"./media/{i}.webp"),size=(960,540)))

        left_side_btn = CTkButton(tutorial_frame,
                                image=left_side_icon,
                                text="",
                                command=left_side_func)
        left_side_btn.grid(column=0,row=0,padx=10,pady=10)


        tutorial_label = CTkLabel(tutorial_frame,
                                text="",
                                image=CTkImage(Image.open(f"./media/{i}.webp"),size=(960,540)))
        tutorial_label.grid(column=1,row=0,padx=10,pady=10,)


        def right_side_func():
            global i
            if i<8:
                i+=1
                tutorial_label.configure(image=CTkImage(Image.open(f"./media/{i}.webp"),size=(960,540)))


        right_side_btn = CTkButton(tutorial_frame,
                                image=right_side_icon,
                                text="",
                                command=right_side_func)
        right_side_btn.grid(column=2,row=0,padx=10,pady=10)

        def close_tutorial():
            tutorial_frame.place_forget()
            cursor.execute(f"UPDATE Tutorial SET Understand = ?",("understand",))
            conn.commit()

        tutorial_btn = CTkButton(
            tutorial_frame,
            text="I'm understand",
            font=en_font,
            command=close_tutorial
        )
        tutorial_btn.grid(column=1,row=1,padx=10,pady=10,sticky="s")

                                                                                                    # tab Leitner

def leitner_func(): # question words
    global en_question
    global fr_question
    global Answer
    global questionToday_list
    global list_another
    global temp_list
    temp_list = questionToday_list.copy()
    for item in temp_list:
        if item[4] == 'on':
            en_question = item[1]
            Flash_card_label.configure(text=en_question)
            Question_label.configure(text="click the flash card!")
            fr_question = item[2]
            yield item
            if Answer == 'n' or Answer == 'N':
                leitner.edit_database("FlashCards",item[0],item[1],item[2],1,"off")
                # item[3] , item[4] = 1 , 'off'
                questionToday_list.remove(item)
                Answer = ""
            elif Answer == 'y' or Answer == 'Y':
                # item[3] , item[4] = (item[3] + 1) , 'off'
                leitner.edit_database("FlashCards",item[0],item[1],item[2],(item[3] + 1),"off")
                questionToday_list.remove(item)
                Answer = ""

def Run_Leitner():
    global generator
    global questionToday_list
    global list_another
    global number_question
    id_0 = list() # list Ids in database
    questionToday_list = list() # list word of question day
    list_another = list() # list word of does't question day
    questionToday_list = []

    cursor.execute("""
        SELECT * FROM Time
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cursor.fetchone()

    tomorrow_year , tomorrow_month , tomorrow_day = int(row[1]) , int(row[2]) , int(row[3])
    e = datetime.datetime.now()

    if e.year > tomorrow_year or (e.year == tomorrow_year and e.month > tomorrow_month) or (e.year == tomorrow_year and e.month == tomorrow_month and e.day >= tomorrow_day):
        leitner.check("FlashCards",30,id_0,questionToday_list,list_another)
        leitner.check("FlashCards",15,id_0,questionToday_list,list_another)
        leitner.check("FlashCards",7,id_0,questionToday_list,list_another)
        leitner.check("FlashCards",3,id_0,questionToday_list,list_another)
        leitner.check("FlashCards",1,id_0,questionToday_list,list_another)
        leitner.check("FlashCards",'another',id_0,list_another,list_another)
        try:
            generator = leitner_func()
            sure = next(generator)
        except:
            if len(questionToday_list) == 0:
                messagebox.showwarning("توجه","لایتنر خالیست،\n اما اگر شما بخواید میتوانید فلش کارت های جدید اضافه کنید\n یا از فلش کارت هایی که برایتان اماده کرده ایم استفاده کنید.")
                Exit_Leitner_btn.invoke()

    else:
        number_question = 0
        questionToday_list = []
        leitner.check_again("FlashCards",30,questionToday_list)
        leitner.check_again("FlashCards",15,questionToday_list)
        leitner.check_again("FlashCards",7,questionToday_list)
        leitner.check_again("FlashCards",3,questionToday_list)
        leitner.check_again("FlashCards",1,questionToday_list)
        leitner.check_again("FlashCards",0,questionToday_list)
        try:
            generator = leitner_func()
            sure = next(generator)
        except:
            if len(questionToday_list) == 0:
                messagebox.showwarning("توجه","لایتنر خالیست،\n اما اگر شما بخواید میتوانید فلش کارت های جدید اضافه کنید\n یا از فلش کارت هایی که برایتان اماده کرده ایم استفاده کنید.")
                Exit_Leitner_btn.invoke()

def Start_Leitner():
    global start_time
    global enable_click
    enable_click = True
    start_time = time.perf_counter()
    Run_Leitner_btn.configure(state="disabled")
    Exit_Leitner_btn.configure(state="normal")
    Question_label.configure(text="click the flash card!")
    number_new_word_input.configure(state="disabled")
    number_new_word_btn.configure(state="disabled")
    Run_Leitner()

Leitner_frame.grid_rowconfigure(0, weight=1)  # Start
Leitner_frame.grid_rowconfigure(1, weight=7)  # Flash card
Leitner_frame.grid_rowconfigure(2, weight=1)  # Question
Leitner_frame.grid_rowconfigure(3, weight=2)  # Radio
Leitner_frame.grid_rowconfigure(4, weight=1)  # Apply
Leitner_frame.grid_rowconfigure(5, weight=1)  # Exit

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
                width=330,
                wraplength=330,
                border_width=2,
                corner_radius=10)
Flash_card_label.grid(column=0,row=1,sticky='nsew',padx=10,pady=10) # TODO
Flash_card_label.bind("<Button-1>", flash_card_func)
window.bind("<space>", flash_card_func)

Question_label = CTkLabel(Leitner_frame,
                text="",
                font=en_font,)
Question_label.grid(column=0,row=2,sticky='nsew',padx=10,pady=10) # TODO

Radio_frame = CTkFrame(Leitner_frame,)
Radio_frame.grid(column=0,row=3,sticky='nsew',padx=10,pady=10)
Radio_frame.grid_rowconfigure(0,weight=1)
Radio_frame.grid_columnconfigure([0,1],weight=1)

controller_var = IntVar(value=2)

def selected_guess(event):
    if enable_click == True: 
        check_btn.invoke()

def select_True_guess(event):
    if enable_click == True: 
        True_Rbtn.select()

True_Rbtn = CTkRadioButton(Radio_frame,
                           text="Yes",
                           font=en_font,
                           variable=controller_var,
                           value=1,state="disabled")
True_Rbtn.grid(column=0,row=0,sticky='nsew',padx=10, pady=10)       # TODO                
True_Rbtn.bind("<Double 1>", selected_guess)
window.bind("<Left>", select_True_guess)

def select_False_guess(event):
    if enable_click == True: 
        False_Rbtn.select()

False_Rbtn = CTkRadioButton(Radio_frame,
                            text="No",
                            font=en_font,
                            variable=controller_var,
                            value=0,state="disabled")
False_Rbtn.grid(column=1,row=0,sticky='nsew',padx=10, pady=10)      # TODO
False_Rbtn.bind("<Double 1>", selected_guess)
window.bind("<Right>", select_False_guess)

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
        row = myframe2.grid_size()[1]
        lbl = CTkLabel(myframe2,
                        text=text,
                        wraplength=320,
                        font=fr_font,
                        justify="left",
                        anchor="w",
                    )
        lbl.grid(row=row,column=0,sticky='ew',padx=10, pady=2)

        myframe2.update_idletasks()
        myframe2._parent_canvas.yview_moveto(1.0)

        controller_var.set(2)
        number_question = 0
        try:
            s = next(generator)
        except:
            Exit_Leitner_btn.invoke()
    else:
        messagebox.showwarning("هشدار","لطفا یک دکمه را انتخاب کنید")

check_btn = CTkButton(Leitner_frame,
                      text="Apply the guess",
                      font=en_font,
                      state="disabled",
                      command=check_btn_func,)
check_btn.grid(column=0,row=4,sticky='nsew',padx=10,pady=10) # TODO

def Exit_Leitner():
    global enable_click
    global start_time
    global Answer
    global temp_list
    Answer = "s"
    Run_Leitner_btn.configure(state="normal")
    Exit_Leitner_btn.configure(state="disabled")
    enable_click = False
    Flash_card_label.configure(text="start the Leitner to show the flash card!")
    Question_label.configure(text="")
    controller_var.set(2)
    False_Rbtn.configure(state="disabled",variable=controller_var)
    True_Rbtn.configure(state="disabled",variable=controller_var)
    number_new_word_input.configure(state="normal")
    number_new_word_btn.configure(state="normal")
    check_btn.configure(state="disabled")
    
    if len(temp_list) !=0:
        cursor.execute("""
            SELECT * FROM Time
            ORDER BY id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()

        tomorrow_year , tomorrow_month , tomorrow_day = int(row[1]) , int(row[2]) , int(row[3])
        e = datetime.datetime.now()
        if e.year > tomorrow_year or (e.year == tomorrow_year and e.month > tomorrow_month) or (e.year == tomorrow_year and e.month == tomorrow_month and e.day >= tomorrow_day):    
            for row in list_another:
                if (row[0] == 1 or row[0] == 3 or row[0] == 7 or row[0] == 15 or row[0] == 30) and row[4] == 'off':
                    leitner.edit_database("FlashCards",row[0],row[1],row[2],row[3],'on')
                    
                elif row[0] != 0 and row[0] != 1 and row[0] != 3 and row[0] != 7 and row[0] != 15 and row[0] != 30:
                # TODO elif or else
                    leitner.edit_database("FlashCards",row[0],row[1],row[2],(row[3] +1),row[4]) # TODO (row[4] or 'off')
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)

            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                cursor.execute(f"""
                                INSERT INTO {"Time"} VALUES (?, ?,?,?,?)
                                """,
                                (
                                    (leitner.last_id("Time") +1),
                                    tomorrow.year,
                                    tomorrow.month,
                                    tomorrow.day,
                                    elapsed
                                ))
                conn.commit()
            for row in questionToday_list:
                leitner.edit_database("FlashCards",row[0],row[1],row[2],row[3],row[4])
        else:
            if start_time is not None:
                New_elapsed = time.perf_counter() - start_time
            cursor.execute(f"SELECT Time_spent FROM {"Time"} WHERE id = {leitner.last_id("Time")}")
            elapsed = cursor.fetchone()[0]
            elapsed = elapsed + New_elapsed
            cursor.execute(f"UPDATE {"Time"} SET Time_spent = ? WHERE id = ?",
                           (elapsed,
                            leitner.last_id("Time")
                            ))
            conn.commit()
            for row in questionToday_list:
                leitner.edit_database("FlashCards",row[0],row[1],row[2],row[3],row[4])

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

def send_number_new_word_btn(event):
    number_new_word_btn.invoke()

number_new_word_input = CTkEntry(input_new_word,                          
                      placeholder_text="give me the number: ",
                      font=en_font,justify="center")
number_new_word_input.grid(sticky='nsew',column=0,row=1,pady=10)
number_new_word_input.bind("<FocusIn>", turn_on_numlock)
number_new_word_input.bind("<Return>", send_number_new_word_btn)


def get_number_new_word():
    try:
        global Table_name
        number_new_word = number_new_word_input.get().strip()
        number_new_word = int(number_new_word)
        text = (f"[{number_new_word}] new word added to your Leitner")
        id_0 = []
        selected_new_word = []
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day = 0")
        Day_Zero_data = cursor.fetchall()
        counter = int(0)

        for row in Day_Zero_data:
            if row[3] == 0:
                id_0.append([row[0],row[1],row[2],1,'off'])
                counter +=1

        if counter != 0:
            if number_new_word > len(id_0):
                number_new_word = len(id_0)
                text = ('all new words in database is [%i] and added to your Leitner' % (number_new_word))

        selected_new_word = leitner.my_append(id_0,selected_new_word,number_new_word)
        selected_new_word.sort(key=lambda x: int(x[0]))

        for temp_list in selected_new_word:
            cursor.execute(f"UPDATE {Table_name} SET question=?,answer=?,day=?,on_off=? WHERE id = ?",
                           (temp_list[1],
                            temp_list[2],
                            temp_list[3],
                            temp_list[4],
                            temp_list[0])
                            )
            conn.commit()

        row = myframe2.grid_size()[1]
        number_new_word_lbl = CTkLabel(myframe2,
                                        text=text,
                                        wraplength=320,
                                        font=en_font,
                                        justify="left",
                                        anchor="w",
                                       )
        number_new_word_lbl.grid(sticky='ew',column=0,row=row,padx=10, pady=2)
        number_new_word_input.delete(0,END)

        myframe2.update_idletasks()
        myframe2._parent_canvas.yview_moveto(1.0)
        

    except:
        messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید") # TODO
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
tab.grid_rowconfigure([4,5,6], weight=1)


def focus_en(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04090409, 0)

def focus_next(event):
    event.widget.tk_focusNext().focus()

en_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="english: ",
                      font=en_font,
                      justify="center",)
en_input.grid(sticky='nsew',column=0,row=0, pady=10)
en_input.bind("<FocusIn>", focus_en)
en_input.bind("<Return>", focus_next)

def focus_fr(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

def send_to_add_word_btn(event):
    add_word_btn.invoke()

fr_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text=" :فارسی",
                      font=fr_font,
                      justify="center",)
fr_input.grid(sticky='nsew',column=0,row=1,pady=10)
fr_input.bind("<FocusIn>", focus_fr)
fr_input.bind("<Return>", send_to_add_word_btn)


new_word = int(0)
def add_the_word():
    global new_word
    if en_input.get().strip() != "" and fr_input.get().strip() != "":
        text_en_input= en_input.get().strip()
        text_fr_input= fr_input.get().strip()
        cursor.execute(f"SELECT * FROM {"FlashCards"} WHERE question = ?",(text_en_input,))
        check_question = cursor.fetchone()
        if check_question == None:
            leitner.append_list_as_row("FlashCards",
                                    [leitner.last_id("FlashCards") +1,
                                        text_en_input,text_fr_input,1,'off'])
            new_word +=1
            text = '[%i]You add [%s] => [%s]' % (new_word,
                                                text_en_input,
                                                text_fr_input)
            row = myframe2.grid_size()[1]
            lbl = CTkLabel(myframe2,
                            text=text,
                            wraplength=320,
                            font=fr_font,
                            justify="left",
                            anchor="w",
                        )
            lbl.grid(sticky='ew',column=0,row=row,padx=10, pady=2)

            myframe2.update_idletasks()
            myframe2._parent_canvas.yview_moveto(1.0)

            en_input.delete(0,END)
            fr_input.delete(0,END)
        else:
            warning_app.edit_app(window,check_question[1],check_question[2],"FlashCards")
            en_input.delete(0,END)
            fr_input.delete(0,END)
            # messagebox.showwarning("هشدار",f"این فلش کارت در دیتابیس وجود دارد! \n [{check_question[1]}] meant [{check_question[2]}]")

    else:
        messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

add_word_btn = CTkButton(my_tabs.tab("Input Word"),
                         text="add the word",
                         font=en_font,
                         command=add_the_word)
add_word_btn.grid(column=0,row=2,sticky='nsew',padx=10,pady=10)

# def focus_next(event):
#     event.widget.tk_focusNext().focus()

Question_column_number_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="Question column number(2):",
                      font=en_font,
                      justify="center",)

Question_column_number_input.grid(column=0,row=4,sticky='nsew', pady=10)
Question_column_number_input.bind("<FocusIn>", turn_on_numlock)
Question_column_number_input.bind("<Return>", focus_next)

def send_to_add_file_btn(event):
    add_file_to_database_btn.invoke()

Answer_column_number_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="Answer column number(3):",
                      font=fr_font,
                      justify="center",)

Answer_column_number_input.grid(column=0,row=5,sticky='nsew',pady=10)
Answer_column_number_input.bind("<FocusIn>", turn_on_numlock)
Answer_column_number_input.bind("<Return>", send_to_add_file_btn)

def add_file_to_database():
        global new_word
        if Question_column_number_input.get().strip() != "" and Answer_column_number_input.get().strip() != "":
            Question_column_number= Question_column_number_input.get().strip()
            Answer_column_number= Answer_column_number_input.get().strip()
            file_csv = filedialog.askopenfilename(
                                                    title="Choose your CSV",
                                                    filetypes=[("CSV files", "*.csv")]
                                                )
            if file_csv != "":
                try:
                    Table_name = "FlashCards" # TODO
                    # cursor.execute(f"""CREATE TABLE IF NOT EXISTS {Table_name}(
                    # Title TEXT,
                    # Data TEXT
                    # )""")
                    # conn.commit() # TODO
                    with open(file_csv, "r", encoding="utf-8") as file:
                        reader = csv.reader(file)
                        try:
                            for row in reader:
                                                                                                                                      # TODO 👇  👇
                                row = [leitner.last_id(Table_name) +1,
                                       row[int(Question_column_number)-1],
                                       row[int(Answer_column_number)-1],
                                       row[3],
                                       row[4]] 
                                leitner.append_list_as_row(Table_name,row)

                            conn.commit()

                        except:
                            for row in reader:
                                                                                                                                  # TODO 👇  👇
                                row = [leitner.last_id(Table_name) +1,
                                       row[int(Question_column_number)-1],
                                       row[int(Answer_column_number)-1]
                                       ,0
                                       ,"off"] 
                                leitner.append_list_as_row(Table_name,row)

                            conn.commit()
                except:
                    messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید")
            Question_column_number_input.delete(0,END)
            Answer_column_number_input.delete(0,END)
        else:
            messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

    

add_file_to_database_btn = CTkButton(my_tabs.tab("Input Word"),
                         text="Add your CSV file",
                         font=en_font,
                         command=add_file_to_database)

add_file_to_database_btn.grid(column=0,row=6,sticky='nsew',padx=10,pady=10)

                                                                                                    # Tab Status
my_tabs.tab("Status").grid_columnconfigure(0, weight=1)
my_tabs.tab("Status").grid_rowconfigure(0, weight=1)

status_tab = CTkScrollableFrame(my_tabs.tab("Status"))
status_tab.grid(row=0, column=0,sticky='nsew')

status_tab.grid_columnconfigure(0, weight=1)

status_labels = []  # بیرون تابع تعریف کن
def Show_status():
    global status_labels
    cursor.execute(f"SELECT * FROM {"Time"} WHERE id = {leitner.last_id("Time")}")
    Last_day = cursor.fetchone()
    Day_th , Time_spent = Last_day[0],Last_day[4]
    status_today = f"Today is the {Day_th-1}th day and your time spent is {int(Time_spent)//60}:{int(Time_spent)%60:02d}."

    lbl = CTkLabel(
        status_tab,
        text=status_today,
        font=en_font,
    )

    lbl.grid(row=1, column=0, sticky='nw', padx=10, pady=2)

    # حذف لیبل‌های قبلی
    for lbl in status_labels:
        lbl.destroy()

    status_labels.clear()

    show_list = leitner.show("FlashCards")

    row = 2
    for i in range(len(show_list)):
        if show_list[i] != 0:
            text = "[%i] flashcards in the [%s]-day box" % (show_list[i], i)

            lbl = CTkLabel(
                status_tab,
                text=text,
                font=en_font,
            )

            lbl.grid(row=row, column=0, sticky='nw', padx=10, pady=2)
            status_labels.append(lbl)
            row += 1


Show_status_btn = CTkButton(
    status_tab,
    text="Show status",
    font=en_font,
    command=Show_status
)

Show_status_btn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

                                                                                                    # Tab FlashCards
my_tabs.tab("FlashCards").grid_columnconfigure(0, weight=1)
my_tabs.tab("FlashCards").grid_rowconfigure([0,1], weight=0)
my_tabs.tab("FlashCards").grid_rowconfigure(2, weight=8)
my_tabs.tab("FlashCards").grid_rowconfigure(3, weight=0)

FlashCards_tab = CTkScrollableFrame(my_tabs.tab("FlashCards"),
                                    border_width=2,
                                    )
FlashCards_tab.grid(row=2, column=0,sticky='nsew')

FlashCards_tab.grid_columnconfigure([0,1,2,3,4], weight=1)

FlashCards_labels = []

def Show_FlashCards(Table_name):
    global FlashCards_page
    global search_day_temp
    global search_question_temp
    global search_answer_input
    search_day_temp = None
    search_question_temp = ""
    search_answer_temp = ""

    try:
        page_number_temp = int(page_number_input.get())
        search_question_temp = search_question_input.get().strip()
        search_answer_temp = search_answer_input.get().strip()
        try:
            if search_day_input.get() != "":
                search_day_temp = int(search_day_input.get())
        except:
            messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید")
            search_day_input.delete(0,"end")

        if page_number_temp >= 1 and page_number_temp <= max_of_page(Table_name,search_day_temp,search_question_temp,search_answer_temp):
            FlashCards_page = page_number_temp
        elif page_number_temp > max_of_page(Table_name,search_day_temp,search_question_temp,search_answer_temp):
            FlashCards_page = max_of_page(Table_name,search_day_temp,search_question_temp,search_answer_temp)
        else:
            FlashCards_page = 1
        page_number_input.delete(0,"end")
        page_number_input.insert(0,FlashCards_page)
    except:
        messagebox.showwarning("هشدار","لطفا عدد صحیح وارد کنید")
        page_number_input.delete(0,"end")
        page_number_input.insert(0,FlashCards_page)

    if search_question_temp != "" and search_day_temp != None and search_answer_temp != "":
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day = ? AND question LIKE ? AND answer LIKE ? LIMIT 50 OFFSET ?",
                                (
                                search_day_temp,
                                "%"+search_question_temp+"%",
                                "%"+search_answer_temp+"%",
                                50*(FlashCards_page-1),
                                ))
        FlashCards_data = cursor.fetchall()

    elif search_question_temp != "" and search_day_temp != None:
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day = ? AND question LIKE ? LIMIT 50 OFFSET ?",
                                (
                                search_day_temp,
                                "%"+search_question_temp+"%",
                                50*(FlashCards_page-1),
                                ))
        FlashCards_data = cursor.fetchall()

    elif search_answer_temp != "" and search_day_temp != None:
        cursor.execute(f"SELECT * FROM {Table_name} WHERE day = ? AND answer LIKE ? LIMIT 50 OFFSET ?",
                                (
                                search_day_temp,
                                "%"+search_answer_temp+"%",
                                50*(FlashCards_page-1),
                                ))
        FlashCards_data = cursor.fetchall()

    elif search_question_temp != "" and search_answer_temp != "":
        cursor.execute(f"SELECT * FROM {Table_name} WHERE answer LIKE ? AND question LIKE ? LIMIT 50 OFFSET ?",
                                (
                                "%"+search_answer_temp+"%",
                                "%"+search_question_temp+"%",
                                50*(FlashCards_page-1),
                                ))
        FlashCards_data = cursor.fetchall()

    elif search_question_temp != "":
        cursor.execute(f"SELECT * FROM {Table_name} WHERE question LIKE ? LIMIT 50 OFFSET ?",
                        (
                        "%"+search_question_temp+"%",
                        50*(FlashCards_page-1),
                        ))
        FlashCards_data = cursor.fetchall()

    elif search_answer_temp != "":
        cursor.execute(f"SELECT * FROM {Table_name} WHERE answer LIKE ? LIMIT 50 OFFSET ?",
                        (
                        "%"+search_answer_temp+"%",
                        50*(FlashCards_page-1),
                        ))
        FlashCards_data = cursor.fetchall()

    elif search_day_temp != None:
        cursor.execute(f"SELECT * FROM {Table_name} WHERE Day = ? LIMIT 50 OFFSET ?",
                        (search_day_temp,
                        50*(FlashCards_page-1), # TODO
                        ))
        FlashCards_data = cursor.fetchall()

    else:
        cursor.execute(f"SELECT * FROM {Table_name} LIMIT 50 OFFSET ?",
                        (50*(FlashCards_page-1), # TODO
                        ))
        FlashCards_data = cursor.fetchall()

    for row, data in enumerate(FlashCards_data):

        # اگر این ردیف قبلاً ساخته نشده باشد
        if row >= len(FlashCards_labels):

            row_labels = []

            for col in range(5):
                lbl = CTkLabel(
                    FlashCards_tab,
                    text="",
                    wraplength=200,
                    font=fr_font,
                )

                lbl.grid(row=row, column=col, sticky="nw", padx=10, pady=2)
                row_labels.append(lbl)

                                                                                                    # Edit FlashCards
            def edit_Flashcard(row):
                for widget in FlashCards_tab.winfo_children():
                    info = widget.grid_info()

                    if info.get("row") == row :
                        if info.get("column") == 1:
                            en_text = widget.cget("text")
                        if info.get("column") == 2:
                            fr_text = widget.cget("text")

                warning_app.edit_app(window,en_text,fr_text,Table_name)
                

            edit_btn = CTkButton(
                FlashCards_tab,
                text="",
                fg_color="transparent",
                image=edit_icon,
                width=24,
                height=24,
                command=lambda r=row: edit_Flashcard(r),
            )

            edit_btn.grid(row=row, column=6,)
            row_labels.append(edit_btn)

                                                                                                    # Delete FlashCard
            def delete_Flashcard(row):
                for widget in FlashCards_tab.winfo_children():
                    info = widget.grid_info()

                    if info.get("row") == row :
                        if info.get("column") == 1:
                            en_text = widget.cget("text")
                        if info.get("column") == 2:
                            fr_text = widget.cget("text")
                            
                warning_app.delete_app(window,en_text,fr_text,Table_name)

            delete_btn = CTkButton(
                FlashCards_tab,
                text="",
                fg_color="transparent",
                image=delete_icon,
                width=24,
                height=24,
                command=lambda r=row: delete_Flashcard(r),
            )

            delete_btn.grid(row=row, column=7,)
            row_labels.append(delete_btn)
            FlashCards_labels.append(row_labels)

        else:
            # ردیف قبلاً ساخته شده ولی ممکن است مخفی شده باشد
            for widget in FlashCards_labels[row]:
                widget.grid()

        # فقط متن لیبل‌ها را عوض کن
        for col in range(5):
            FlashCards_labels[row][col].configure(text=str(data[col]))

    # اگر این بار تعداد رکوردها کمتر شده بود، لیبل‌های اضافی را مخفی کن
    for row in range(len(FlashCards_data), len(FlashCards_labels)):
        for lbl in FlashCards_labels[row]:
            lbl.grid_remove()


Show_FlashCards_btn = CTkButton(
    my_tabs.tab("FlashCards"),
    text="Show FlashCards",
    font=en_font,
    command=lambda: Show_FlashCards("FlashCards")
)

Show_FlashCards_btn.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

                                                                                                    # Search FlashCard
def update_page(event):
    Show_FlashCards_btn.invoke()

search_frame = CTkFrame(my_tabs.tab("FlashCards"))
search_frame.grid(column=0,row=1,sticky='nsew')

search_frame.grid_columnconfigure([0,1,2], weight=1)
search_frame.grid_rowconfigure(0, weight=1)

search_question_input = CTkEntry(search_frame,
                    placeholder_text="your question: ",
                    font=en_font,
                    justify="center",
                    )
search_question_input.grid(sticky='nsew',column=0,row=0, pady=5)
search_question_input.bind("<Return>", update_page)
search_question_input.bind("<FocusIn>", focus_en)

search_answer_input = CTkEntry(search_frame,
                    placeholder_text="your answer: ",
                    font=fr_font,
                    justify="center",
                    )
search_answer_input.grid(sticky='nsew',column=1,row=0, pady=5)
search_answer_input.bind("<Return>", update_page)
search_answer_input.bind("<FocusIn>", focus_fr)

search_day_input = CTkEntry(search_frame,
                    placeholder_text="day number: ",
                    font=en_font,
                    justify="center",
                    )
search_day_input.grid(sticky='nsew',column=2,row=0, pady=5)
search_day_input.bind("<Return>", update_page)
                                                                                                    # Right_Left_frame FlashCards
Right_Left_frame = CTkFrame(my_tabs.tab("FlashCards"),height=0)
Right_Left_frame.grid(column=0,row=3)

def left_page_func():
    global FlashCards_page
    if FlashCards_page>1:
        FlashCards_page-=1
        page_number_input.delete(0, "end")
        page_number_input.insert(0,FlashCards_page)
    Show_FlashCards_btn.invoke()

left_side_btn = CTkButton(Right_Left_frame,
                        image= left_side_icon,
                        text="",
                        command=left_page_func)
left_side_btn.grid(column=0,row=0,padx=10,pady=10)

page_number_input = CTkEntry(Right_Left_frame,                          
                      placeholder_text="page number: ",
                      font=en_font,
                      justify="center",)

page_number_input.grid(column=1,row=0,sticky="ns",padx=10,pady=10)
page_number_input.bind("<Return>", update_page)

page_number_input.insert(0,FlashCards_page)

def right_page_func():
    global FlashCards_page
    max_page = max_of_page(Table_name,search_day_temp,search_question_temp,search_answer_temp)

    if FlashCards_page<max_page:
        FlashCards_page+=1
        page_number_input.delete(0, "end")
        page_number_input.insert(0,FlashCards_page)

    Show_FlashCards_btn.invoke()


right_side_btn = CTkButton(Right_Left_frame,
                        image=right_side_icon,
                        text="",
                        command=right_page_func)
right_side_btn.grid(column=2,row=0,padx=10,pady=10)




                                                                                                    # End app
window.after(0, lambda: window.state('zoomed'))
window.mainloop()