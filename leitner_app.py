from customtkinter import *
import leitner


window = CTk()
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f'{width}x{height}+0+0')


window.grid_columnconfigure([0],weight=3)
window.grid_columnconfigure([1],weight=1)
window.grid_rowconfigure([0],weight=1)

my_tabs = CTkTabview(window,)                                   
my_tabs.add("Leitner")                                 
my_tabs.add("Input Word")
my_tabs.add("Status")
my_tabs.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)

def click_button():
    lbl = CTkLabel(myframe2,text="hi")
    lbl.grid()


btn = CTkButton(my_tabs.tab("Leitner"),
                text="print",
                command=click_button)
btn.grid(column=0,row=0,sticky='nsew',padx=10,pady=10)


lbl2 = CTkLabel(my_tabs.tab("Leitner"),text="Your guess is True?")
lbl2.grid(sticky='nsew',padx=10,pady=10)


controller_var = IntVar(value=2)

True_Rbtn = CTkRadioButton(my_tabs.tab("Leitner"),
                           text="Yes",
                           variable=controller_var,
                           value=1,)
True_Rbtn.grid(sticky='nsew',padx=10,pady=10)                       

False_Rbtn = CTkRadioButton(my_tabs.tab("Leitner"),
                            text="No",
                            variable=controller_var,
                            value=0)
False_Rbtn.grid(sticky='nsew',padx=10,pady=10)

check_btn = CTkButton(my_tabs.tab("Leitner"),text="Apply the guess",)
check_btn.grid(sticky='nsew',padx=10,pady=10)

Exit_Leitner_btn = CTkButton(my_tabs.tab("Leitner"),text="I'm want to exit Leitner",)
Exit_Leitner_btn.grid(sticky='nsew',padx=10,pady=10)

myframe2 = CTkScrollableFrame(window)
myframe2.grid(column=1,row=0,sticky='nsew',padx=10,pady=10)


en_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="انگلیسی: ")   # متنی که تا وقتی ننویسی توش اونجا هست
en_input.grid(pady=10)

fr_input = CTkEntry(my_tabs.tab("Input Word"),                          
                      placeholder_text="فارسی: ")   # متنی که تا وقتی ننویسی توش اونجا هست
fr_input.grid(pady=10)

def add_the_word():
    leitner.append_list_as_row(leitner.basic_csv,[str(leitner.last_id() +1),en_input.get().strip(),fr_input.get().strip(),'1','off'])
    en_input.delete(0,END)
    fr_input.delete(0,END)

add_word_btn = CTkButton(my_tabs.tab("Input Word"),text="add the word",command=add_the_word)
add_word_btn.grid(sticky='nsew',padx=10,pady=10)



# show_status_frame = CTkScrollableFrame(my_tabs.tab("Status"))
# show_status_frame.grid(sticky='nsew',padx=10,pady=10)

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