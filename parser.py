import tkinter as Tkinter
from tkinter import font as tkFont
from docx import Document
import re

Tkinter.Frame().destroy()
chordFont = tkFont.Font(family="Times New Roman", size=8, weight="bold")
textFont = tkFont.Font(family="Times New Roman", size=10)

def isTitle(inputString):
    return any(char.isdigit() for char in inputString)

def getTitle(inputString):
    return inputString.split('.')[1]

def getSongNo(inputString):
    return inputString.split('.')[0]

def getScale(inputString):
    return inputString.split(' ')[0]

def get_printed_size(text,font):
    return font.measure(text)

def find_index(s1,loc):
    for i, c in enumerate(s1):
        if (get_printed_size(s1[0:i],textFont)) > loc:
            return i+1

def get_chord_vector(s1):
    chordregex = '[A-Za-z][A-Za-z0-9]*'
    cvector = dict()
    for match in re.finditer(chordregex, s1):
        s = match.start()
        e = match.end()
        cvector[get_printed_size(s1[0:s],chordFont)] = s1[s:e]
    return cvector

def insert_chords(s1,cv):
    oi = 0
    os = ""
    for loc in cv:
        i = find_index(s1,loc)
        os = os + s1[oi:i] + '[' + cv[loc] + ']'
        oi = i
    os = os + s1[oi:len(s1)]
    return os

document = Document('data/NTC Songs 1-1000.docx')
styles = document.styles

count = 0
firstLine = False
hasChords = True
inChorus = False
cv = dict()

for para in document.paragraphs:
    if str(para.style.name) == "SONG TITLE":
        count = count + 1
#        if count > 157:
 #           exit(0)
        if isTitle(para.text):
            print ("\n\n{song number: " + getSongNo(para.text.lstrip()) + "}")
            print ("{title: " + getTitle(para.text.lstrip()) + "}")
            firstLine = True

    if (firstLine and (para.style.name == "CHORDS")):
        print ("Scale: " + getScale(para.text.lstrip()))
        firstLine = False

    if (para.style.name == "CHORDS"):
        hasChords = True
        cv = get_chord_vector(para.text.replace("\t", "   "))
#        for x in cv:
#            print('Chord : %s in location %d' % (cv[x], x))

    if (para.style.name == "REGULAR" and para.text.strip()== "Chorus:"):
        inChorus = True
        print("{start_of_chorus}")

    if (inChorus and para.style.name == "REGULAR" and len(para.text.strip()) == 0 ):
        inChorus = False
        print("{end_of_chorus}")

    if (para.style.name == "REGULAR"):
        if (hasChords):
            print(insert_chords(para.text.replace("\t", "   "), cv))
        else:
            print(para.text)
        hasChords = False

