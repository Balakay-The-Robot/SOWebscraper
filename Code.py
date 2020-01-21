import urllib.request
from bs4 import BeautifulSoup

import time

url = "https://stackoverflow.com/jobs?sort=i&pg="
min = 0 
index = min;
target = "post-tag job-link no-tag-menu"

max = int(BeautifulSoup(urllib.request.urlopen("https://stackoverflow.com/jobs"), 'html.parser').find_all('a', class_="s-pagination--item")[4].contents[1].text)
print(max)


pages = []

while index <= max:
  temp = url + str(index)
  pages.append(BeautifulSoup(urllib.request.urlopen(temp), 'html.parser').find_all('a', class_=target))
  print(index)
  time.sleep(5)

  index += 1

raw = []
organized = {}

for i in pages:
  for i0 in i:
    raw.append(i0.text)
    if not i0.text in organized:
      organized[i0.text] = 1
    else:
      organized[i0.text] += 1

sorted = []

for i in organized:
