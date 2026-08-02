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
generator = None
number_question = 0
font_size = 15
flashcard_font_size = 15
start_time = 0
