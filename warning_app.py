from variable import *

# warning_app = CTk()
# warning_app.title("Warning app")

# def Run_warning_app():
#     warning_app.mainloop()

def warning_app1(parent,en_text,fr_text,Table_name):
    warning_app = CTkToplevel(parent)
    warning_app.title("Warning")
    warning_app.grab_set()

    warning_app.after(10, warning_app.lift)
    warning_app.after(20, warning_app.focus_force)

    warning_app.grid_columnconfigure(0, weight=1)

    warning_app.grid_rowconfigure(0, weight=1)
    warning_app.grid_rowconfigure(1, weight=1)
    warning_app.grid_rowconfigure(2, weight=1)
    warning_app.grid_rowconfigure(3, weight=8)
    warning_app.grid_rowconfigure([4,5,6], weight=1)


    # def focus_en(event):
    #     ctypes.windll.user32.ActivateKeyboardLayout(0x04090409, 0)

    # def focus_next(event):
    #     event.widget.tk_focusNext().focus()

    en_input = CTkEntry(warning_app,                          
                        placeholder_text="english: ",
                        # font=en_font, # TODO
                        justify="center",
                        )
    en_input.grid(sticky='nsew',column=0,row=0, pady=10)
    # en_input.bind("<FocusIn>", focus_en)
    # en_input.bind("<Return>", focus_next)

    en_input.insert(0, en_text)
    en_input.configure(state="disabled")

    def focus_fr(event):
        ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

    def send_to_add_word_btn(event):
        add_word_btn.invoke()

    fr_input = CTkEntry(warning_app,                          
                        placeholder_text=" :فارسی",
                        # font=fr_font, # TODO
                        justify="center",)
    fr_input.grid(sticky='nsew',column=0,row=1,pady=10)
    fr_input.bind("<FocusIn>", focus_fr)
    fr_input.bind("<Return>", send_to_add_word_btn)

    fr_input.insert(0, fr_text)

    def add_the_word():
        if en_input.get().strip() != "" and fr_input.get().strip() != "":
            text_en_input= en_input.get().strip()
            text_fr_input= fr_input.get().strip()
            cursor.execute(f"UPDATE {Table_name} SET answer=? WHERE question=?",
                               (text_fr_input,
                                text_en_input
                                ))
            conn.commit()

            en_input.delete(0,END)
            fr_input.delete(0,END)
            warning_app.destroy()

            # cursor.execute(f"SELECT * FROM {"FlashCards"} WHERE question = ?",(text_en_input,))
            # check_question = cursor.fetchone()
            # if check_question == None:
            #     leitner.append_list_as_row("FlashCards",
            #                             [leitner.last_id("FlashCards") +1,
            #                                 text_en_input,text_fr_input,1,'off'])
            #     new_word +=1
            #     text = '[%i]You add [%s] => [%s]' % (new_word,
            #                                         text_en_input,
            #                                         text_fr_input)
            #     row = myframe2.grid_size()[1]
            #     lbl = CTkLabel(myframe2,
            #                     text=text,
            #                     wraplength=320,
            #                     font=fr_font,
            #                     justify="left",
            #                     anchor="w",
            #                 )
            #     lbl.grid(sticky='ew',column=0,row=row,padx=10, pady=2)

            #     myframe2.update_idletasks()
            #     myframe2._parent_canvas.yview_moveto(1.0)

                # en_input.delete(0,END)
                # fr_input.delete(0,END)
            # else:
            #     messagebox.showwarning("هشدار",f"این فلش کارت در دیتابیس وجود دارد! \n [{check_question[1]}] meant [{check_question[2]}]")

        else:
            messagebox.showwarning("هشدار","لطفا کادرها را پر کنید")

    add_word_btn = CTkButton(warning_app,
                            text="edit your Flashcard",
                            # font=en_font, # TODO
                            command=add_the_word)
    add_word_btn.grid(column=0,row=2,sticky='nsew',padx=10,pady=10)

    # Run_warning_app()