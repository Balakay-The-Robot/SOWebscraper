import urllib.request
from bs4 import BeautifulSoup

import time

url = "https://stackoverflow.com/jobs?sort=i&pg=" #Base URL to which the index is added in order to get the multiple pages of jobs
min = 0 #Minimum index value that has a webpage associated with it
index = min; #defining interator that combs through the many pages
target = "post-tag job-link no-tag-menu" #Specifying the class of the tags that contain skill requests

try:
  max = int(input("Max: ")) #If input is a number then only go through pages with a index less than or equal to the input
except:
  max = int(BeautifulSoup(urllib.request.urlopen("https://stackoverflow.com/jobs"), 'html.parser').find_all('a', class_="s-pagination--item")[4].contents[1].text)#If input is not a number than go thorugh all of the pages
  
  print("\t"+str(max)) #Print the value to console
  max = max-1 #Account for arrays counting from 0

try:
  wait = int(input("Courtesy Wait Time: ")) #If input is a number than wait this many seconds between requests
except:
  wait = 5; #If input is invalid then set wait period to a default of 5 seconds

pages = [] #Define an array to store requested pages

while index <= max:
  try:
    temp = url + str(index) #Get exact page's url
    pages.append(BeautifulSoup(urllib.request.urlopen(temp), 'html.parser').find_all('a', class_=target)) #Get target tagss' values and add it to "pages" array 
  
    print(index)
    time.sleep(wait)
    index += 1
  except:
    break

#Define arrays to store the the tags and the amount of times they occur
raw = []
organized = {}

for i in pages:#Open all the pages
  for i0 in i:#Open every tag in the page
    raw.append(i0.text) #Add tag to raw storage
    
    if not i0.text in organized:
      organized[i0.text] = 1 #If it doesn't exist in organized then add it to organized with an occurrance of 1
    else:
      organized[i0.text] += 1 #If it exists in organized then increase the stored amount by one

def check(array):
  if len(array) <= 1: #If the array is empty or only has one item then it is already sorted
    return True
  i = 1; #Define iterator to loop through array
  while i < len(array):
    if array[i][1] > array[i-1][1] : #Check if items are not in order
      return False
    else:
      i += 1

  return True
  
def partitionAround(array, index):
  part1 = [] #All items greater than index
  part2 = [] #Items less than index

  for i in array:
    if i[1] > index[1]: #Add itme to relevent array
      part1.append(i)
    else:
      part2.append(i)

  return [part1, part2]


def sort(unSortedArray):
  index = unSortedArray.pop(len(unSortedArray)-1) #Define pivot point and then remove it from array
  tempArrays = partitionAround(unSortedArray, index)
  if not check(tempArrays[0]): #If the sections are not sorted then sort them through recursion
    tempArrays[0] = sort(tempArrays[0])
  if not check(tempArrays[1]):
    tempArrays[1] = sort(tempArrays[1])
  
  tempArrays[0].append(index) #Add removed pivot point
  return tempArrays[0] + tempArrays[1] #Combine everything into one list

sorted = [] #Define array used for sorting items from greatest to least occurrance

for i in organized:
  sorted.append([i, organized[i]]) #Convert array "organized" into a useable format for sort function
sorted = sort(sorted)

#Erase file and then open it in write-append mode
f = open("OrganizedValues.csv", "w") 
f.close()
f = open("OrganizedValues.csv", "a")

for i in sorted:
  temp = i[0]+", "+str(i[1])+"\n"
  f.write(temp) #Append data to file

f.close()

try:
  readOut = int(input("Read Top: "))#Print the top input amount of items
except:
  readOut = len(sorted)#Print all items if input is not a number

for i in range(readOut): #Print items to console
  print(sorted[i][0]+", "+str(sorted[i][1]))
