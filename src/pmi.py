import codecs
import sys
import math
import numpy as np
from sklearn import preprocessing

def calc_pmi(pFreq, pOutput):

	WORDSCOUNTED = pFreq
	DESTFOLDER = pOutput

	#Websize is the number of  words in the wikipedia corpus,
	#run wc -w < wikipedia to get the number of words, extract tags
	WEBSIZE = 294000000.0

	#Open the file with the words frequency
	words_file = codecs.open(WORDSCOUNTED, "r", "utf-8")

	#Open the file that will store the pmi calculated
	pmi_calculated = codecs.open(DESTFOLDER, "wb", "utf-8")

	#Read all the terms in the frequency file and store into a list
	terms= words_file.readlines()

	#Calculate the pmi of each pair of words and stores into the output file 
	i = 0
	pmiList = []

	while i <= len(terms) - 3:
		#Split the word1 from its frequency
		word1 = terms[i].split(": ")[0]
		freq_word1 = float(terms[i].split(": ")[1])
		
		#Split the word2 from its frequency
		word2 = terms[i+1].split(": ")[0]
		freq_word2 = float(terms[i+1].split(": ")[1])
		
		#Split the word pair from its frequency
		word_pair = terms[i+2].split(": ")[0]
		freq_word_pair = float(terms[i+2].split(": ")[1])

		i += 3

		#Verify if one of the words have 0 as frequency, if yes, the pmi value will be 0
		if (freq_word1 == 0) or (freq_word2 == 0) or (freq_word_pair == 0):
			pmiList.append(0)
		#If none of that happens, calculates the pmi using the formula demostrated in the article
		#Corpus-based and knowledge-based measures of text semantic similarity
		else:
			pmiList.append(math.log((freq_word_pair / WEBSIZE) / ((freq_word1 / WEBSIZE) * (freq_word2/ WEBSIZE)), 2))

	
	listSize = len(pmiList)

	auxPmiList = np.reshape(pmiList, (-1,1))

	#normalize the lsa values
	min_max_scaler = preprocessing.MinMaxScaler()
	nPmiList = min_max_scaler.fit_transform(auxPmiList)

	normPmiList = np.reshape(nPmiList, listSize)

	i = 0
	for word_pair in terms:
		if "_" in word_pair:
			pmi_calculated.write(word_pair.split(": ")[0] + ": " + str(normPmiList[i]) + "\n")
			i += 1
		