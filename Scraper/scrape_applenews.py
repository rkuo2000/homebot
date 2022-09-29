from bs4 import BeautifulSoup
from selenium import webdriver

url = 'http://www.appledaily.com.tw/realtimenews/section/new/'

browser = webdriver.Chrome(executable_path=r'C:\Users\RKUO\chromedriver.exe') # for Windows
browser.get(url)
soup = BeautifulSoup(browser.page_source, "html5lib")
browser.close()

time=[]
for item in soup.select('.flex-feature '):
    time.append(item.text)

title=[]
for item in soup.select('.box--margin-top'):
    title.append(item.text)

news = {
       'time': time,
       'title': title
}

for title in news['title']:
    print(title)
