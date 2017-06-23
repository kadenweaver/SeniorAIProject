#Title: format2
#Created By: Kaden Weaver
#Purpose: Reads URLs from a txt file, and accesses the Songmeanings.com sites associated with them. This code then collects
#data on the lyrics into three dictionaries. These dictionaries are then pickled for later use by the search engine.
import requests
from bs4 import BeautifulSoup
import collections
import time
import pickle

#global dictionaries to be used in search engine
doclength = collections.defaultdict(int)
doctostats = collections.defaultdict(dict)
numdocs = collections.defaultdict(int)

#accesses the website associated with a URL, identify its lyrics, and collect data on those songs
#Param: aurl = a string, representing a web address
#Return: void, this code maps an artist and song name to its dictionary of term frequencies
def infolyrics(aurl):
    global doclength, doctostats
    try:
        page = requests.get(aurl)
    except requests.exceptions.RequestException as e:
        print("Error loading "+aurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    count = 0
    switch = False
    songinfoswtch = True
    docstats = collections.defaultdict(int)
    commentSwitch = True
    song = ""
    artist = ""

    for string in soup.strings:

        if "SongMeanings" in string and songinfoswtch:
            songinfoswtch = not songinfoswtch
            dashindex = string.find('-')
            lyricsindex = string.find('Lyrics')
            artist = string[:dashindex - 1]
            song = string[dashindex + 2:lyricsindex - 1]
        if switch and count != 6:
            count += 1
        if 'Edit Wiki' in repr(string):
            switch = not switch
        if count == 6 and switch and string.strip()!= '':
            words = string.strip().lower().replace(',', '').replace('!', '').replace('?', '').replace('(', '').replace(')', '').replace('.', '').split(" ")
            for word in words:
                docstats[word]+=1
                doclength[artist+"-"+song]+=1
    doctostats[artist + "-" + song] = docstats
    time.sleep(1)

#updates the numdocs dictionary to tie song titles with their lengths
def update_numdocs():
    global doctostats, numdocs
    for key in doctostats:
        for key2 in doctostats[key]:
            numdocs[key2]+=1


#iterate through the song URLs and collect data
letterlink = 'P:\slulabs\pycharm\\untitled3\popularartists.txt'
file = open(letterlink, "r")
counter = 1
for line in file:
    print("now processing line " + str(counter))
    infolyrics(line.strip())
    print("finished")
    counter += 1
print("finished processing all lines")

update_numdocs()
print("finished updating numdocs")

#pickle the three data structures for use in seach engine.py
with open('thedoctostats1.txt.pickle', 'wb') as handle:
    pickle.dump(doctostats, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("finished pickling doctostats")

with open('numdocs1.txt.pickle', 'wb') as handle:
    pickle.dump(numdocs, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("finished pickling numdocs")

with open('doclength1.txt.pickle', 'wb') as handle:
    pickle.dump(doclength, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("finished pickling doclength")

