#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import re

#url = 'https://www.youtube.com/results?search_query=alan+walker'
#url = 'https://www.youtube.com/user/DjWalkzz'
#url = 'https://www.youtube.com/results?search_query=Dua+Lipa'
#url = 'https://www.youtube.com/results?search_query=INNA'
url = 'https://www.youtube.com/results?search_query=Top+50+this+week'
#url = 'https://www.youtube.com/watch?v=Nj2U6rhnucI&list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG'

res = requests.get(url)
page = res.text
soup = BeautifulSoup(page, "html5lib")
# soup.select('.class')
# soup.select('#id')
# soup.select('a')  # for tag
# soup.select('.class a')

contents = soup.select('.yt-lockup-content')
titles=[]
hrefs =[]

i=0
for content in contents:
	text=str(content)
	
	b=text.find('title=')
	title=text[b:]
	e=title[7:].find('"')
	title=title[:e+8]
	titles.append(title[7:-1])
	
	b=text.find('href=')
	href=text[b:]
	e =href.find(' ')
	href=href[:e]
	href=href.replace('&amp;','&')
	hrefs.append(href[6:-1])
	i+=1

for i in range(len(titles)):
	print(hrefs[i], titles[i])
print(len(hrefs))
