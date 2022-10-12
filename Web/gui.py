# pip install PySimpleGUI

import PySimpleGUI as sg
name = sg.popup_get_text('輸入你的姓名')
sg.popup_no_buttons('你的名字是'+name)
