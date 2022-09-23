### Usage: python gSTT.py en
import speech_recognition as sr
from gtts import gTTS
import requests
import urllib.request
import sys
import os
import random

sl = sys.argv[1]
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def text2speech(text,tl):
    tts=gTTS(text, lang=tl)
    filename='gSTT.mp3'
    tts.save(filename)
    #os.system('mpg321 '+filename)  # PiZero
    #os.system('madplay '+filename) # RPi3
    os.system('cmdmp3 '+filename)  # PC
    #os.system('afplay '+filename)  # MAC
    os.remove(filename)
    
def speech2text():    
    print("Speak:")
    audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language=sl)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio!")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)    
        while True:
            text  = speech2text()
            if text is not None:
                text2speech(text,sl)
            if text=='exit':
                break;
