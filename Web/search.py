# pip install google

from googlesearch import search

query = "Tesla Optimus"

for url in search(query):
    print(url)
