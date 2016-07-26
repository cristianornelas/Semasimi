from lxml import etree
from operator import add
import sys
import time
import regex
import codecs
from threading import Thread
import multiprocessing
import operator
import numpy as np

#verify if a text segment contains a specific word
def findWholeWord(w):
	return regex.compile(ur'\b({0})\b'.format(w), regex.UNICODE | regex.IGNORECASE).search

#verify if a text segment contains two specific words with a max distance of 10 words between them
def findPair(w1,w2):
    return regex.compile(ur'\b{0}(?:\W+\w+){{0,10}}\W+{1}\b'.format(w1,w2), regex.UNICODE | regex.IGNORECASE).search

def findTerms(threadName, XMLFILE, list_terms, queue):
	print "Running thread %d" % threadName

	list_count_terms = queue.get()

	context = etree.iterparse(XMLFILE, events=("end",), tag="page")

	#for each article, which is each <page> tag, verifies if each term or pair of terms appear in it
	count = 0
	for event, elem in context:
		for each_term in list_terms:
			#If it's a pair of terms
			if each_term.find("_") > -1:
				words = each_term.split(":")[0]
				if findPair(words.split("_")[0], words.split("_")[1])(elem.text) or findPair(words.split("_")[1], words.split("_")[0])(elem.text):
					index = list_terms.index(each_term)
					list_count_terms[index] += 1	
			#If it's only one term
			elif each_term.find("_") == -1 and findWholeWord(each_term.split(":")[0])(elem.text):
				index = list_terms.index(each_term)
				list_count_terms[index] += 1
		count += 1
		if count % 1000 == 0:
			print "Thread %d processed %d articles." % (threadName, count)
		#after verifing all the terms, clear the element from memory, because otherwise we end up with all the file in memory, and THAT IS BAD
		elem.clear()

	queue.put(list_count_terms)
	print "Thread %d finished" % threadName

#Count in how many articles each word and pair appear
def count_terms(pXml, pTerms, pOutput):
	#XML file extracted from wikiforia [https://github.com/marcusklang/wikiforia]
	XMLFILE = pXml
	#File with the terms
	CROSSEDFILE = pTerms
	#File with the frequency of each term
	OUTPUTFILE = pOutput

	cpuNumber = multiprocessing.cpu_count()

	#Open all the files needed in the code
	output_file = codecs.open(OUTPUTFILE, "wb", "utf-8")
	content_crossed_file = codecs.open(CROSSEDFILE, "r", "utf-8")

	#remove the repeated terms
	backup_list_terms = content_crossed_file.readlines()
	list_terms = set(backup_list_terms)
	list_terms = list(list_terms)

	list_count_terms = np.zeros((cpuNumber, len(list_terms)), dtype=np.int)

	queues = []
	for i in range(0, cpuNumber):
		queues.append(multiprocessing.Queue())

	for i in range(0, cpuNumber):
		queues[i].put(list_count_terms[i])

	activeThreads = []
	for i in range(0, cpuNumber):
		activeThreads.append(multiprocessing.Process(target=findTerms, args=(i, XMLFILE+str(i), list_terms, queues[i])))
		activeThreads[i].start()
	
	for i in range(0, cpuNumber):
		activeThreads[i].join()

	auxList = np.zeros((len(list_terms),), dtype=np.int)
	for i in range(0, cpuNumber):
		each_count_list = queues[i].get()
		auxList = map(add, auxList, each_count_list)

	#Write the terms and their frequency in a file
	for each_term in backup_list_terms:
		index = list_terms.index(each_term)
		output_file.write(each_term.rstrip() + " " + str(auxList[index]) + "\n")
