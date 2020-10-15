#Project by Blayke Nutter
#.
#Used to scrape through the stack overflow jobs page and see what skills are requested the most
#
#Creates 3 arrays: 
#
#     raw (each occurance of a tag is appended to the array),
# 
#     organized (dictionary of format INDEX:TAG VALUE:OCCURANCE), 
#
#     sorted (tags are sorted by most to least occurace in a 2d array where the innermost is in the format (tag, occurance))

import urllib.request
from bs4 import BeautifulSoup

import time

def check(array):
  if len(array) <= 1: #If the array is empty or only has one item then it is already sorted
    return True

  #go through array checking every element against the previous to see if its sorted
  i = 1;
  while i < len(array):
    if array[i][1] > array[i-1][1]:
      return False #If not sorted than return false
    else:
      i += 1 #If in right position then go to next element

  #If code gets to this point then its gone through all elements so its sorted
  return True
  
def partitionAround(array, index):
  part1 = [] #All items greater than index
  part2 = [] #Items less than index

  #Loops through elements and puts them in the correct array
  for i in array:
    if i[1] > index[1]:
      part1.append(i) #item is greater than index so add to first array
    else:
      part2.append(i) #Item is equal to or less than index array

  #return the arrays through another array
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

#writes the inputted data to the specifed file
def writeToFile(fileName, data):
  f = open(fileName, "w")
  f.close()
  f = open(fileName, "a")

  #put data in the file in the format "tag, amount\n"
  for i in data:
    f.write(i[0]+", "+str(i[1])+"\n")
  f.close()
#read the csv file with the name specifed and returns its value
def readCSV(fileName):
  f = open(fileName, "r")
  values = f.readlines()

  returnData = [];
  
  for line in values:
    i = len(line)-1
    while i >= 0:
      if line[i] == ",":
        break;
      i -=1
    val1 = ""
    val2 = ""
    for x in range(i):
      val1 += line[x]
    for y in range(len(line) - i-1):
      val2 = val2 + line[y+i+1]
    returnData.append([val1, int(val2)])
  return returnData
#combines the two arrays by combining elements that share the same tag and adding their occurance then returns the output
def merge(arr1, arr2):
  merged = []
  i = 0
  while i < len(arr1):
    iterate = True
    i1 = 0
    while i1 < len(arr2):
      print(i, i1)
      if(arr1[i][0] == arr2[i1][0]):
        merged.append([arr1[i][0], arr1[i][1] + arr2[i1][1]])
        print(merged[len(merged)-1])
        arr1.pop(i)
        arr2.pop(i1)
        iterate = False
        break
      i1 += 1
    if iterate: i+= 1
  for item in arr1:
    merged.append(item)
  for item in arr2:
    merged.append(item)
  return sort(merged)

url = "https://stackoverflow.com/jobs?pg=" #Base URL to which the index is added in order to get the pages
target = "post-tag no-tag-menu" #Specifying the class of the tags that contain (the data being searched for) skill requests 
index = 0 #index of the first page OR the one you want to start at

#Goes to pages indexed by only less than or equal to the user input OR finds the last indexed page and sets that as max 
try:
  max = int(input("Maximum page index to use: "))
except:
  max = int(BeautifulSoup(urllib.request.urlopen("https://stackoverflow.com/jobs"), 'html.parser').find_all('a', class_="s-pagination--item")[4].contents[1].text)
  print("\t"+str(max)) #Finds the index of last page
  max = max-1 #Account for arrays counting from 0

#Wait this many seconds between each page
#Set the wait time to input OR to the default if invalid
try:
  wait = int(input("Courtesy wait time between pages in seconds: "))
except:
  wait = 5
  print("\t Default " + str(wait) + " Seconds")

#open all pages and adds their tags to the array
pages = []
while index <= max:
  temp = url + str(index)
  pages.append(BeautifulSoup(urllib.request.urlopen(temp), 'html.parser').find_all('a', class_=target))
  print(index)
  time.sleep(wait)
  index += 1

raw = [] #each instance of a tag is represented up appending the tag to the array
organized = {} #each tag is an index to a number which is how many times it occured

#sort tags
for i in pages:
  for i0 in i:
    raw.append(i0.text) # put the tag name in the unorganized array
    
    #If tag hasnt been recorded then add it to the organized array, if it has than increase the amount counted by one
    if not i0.text in organized:
      organized[i0.text] = 1
    else:
      organized[i0.text] += 1

sorted = [] #"organized" array sorted by most to least occurance

#Convert array "organized" into a useable format for sort function then sort
for i in organized:
  sorted.append([i, organized[i]]) 
sorted = sort(sorted)

writeToFile(input("Save data to filename: "), sorted)

#prints the first however so many out of the organized list OR prints all
try:
  readOut = int(input("Prints the first X amount of tags sorted by most to least occurace: "))
except:
  readOut = len(sorted)
for i in range(readOut):
  print(sorted[i][0]+", "+str(sorted[i][1]))
