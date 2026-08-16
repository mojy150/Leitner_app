from variable import *



def focus_en(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04090409, 0)

def focus_next(event):
    event.widget.tk_focusNext().focus()

def focus_fr(event):
    ctypes.windll.user32.ActivateKeyboardLayout(0x04290429, 0)

def turn_on_numlock(event=None):
    VK_NUMLOCK = 0x90

                        # وضعیت فعلی Num Lock
    if not ctypes.windll.user32.GetKeyState(VK_NUMLOCK) & 1:
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0, 2, 0)

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

def max_of_page(count):
    if count%50==0 and count!=0:
        max_count = count/50
    else:
        max_count = 1 + count//50
    return max_count