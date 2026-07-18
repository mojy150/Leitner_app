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
