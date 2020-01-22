import urllib.request
from bs4 import BeautifulSoup

import time

url = "https://stackoverflow.com/jobs?sort=i&pg="
min = 0 
index = min;
target = "post-tag job-link no-tag-menu"

try:
  max = int(input("Max: "))
except:
  max = int(BeautifulSoup(urllib.request.urlopen("https://stackoverflow.com/jobs"), 'html.parser').find_all('a', class_="s-pagination--item")[4].contents[1].text)

try:
  wait = int(input("Courtesy Wait Time: "))
except:
  wait = 5;

print(max)

pages = []

while index <= max:
  temp = url + str(index)
  pages.append(BeautifulSoup(urllib.request.urlopen(temp), 'html.parser').find_all('a', class_=target))
  print(index)
  time.sleep(wait)

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

def check(array):
  if len(array) <= 1:
    return True
  i = 1;
  while i < len(array):
    if array[i][1] > array[i-1][1] :
      return False
    else:
      i += 1

  return True
  
def partitionAround(array, index):
  part1 = []
  part2 = []
  for i in array:
    if i[1] > index[1]:
      part1.append(i)
    else:
      part2.append(i)
  return [part1, part2]


def sort(unSortedArray):
  index = unSortedArray.pop(len(unSortedArray)-1)
  tempArrays = partitionAround(unSortedArray, index)
  if not check(tempArrays[0]):
    tempArrays[0] = sort(tempArrays[0])
  if not check(tempArrays[1]):
    tempArrays[1] = sort(tempArrays[1])
  tempArrays[0].append(index)
  return tempArrays[0] + tempArrays[1]

sorted = []

for i in organized:
  sorted.append([i, organized[i]])
sorted = sort(sorted)

f = open("OrganizedValues.csv", "w")
f.close()
f = open("OrganizedValues.csv", "a")

for i in sorted:
  temp = i[0]+", "+str(i[1])+"\n"
  f.write(temp)

f.close()

try:
  readOut = int(input("Read Top: "))
except:
  readOut = len(sorted)

for i in range(readOut):
  print(sorted[i][0]+", "+str(sorted[i][1]))
