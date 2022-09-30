### pip install BeautifulSoup4
### pip install html5lib
### pip install selenium
# download chromedriver.exe (https://chromedriver.chromium.org/downloads)
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.accuweather.com/en/tw/taipei-city/315078/weather-forecast/315078'

browser = webdriver.Chrome(executable_path=r'C:\Users\RKUO\chromedriver.exe') # for Windows
browser.get(url)
soup = BeautifulSoup(browser.page_source, "html5lib")
browser.close()

item = soup.select('.temp')
temp = item[0].text
print("Current Temp:",temp.replace('\t','').replace('\n',''))

item = soup.select('.real-feel')
real = item[0].text
print("Real-Feel:", real.replace('\t','').replace('\n',''))

item = soup.select('.cond')
cond = item[0].text
print("Condition:",cond.replace('\t','').replace('\n',''))
