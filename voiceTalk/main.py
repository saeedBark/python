import  pyttsx3
import  speech_recognition as sr
import  webbrowser
import  time
import  datetime
import  os
from pydub import AudioSegment
from  pydub.playback import  play
import pyautogui


wel = pyttsx3.init()
voices = wel.getProperty('voices')
wel.setProperty('voice',voices[0].id)


def Speak(audio): 
    wel.say(audio)
    wel.runAndWait()

def TakeCommands(): 
    command = sr.Recognizer() 
    with sr.Microphone() as mic:
        print('Say commands sir ......')
        command.phrase_thrshold = 0.4
        audio = command.listen(mic)

        try:
            print('Recording ...')
            query = command.redcognize_google(audio,language='ar')
            print(f'you said :  {query}')
        except Exception as Error:
            return None
        return query.lower()
    


music = AudioSegment.from_mp3('sounds/welcome.mp3')
play(music)


#time.sleep(1)

#music1 =  AudioSegment.from_mp3('sounds/welcome2.mp3')
#play(music1)




