#Title: search engine
#Created By: Kaden Weaver
#Purpose: Accepts user queries and returns the top three relevant documents based on three different scoring functions,
#all of which are variants of a regular BM25 function.
import pickle
import collections
import math
import nltk

#unpickle relevant documents
with open('thedoctostats1.txt.pickle', 'rb') as handle:
    doctostats = pickle.load(handle)

with open('numdocs1.txt.pickle', 'rb') as handle:
    numdocs = pickle.load(handle)

with open('doclength1.txt.pickle', 'rb') as handle:
    doclength = pickle.load(handle)


numofsongs = 0
numofsongs2 = 0
totallength = 0

for key in doclength:
    numofsongs += 1
    totallength += doclength[key]
for key in doctostats:
    numofsongs2 += 1

#provide basic information about the corpus of documents accessed
print("There are "+str(numofsongs) + " songs")
print("The total length of documents is " + str(totallength) + " words")
print("The average document length is " + str(totallength/numofsongs) + " words")

averagelength = totallength/numofsongs


#takes a word and computes its inverse document frequency based off of the word's document frequency
#Param: aword = a word, represented as a string
#Return: idf = a float, representing the IDF of the word
def inverse_doc_freq(aword):
    global numofsongs, numdocs
    df = float(numdocs[aword])
    numerator = float(numofsongs) - df +.5
    denominator = df + 0.5
    inner = numerator/denominator
    idf = math.log(inner)
    return idf

#takes a word and computes its inverse document frequency based off of the word's document frequency
#Param: aword = a word, represented as a string
#Return: idf = a float, representing the IDF of the word
def hit_list(aquery):
    global doctostats
    hitset = set()

    setofwords = set(aquery.lower().replace("?","").replace("!","").replace(",","").replace("'","").split(" "))

    for doc in doctostats:
        wordset = set(doctostats[doc])
        for word in setofwords:
            if word in wordset:
                hitset.add(doc)
    return hitset

#measures a document's relevancy to a query using the bm25 equation
#Param: adoc = a string, a song lyric document represented as artistname"-"songname
#       aquery = a string containing a user's query input
#Return: adocscore = a float, measuring the document's relevance to the given query
def bm25(adoc, aquery):
    global doctostats, doclength, averagelength
    adocscore = 0
    k = 2.0
    b = 0.75
    adoclength = doclength[adoc]
    setofwords = set(aquery.lower().replace("?", "").replace("!", "").replace(",", "").replace("'", "").split(" "))
    for word in setofwords:
        idf = inverse_doc_freq(word)
        tf = float(doctostats[adoc][word])
        numerator = tf * (k+1)
        denominator = tf + k * (1-b+b*adoclength/averagelength)
        fraction = numerator/denominator
        singlebm25 = idf * fraction
        adocscore += singlebm25
    return adocscore

#same as bm25 but b = 0.0
def bm25k(adoc, aquery):
    global doctostats, doclength, averagelength
    adocscore = 0
    k = 2.0
    b = 0.0
    adoclength = doclength[adoc]
    setofwords = set(aquery.split(" "))
    for word in setofwords:
        idf = inverse_doc_freq(word)
        tf = float(doctostats[adoc][word])
        numerator = tf * (k+1)
        denominator = tf + k * (1-b+b*adoclength/averagelength)
        fraction = numerator/denominator
        singlebm25 = idf * fraction
        adocscore += singlebm25
    return adocscore

#same as bm25 but b = 1.5
def bm25b(adoc, aquery):
    global doctostats, doclength, averagelength
    adocscore = 0
    k = 2.0
    b = 1.5
    adoclength = doclength[adoc]
    setofwords = set(aquery.split(" "))
    for word in setofwords:
        idf = inverse_doc_freq(word)
        tf = float(doctostats[adoc][word])
        numerator = tf * (k+1)
        denominator = tf + k * (1-b+b*adoclength/averagelength)
        fraction = numerator/denominator
        singlebm25 = idf * fraction
        adocscore += singlebm25
    return adocscore

#the actual search engine-- this method takes user input and returns the three highest-ranking documents for each
#of the three functions. It will then check to see if it found the user's result, and allow the user to search for the
#correct song in its copus if not.
#Param: aquery = a string, containing a user's query input
#Return: void, this method prints out BM scores and checks its own precision
def search(aquery):
    global doctostats
    hitlistscores = collections.defaultdict(int)
    hitlistscoresk = collections.defaultdict(int)
    hitlistscoresb = collections.defaultdict(int)
    hitset = hit_list(aquery)

    for doc in hitset:
        hitlistscores[doc]=bm25(doc, aquery)
        hitlistscoresk[doc] = bm25k(doc, aquery)
        hitlistscoresb[doc] = bm25b(doc, aquery)
    dictlist = [hitlistscores,hitlistscoresk,hitlistscoresb]
    for list in dictlist:
        result = scorelist(list)
    response = input("Did the engine find your song? Put y/n ")

    if 'n' in response:
        artistname = input("Input the artist name with correct capitalization: ")
        for key in doctostats:
            if artistname in key:
                print(key)
        songname = input("If the song is here, put its name: ")
        if (artistname+"-"+songname) not in hitlistscores:
            print("No Result")
        else:
            print(hitlistscores[artistname+"-"+songname])
            print(hitlistscoresk[artistname + "-" + songname])
            print(hitlistscoresb[artistname + "-" + songname])

#prints the top three results for a scoring function
#Param: alist = a dictionary, mapping documents to their BM scores
#Return: savehitlist = a list, containing the three top results from a BM score dictionary
def scorelist(alist):
    savehitlist = list()
    for n in range(3):
        if len(alist) != 0:
            maxdoc = max(alist, key=alist.get)
            print(str(n + 1) + ". " + maxdoc + " BM25 Score: " + str(alist[maxdoc]))
            savehitlist.append((maxdoc, alist[maxdoc]))
            del alist[maxdoc]
        else:
            print("---No Result---")
    print()
    return savehitlist


query = input("Lyrics search: ")

search(query)

