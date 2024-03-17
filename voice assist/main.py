import tkinter as tk
from functools import partial
from gtts import gTTS
import os
import playsound
import datetime
import speech_recognition as sr
import random
import requests
from bs4 import BeautifulSoup
import pywhatkit
import wikipedia
import pyjokes
from googletrans import Translator, constants

LANG = "ar"
wikipedia.set_lang(LANG)
translator = Translator()

preReponses = [' .حسنا.', ' .تحت أمرِكْ.', ' .أمركَ مُطاعْ.', ' .أوكي', ' .أنا مشغولةٌ الآنْ. لكنْ سأجيبكْ.', ' .لا أريدُ الإجابةَ على سؤالكْ. لاتقلقْ. فقطْ أمزحُ معكْ.']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
}

def speak(text):
    tts = gTTS(text=text, lang=LANG)
    tts.save("hello.mp3")
    playsound.playsound("hello.mp3", True)
    os.remove("hello.mp3")

listener = sr.Recognizer()

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%A %d/%m/%Y")

def listen(text_box):
    try:
        with sr.Microphone() as source:
            print("انا في الاستماع")
            text_box.insert(tk.END, "Listening...\n")
            text_box.update_idletasks()
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language=LANG)
            text_box.insert(tk.END, f"You said: {command}\n")
            text_box.update_idletasks()
            if 'سعيد' in command:
                print(command)
                return command
            else:
                return ""
    except:
        speak("لم أستطع فهم طلبكم")


def handle_command(command_text):
    i = random.randint(0, 5)
    intro = preReponses[i]
    if 'انهاء' in command_text:
        window.destroy()
    elif 'ساعه' in command_text:
        speak(intro + ".الساعة الان هي ." + get_time())
    elif 'تاريخ' in command_text:
        speak(intro + ".التاريخ الان هو ." + get_date())
    elif 'كيف حالك' in command_text:
        speak(".بخير الحمد لله .")
    elif 'عنوانك' in command_text:
        speak(".أنا أسكن في نواكشوط .")
    elif 'اخبار' in command_text:
        URL = "https://www.hespress.com"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        news = [a.text for a in soup.select('div li a h3')]
        for news_item in news:
            print(news_item)
            speak(news_item)
    elif 'لدي سؤال' in command_text:
        question = command_text.replace('لدي سؤال', '').replace('سعيد', '')
        URL = "https://www.google.co.ma/search?hl="+LANG+"&q=" + question
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = ""
        try:
            result = soup.find(class_='HwtpBd gsrt PZPZlf kTOYnf').get_text()
            speak(result)
        except:
            pass
    elif 'اغنيه' in command_text or 'موسيقى' in command_text or 'سوره' in command_text :
        command_text = command_text.replace('سعيد', '')
        speak(intro + " ها هي " + command_text)
        pywhatkit.playonyt(command_text)
    elif 'كلمني عن' in command_text:
        command_text = command_text.replace('كلمني عن', '').replace('سعيد', '')
        info = wikipedia.summary(command_text, 1)
        speak(info)
    elif 'نكته' in command_text:
        joke = pyjokes.get_joke(language="en", category="neutral")
        print(joke)
        translated_joke = translator.translate(joke, dest=LANG)
        speak(translated_joke.text)


def start_listening(text_box):
    command = listen(text_box)
    if command:
        handle_command(command)


# GUI setup
window = tk.Tk()
window.title("Voice Command Assistant")
window.geometry("900x800")

# Microphone icon
microphone_icon = tk.PhotoImage(file="microphone_icon.png")

text_box = tk.Text(window, height=20, width=100)
text_box.pack(pady=10)

start_button = tk.Button(window, image=microphone_icon, compound="left", command=lambda: start_listening(text_box), bg="white", borderwidth=0, highlightthickness=0)
start_button.pack(pady=20)

exit_button = tk.Button(window, text="Exit", command=window.destroy, bg="red", fg="white", padx=10, pady=5, borderwidth=0, highlightthickness=0)
exit_button.pack(pady=10)

window.mainloop()
