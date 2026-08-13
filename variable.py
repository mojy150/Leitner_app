import pyttsx3
import sqlite3
from tkinter import messagebox,filedialog
from customtkinter import *
import ctypes
import datetime
from tempfile import NamedTemporaryFile
from PIL import Image
import time
import csv
from random import choice
import webbrowser

                                                                                                    # main
window = CTk()
window.title("Leitner app")
fr_font = CTkFont(family="vazir",size=15)
en_font = CTkFont(family="Arial",size=15)
flashcard_fr_font = CTkFont(family="vazir",size=15)
flashcard_en_font = CTkFont(family="Arial",size=15)

engine = pyttsx3.init()
engine.setProperty('rate', 170)

conn = sqlite3.connect("Leitner_DB.db")
cursor = conn.cursor()
Table_name = "FlashCards"

enable_click = False
en_question = ""
fr_question = ""
Answer = "s"
sure = "null"
questionToday_list = list()
temp_list = questionToday_list.copy()
generator = None
number_question = 0
font_size = 15
flashcard_font_size = 18
start_time = 0
FlashCards_page = 1
search_day_temp = None
search_question_temp = ""
search_answer_temp = ""
max_count = 0

edit_icon = CTkImage(
    Image.open("./media/icon-edit-48x48.png"),
    size=(24,24)
)

delete_icon = CTkImage(
    Image.open("./media/icon-delete-48x48.png"),
    size=(24,24)
)

right_side_icon = CTkImage(
    Image.open(f"./media/right_side.png"),
    size=(70,70)
)

left_side_icon = CTkImage(
    Image.open(f"./media/left_side.png"),
    size=(70,70)
)
