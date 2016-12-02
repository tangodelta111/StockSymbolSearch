import sqlite3 as lite
import json
import sys
import requests


dataURL = "http://oatsreportable.finra.org/OATSReportableSecurities-SOD.txt"

r = requests.get(dataURL)

datalist = [tuple(str(s.strip()).split('|')) for s in r.text.splitlines()]

datalist.pop(0)
datalist.pop()

#Create table Companies(Symbol TEXT UNIQUE, Name TEXT, Market TEXT, SName TEXT)

con = lite.connect("symbols.db")

#Creates a new list for holding the expanded tuples list
datalist2 = []

for data in datalist:
	sName = re.sub(r'[^\w]', ' ', data[1].lower()) + " " #Removes all symbols
	sName = sName + re.sub(r'[^\w ]', '', data[1].lower()) + " " #Removes all symbols but no spaces
	sName = sName + re.sub(r'(philip)\b', "phillip", data[1].lower()) + " " #Changes Philip to Phillip, since alexa can't recognize Philip.
	sName = sName + re.sub(r'(and)\b', " and ", re.sub(r'(\&)', " and ", data[1].lower())) + " "
	sName = sName + re.sub(r'(\&)', " and ", data[1].lower()) + " "
	sName = sName + re.sub(r'(and)\b', " and ", sName) + " " # adds a space betwen and since some names are cool like that.
	sName = sName + re.sub(r'(and)\b', " and ", data[1].lower()) + " "  
	sName = sName + re.sub(r'(^[A-Z]{2})', r'\1 ', data[1]) + " "#separate out names like JPMorgan to JP Morgan.
	sName = sName + re.sub(r'(\&)', " and ", data[1].lower()) #changes all the & to and
	newTuple = (data[0], data[1], data[2], sName)
	datalist2.append(newTuple)

with con:
	cur = con.cursor()
	cur.executemany("INSERT OR IGNORE INTO Companies VALUES(?, ?, ?, ?)", datalist2)
	cur.execute("DELETE FROM Companies WHERE Symbol=?", ("PHPMF",))
	cur.execute("DELETE FROM Companies WHERE Symbol=?", ("HRCR",))
con.close()
