### Usage : python win7api.py en
import speech_recognition as sr
import cv2
import numpy as np
import os
import sys
import time
import psutil
import pynput
import win32gui
import win32con
import win32api
import win32process
#from win32gui import GetWindowText, GetForegroundWindow

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()

sl = sys.argv[1]
recognizer = sr.Recognizer()
microphone = sr.Microphone()

URL = "https://google.com"
BROWSER = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

os.chdir("..")
usr_path   = str(os.system("pwd"))
desktop_path = usr_path+"/Desktop"
doc_path     = usr_path+"/Documents"
music_path   = doc_path+"/My Music"
video_path   = doc_path+"/My Videos"
picture_path = doc_path+"/My Pictures"

def enumWindowsProc(hwnd, lParam):
    if (lParam is None) or ((lParam is not None) and win32process.GetWindowThreadProcessId(hwnd)[1] == lParam):
        text = win32gui.GetWindowText(hwnd)
        if text:
            win32api.SendMessage(hwnd, win32con.WM_CLOSE)

def stop_app(app_exe):
    for process in psutil.process_iter():
        if process.name() == app_exe:
            win32gui.EnumWindows(enumWindowsProc, process.pid)

with microphone as source:
	recognizer.adjust_for_ambient_noise(source)

	while True:
		print("Speak:")	
		audio = recognizer.listen(source)
		try:
			url=" "
			text = recognizer.recognize_google(audio, language=sl)
			cmd = text.split(" ")
			cmd[0]=cmd[0].lower()
			print("You said:", text) 
			if text=='exit':
				print('Bye Bye, see you!')
				break
			if cmd[0]=='open':
				if cmd[1]=='Chrome' or cmd[1]=='browser':
					win32api.WinExec(BROWSER)
					hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
					print(hwnd)
			if cmd[0]=='search' or cmd[0]=='Google':
				hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
				print(hwnd)
				if len(cmd)==1:
					txt=" "
				else:
					txt=" google.com/search?q="
					for i in range(1,len(cmd)):
						txt += cmd[i]+'+'
				win32api.WinExec(BROWSER+txt[:-1])
			if cmd[0]=='watch' or cmd[0]=='YouTube':
				if len(cmd)==1:
					txt=" youtube.com "
				else:
					txt=" youtube.com/search?q="
					for i in range(1,len(cmd)):
						txt += cmd[i]+'+'
				win32api.WinExec(BROWSER+txt[:-1])
			if cmd[0]=='scroll':
				if len(cmd)>1:
					if cmd[1]=='up':
						keyboard.press('page up')
					if cmd[1]=='down':
						keyboard.press('page down')					
			if cmd[0]=='move':
				if len(cmd)>1:
					if cmd[1]=='up':
						keyboard.press('up')
					if cmd[1]=='down':
						keyboard.press('down')
			if cmd[0]=='play' or cmd[0]=='click':	
				mouse.click(Button.left,1)
			if cmd[0]=='play' or cmd[0]=='click':	
				mouse.click(Button.left,1)
			if cmd[0]=='double' and cmd[1]=='click':
				mouse.click(Button.left,2)				
			if cmd[0]=='close' or cmd[0]=='quit':
				if cmd[1]=='Chrome' or cmd[1]=='browser':
					stop_app('chrome.exe')
			if cmd[0]=='type':
				txt = text.replace(cmd[0]+" ","")+"\n"
				keyboard.type(txt)
				input_len=len(txt)
			if cmd[0]=='cancel':
				if cmd[1]=='Chrome':
					stop_app('chrome.exe')
		except sr.UnknownValueError:
			#print("Could not understand audio!")
			print("please say that again")
		except sr.RequestError as e:
			#print("Could not request results; {0}".format(e))
			pritn("please try again")
		print("")
