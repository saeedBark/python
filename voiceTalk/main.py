from gtts import gTTS
import os
import playsound

import speech_recognition as sr
import datetime

LANG = "ar"
def speak(text):

   tts = gTTS(text=text ,lang=LANG)
   tts.save("hello.mp3")
   playsound.playsound("hello.mp3",True) 
   os.remove("hello.mp3")


listener = sr.Recognizer()

def get_time():
   return datetime.datetime.now().strftime("%H:%M:%S")

def listen():
  
   try:
     with sr.Microphone() as source: 
      print('انا في حالة الاستماع')
   #   print(get_time())
      voice = listener.listen(source)
      command= listener.recognize_google(voice,language=LANG)
      if 'سعيد': 
        print(command)
        speak(command)
        return command
      else:
         return ""
   except: 
     speak("لم أستطع سماع طلبكم")

def run(): 
    v = True
    while v:
       command = listen()
       if 'انهاء' in command:
             v = False
       elif 'ساعه' in command: 
             speak("الساعة الان " + get_time())
    speak("مع السلامة")   

run()