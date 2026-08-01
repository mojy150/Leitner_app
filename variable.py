import pyttsx3
import sqlite3
from tkinter import messagebox,filedialog

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
generator = None
number_question = 0
font_size = 15
flashcard_font_size = 15
start_time = 0
