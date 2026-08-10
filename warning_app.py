from variable import *


def edit_app(parent,en_text,fr_text,Table_name):
    edit_app = CTkToplevel(parent)
    edit_app.title("Edit FlashCard")
    edit_app.geometry("300x400")
    edit_app.grab_set()

    edit_app.after(10, edit_app.lift)
    edit_app.after(20, edit_app.focus_force)

    edit_app.grid_columnconfigure(0, weight=1)

    edit_app.grid_rowconfigure(0, weight=1)
    edit_app.grid_rowconfigure(1, weight=1)
    edit_app.grid_rowconfigure(2, weight=0)
    edit_app.grid_rowconfigure(3, weight=1)
    # edit_app.grid_rowconfigure([4,5,6], weight=1)

    en_input = CTkEntry(edit_app,                          
                        placeholder_text="english: ",
                        font=en_font,
                        justify="center",
                        )
    en_input.grid(sticky='nsew',column=0,row=0, pady=10)

    en_input.insert(0, en_text)
    en_input.configure(state="disabled")

    def focus_fr(event):
        ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

    def send_to_add_word_btn(event):
        add_word_btn.invoke()

    fr_input = CTkEntry(edit_app,                          
                        placeholder_text=" :فارسی",
                        font=fr_font,
                        justify="center",)
    fr_input.grid(sticky='nsew',column=0,row=1,pady=10)
    fr_input.bind("<FocusIn>", focus_fr)
    fr_input.bind("<Return>", send_to_add_word_btn)

    fr_input.insert(0, fr_text)

    day_1th_checkbox = CTkCheckBox(edit_app,text="day 1th ?",       
                        onvalue="on",                      
                        offvalue="off",                 
                        font=en_font,                      
                        variable=StringVar(value="off"),
                        )              
    day_1th_checkbox.grid(column=0,row=2,padx=10,pady=10)  

    def add_the_word():
        if en_input.get().strip() != "" and fr_input.get().strip() != "":
            text_en_input= en_input.get().strip()
            text_fr_input= fr_input.get().strip()
            if day_1th_checkbox.get() != "on":
                cursor.execute(f"UPDATE {Table_name} SET answer=? WHERE question=?",
                                    (text_fr_input,
                                    text_en_input
                                    ))
                conn.commit()
            else:
                cursor.execute(f"UPDATE {Table_name} SET answer=?, day=? WHERE question=?",
                                                    (text_fr_input,
                                                    1,
                                                    text_en_input,
                                                    ))
                conn.commit()

            en_input.delete(0,END)
            fr_input.delete(0,END)
            edit_app.destroy()
        else:
            messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

    add_word_btn = CTkButton(edit_app,
                            text="edit your Flashcard",
                            font=en_font,
                            command=add_the_word)
    add_word_btn.grid(column=0,row=3,sticky='nsew',padx=10,pady=10)



def delete_app(parent,en_text,fr_text,Table_name):
    delete_app = CTkToplevel(parent)
    delete_app.title("Delete FlashCard")
    delete_app.geometry("300x400")
    delete_app.grab_set()

    delete_app.after(10, delete_app.lift)
    delete_app.after(20, delete_app.focus_force)

    delete_app.grid_columnconfigure(0, weight=1)

    delete_app.grid_rowconfigure(0, weight=1)
    delete_app.grid_rowconfigure(1, weight=1)
    delete_app.grid_rowconfigure(2, weight=0)
    delete_app.grid_rowconfigure(3, weight=1)
    # delete_app.grid_rowconfigure([4,5,6], weight=1)

    en_input = CTkEntry(delete_app,                          
                        placeholder_text="english: ",
                        font=en_font,
                        justify="center",
                        )
    en_input.grid(sticky='nsew',column=0,row=0, pady=10)

    en_input.insert(0, en_text)
    en_input.configure(state="disabled")

    def focus_fr(event):
        ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

    # def send_to_add_word_btn(event):
        # add_word_btn.invoke()

    fr_input = CTkEntry(delete_app,                          
                        placeholder_text=" :فارسی",
                        font=fr_font,
                        justify="center",)
    fr_input.grid(sticky='nsew',column=0,row=1,pady=10)
    fr_input.bind("<FocusIn>", focus_fr)
    # fr_input.bind("<Return>", send_to_add_word_btn)

    fr_input.insert(0, fr_text)
    fr_input.configure(state="disabled")

    delete_frame_btn = CTkFrame(delete_app)
    delete_frame_btn.grid(column=0,row=3,sticky='nsew',pady=10,padx=2)

    delete_frame_btn.grid_columnconfigure(0, weight=1)
    delete_frame_btn.grid_columnconfigure(1, weight=1)

    delete_frame_btn.grid_rowconfigure(0, weight=1)

    def Delete_FlashCard_func():
        cursor.execute(f"DELETE FROM {Table_name} WHERE question=?",
                       (en_text,))
        delete_app.destroy()

    delete_btn = CTkButton(delete_frame_btn,text="Delete FlashCard",
                    corner_radius=10,
                    fg_color="red",
                    font=CTkFont(family="Arial"),
                    command=Delete_FlashCard_func)
    delete_btn.grid(padx=2,row=0,column=0,sticky='nsew')

    def Edit_FlashCard_func():
        delete_app.destroy()
        edit_app(parent,en_text,fr_text,Table_name)

    edit_btn = CTkButton(delete_frame_btn,text="Edit FlashCard",
                    corner_radius=10,
                    font=CTkFont(family="Arial"),
                    command=Edit_FlashCard_func)
    edit_btn.grid(padx=2,row=0,column=1,sticky='nsew')