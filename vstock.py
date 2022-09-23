### Usage : python macapi.py en
import speech_recognition as sr 
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import time
import psutil
import pynput
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from alpha_vantage.timeseries import TimeSeries
API_KEY = 'K6LJO3BJMBJMTT1A'

keyboard = KeyboardController()
mouse = MouseController()

os.system("cd ~")
usr_path   = str(os.system("pwd"))
app_path   = usr_path+"/Applications"
download_path = usr_path+"/Downloads"
desktop_path  = usr_path+"/Desktop"
doc_path   = usr_path+"/Documents"
music_path = usr_path+"/Music"
video_path = usr_path+"/Movies"
pic_dir    = usr_path+"/Pictures"

history_points = 50 # for 2 months 
def download_stock(symbol):
	print('downloading...')
	ts = TimeSeries(key=API_KEY, output_format='pandas')
	data, meta_data = ts.get_daily(symbol, outputsize='full')
	data.to_csv(f'./{symbol}_daily.csv')
	data = pd.read_csv(f'./{symbol}_daily.csv')
	data = data.drop('date',axis=1)
	data = data[::-1]
	data = data.reset_index()
	data = data.drop('index', axis=1)
	next_day_open_values = np.array([data.loc[:,"1. open"][i + history_points].copy() for i in range(len(data) - history_points)])
	next_day_open_values = np.expand_dims(next_day_open_values, -1)
	return next_day_open_values
	 
URL = "https://google.com"
sl = sys.argv[1]
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def stop_app(app_exe):
	for process in psutil.process_iter():
		if process.name() == app_exe:
			os.system("kill -9 "+process.pid)
	
with microphone as source:
	recognizer.adjust_for_ambient_noise(source)

	while True:
		print("Speak:")	
		audio = recognizer.listen(source)
		try:
			url=" "
			text = recognizer.recognize_google(audio, language=sl)
			cmd = text.split(" ")
			print("You said:", text)
			if text=='exit':
				print('Bye Bye, see you!')
				break
			if cmd[0]=='download':
				symbol=cmd[1]
				if cmd[1]=='Google': symbol='GOOGL'
				if cmd[1]=='Microsoft': symbol='MSFT'
				stock  = download_stock(symbol)
			if cmd[0]=='plot':
				symbol=cmd[1]
				if cmd[1]=='Google': symbol='GOOGL'
				if cmd[1]=='Microsoft': symbol='MSFT'
				fig=plt.plot(stock[0:-1], label=symbol)
				plt.title(symbol)
				#plt.legend([cmd[1], cmd[2]])
				#fig.savefig(symbol+'.png')
				plt.show(fig)
				plt.pause(3)
			if cmd[0]=='close':
				symbol=cmd[1]
				if cmd[1]=='Google': symbol='GOOGL'
				if cmd[1]=='Microsoft': symbol='MSFT'
				plt.close(symbol)
			if cmd[0]=='open':
				if cmd[1]=='browser' or cmd[1]=='Chrome':
					os.system("sudo open "+URL)
			if cmd[0]=='search' or cmd[0]=='Google':
				if len(cmd)==1:
					url=" "
				else:
					url=" https://google.com/search?q="
					for i in range(1,len(cmd)):
						url += cmd[i]+'+'
				os.system("sudo open "+url[:-1])
			if cmd[0]=='watch' or cmd[0]=='YouTube':
				if len(cmd)==1:
					url=" https://youtube.com "
				else:
					url=" https://youtube.com/search?q="
					for i in range(1,len(cmd)):
						url += cmd[i]+'+'
				os.system("sudo open "+url[:-1])
			if cmd[0]=='scroll':
				if len(cmd)>1:
					if cmd[1]=='up':
						keyboard.press('<cmd>+<up>')
					if cmd[1]=='down':
						keyboard.press('<cmd>+<down>')					
			if cmd[0]=='move':
				if len(cmd)>1:
					if cmd[1]=='up':
						keyboard.press('<up>')
					if cmd[1]=='down':
						keyboard.press('<down>')
			if cmd[0]=='play' or cmd[0]=='click':	
				mouse.click(Button.left,1)
			if cmd[0]=='double' and cmd[1]=='click':
				mouse.click(Button.left,2)
			if cmd[0]=='close' or cmd[0]=='quit':
				if cmd[1]=='Chrome':
					stop_app('chrome.exe')
			if cmd[0]=='input':
				txt = text.replace(cmd[0]+" ","")+"\n"
				keyboard.type(txt)
				input_len=len(txt)
			if cmd[0]=='cancel':
				if cmd[1]=='input':
					stop_app('chrome')
		except sr.UnknownValueError:
			#print("Could not understand audio!")
			print("please say that again")
		except sr.RequestError as e:
			#print("Could not request results; {0}".format(e))
			pritn("please try again")
		print("")
