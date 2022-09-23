# $pip3 install pypiwin32
# $pip3 install pyttsx3
import pyttsx3
engine = pyttsx3.init()
rate=engine.getProperty('rate')
engine.setProperty('rate', rate-40)
volume=engine.getProperty('volume')
engine.setProperty('volume',volume-0.1)
engine.say("How are you")
engine.runAndWait()
