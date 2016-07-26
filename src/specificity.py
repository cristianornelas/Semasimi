import sys
import codecs
import numpy as np
from sklearn import preprocessing

#argv[1] = Path to the file with the frequency of the words
#argv[2] = Path to the output file with the specificity of each word
#specificity = number of documents in the corpus / number of documents that contains that word

def calc_specificity(pFreq, pOutput):

	#Websize is the number of articles in the wikipedia folder
	WEBSIZE = 1521800.0
	COUNTED_WORDS = pFreq
	DESTFOLDER = pOutput
	specList = []

	#Open the file with the words frequency and the file that will store the specificities
	counted_words_file = codecs.open(COUNTED_WORDS, "r", "utf-8")
	specificity_words_file = codecs.open(DESTFOLDER, "wb", "utf-8")

	#Store all terms and its frequency in a list
	terms = counted_words_file.readlines()

	#Create a list to store the frequency of each word
	words_frequency = []

	#Remove the pairs of words from the list
	for each_term in terms:
		if each_term not in words_frequency:
			if "_" not in each_term:
				words_frequency.append(each_term)

	#Calculate the specificity of each individual words
	for each_word in words_frequency:
		word = each_word.split(": ")[0]
		frequecy = float(each_word.split(": ")[1])
		specificity = WEBSIZE / frequecy
		#add the specificity value to a list in order to normalize its values
		specList.append(specificity)

	listSize = len(specList)
	auxSpecList = np.reshape(specList, (-1,1))

	#normalize the specificity values
	min_max_scaler = preprocessing.MinMaxScaler()
	nSpecList = min_max_scaler.fit_transform(auxSpecList)

	normSpecList = np.reshape(nSpecList, listSize)
	
	i = 0
	for x in normSpecList:
		#write the word with the character > in the begining so that there will be no problems with 
		#word that are substring of others
		specificity_words_file.write(">" + words_frequency[i].split(": ")[0] + ": " + str(x) + "\n")
		i += 1