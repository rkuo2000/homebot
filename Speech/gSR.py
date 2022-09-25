### pip install SpeechRecognition
### python -m pip install pyaudio (for Windows)
### sudo apt install python3-pyaudio (for Ubuntu)

### brew install portaudio (for macOS)
### pip install pyaudio(for macOS)

### Usage  : python gSR.py en
###          python gSR.py zh-TW
###
### (Gitbash)$ winpty gSR.py en

import speech_recognition as sr
import sys

sl = sys.argv[1]
r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.2)
    r.energy_threshold = 4000

    while True:
        keyin = input("talk (y/n)?")
        if keyin=="y":
            print("Listen...")	
            audio = r.listen(source)
            print("Done!\n")
            try:
                # r.recognize_houndify()
                # r.recognize_ibm()
                # r.recognize_sphinx()
                # r.recognize_google()
                # r.recognize_google_cloud()
                text = r.recognize_google(audio, language=sl)
                print("said:", text)
            except sr.UnknownValueError:
                print("say that again!")
            except sr.RequestError as e:
                print("request error; {0}".format(e))
            print("")
        else:
            break
        
