import gensim
import bz2
import codecs
import sys
import math
import numpy as np
from os import path
from sklearn import preprocessing

#First, download the dump of all Wikipedia articles from http://download.wikimedia.org/ptwiki/ 
#(you want the file enwiki-latest-pages-articles.xml.bz2, or enwiki-YYYYMMDD-pages-articles.xml.bz2
#for date-specific dumps).

#Then convert the articles to plain text and store the result as sparse TF-IDF vectors using
#python -m gensim.scripts.make_wiki

#NUM_TOPICS is the number of articles that will be processed
NUM_TOPICS = 400


#	if sys.argv[1] == "--create-model":
#		MODEL_PATH = sys.argv[2]
#		WORDIDS_TXT = sys.argv[3]
#		TFIDF_MM = sys.argv[4]
#		else:


#Compute the lsi to all the relevant terms on each article
def create_LSI_model(WORDIDS_TXT, MODEL_PATH):

	# load id->word mapping (the dictionary), one of the results of step 2 above
	id2word = gensim.corpora.Dictionary.load_from_text(WORDIDS_TXT)
	# load corpus iterator
	mm = gensim.corpora.MmCorpus(TFIDF_MM)	

	#extract the LSI topics, use the default one-pass algorithm
	lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=NUM_TOPICS)

	#Save the model
	lsi.save(MODEL_PATH)

#Load the LSI model in order to get the results
def load_LSI_model(MODEL_PATH):

	return gensim.models.LsiModel.load(MODEL_PATH)

#Return a list with all the single terms that are being processed
def get_single_terms(CROSSED_FILE):

	#open the file with the crossed terms
	crossed_terms_file = codecs.open(CROSSED_FILE, "r", "utf-8")
	aux_list = crossed_terms_file.readlines()
	single_terms_list = []

	#copy the single terms to a second list
	for each_term in aux_list:
		if each_term.find("_") == -1:
			single_terms_list.append(each_term.split(":")[0])

	#remove the repetitions
	single_terms_list = set(single_terms_list)

	#return a list with single terms
	return list(single_terms_list)


#Return a list with all the double terms
def get_double_terms(CROSSED_FILE):

	#open the file with the crossed terms
	crossed_terms_file = codecs.open(CROSSED_FILE, "r", "utf-8")
	aux_list = crossed_terms_file.readlines()
	single_terms_list = []

	#copy the double terms to a second list
	for each_term in aux_list:
		if each_term.find("_") > 0:
			single_terms_list.append(each_term.split(":")[0])

	#remove the repetitions
	single_terms_list = set(single_terms_list)

	#return a list with the double terms
	return list(single_terms_list)

#Create files that will store the NUM_TOPICS lsi values for each single term processed
#def create_vectors(single_terms_list):
def create_vectors(single_terms_list, VECTORS_PATH, MODEL_PATH):

	#load the model created in create_LSI_model()
	lsi = load_LSI_model(MODEL_PATH)
	#get the list with the single terms
	#single_terms_list = get_single_terms()


	#For each single term, create its file
	for each_term in single_terms_list:
		output = codecs.open(VECTORS_PATH+each_term.encode("utf-8").lower(), "wb", "utf-8")
		#run throughout the NUM_TOPICS topics saving in a list the 100000 most relevant lsi values
		for each_topic in range(0,NUM_TOPICS):
			print "%s - %d" % (each_term, each_topic)
			tuple_list = lsi.show_topic(each_topic, topn=100000)	
			wrote = False
			#For each list of values, look for the value of the correspondent term and write it on the file
			for each_tuple in tuple_list:
				if each_term.encode("utf-8") == each_tuple[0].encode("utf-8"):
					output.write(str(each_tuple[1])+"\n")
					wrote = True
		#Close the file
		output.close()

#Compute the similarity between two words using its lsi values
def calc_similarity(word1, word2, VECTORS_PATH):

	#verifiy if the two words have its lsi values calculated
	if path.isfile(VECTORS_PATH+word1.lower().encode("utf-8")) and path.isfile(VECTORS_PATH+word2.lower().encode("utf-8")):
		file1 = codecs.open(VECTORS_PATH+word1.lower().encode("utf-8"))
		file2 = codecs.open(VECTORS_PATH+word2.lower().encode("utf-8"))

		#load the lsi values of the words into a list
		lsa_w1 = file1.readlines()
		lsa_w2 = file2.readlines()

		numerator = 0.0
		denominator1 = 0.0
		denominator2 = 0.0

		#compute the similarity between two words
		#standard cosine similarity
		for i in range(0, NUM_TOPICS):
			numerator += float(lsa_w1[i]) * float(lsa_w2[i])
			denominator1 += float(lsa_w1[i]) * float(lsa_w1[i])
			denominator2 += float(lsa_w2[i]) * float(lsa_w2[i])

		denominator1 = math.sqrt(denominator1)
		denominator2 = math.sqrt(denominator2)

		denominator = denominator1 * denominator2

		return numerator / denominator

def calc_lsa(pCrossed_file, pModel_path, pVectors_path, pLsa_values_file):	

	MODEL_PATH = pModel_path
	CROSSED_FILE = pCrossed_file
	VECTORS_PATH = pVectors_path
	LSA_VALUES_FILE = pLsa_values_file
	lsaList = []

	create_vectors(get_single_terms(CROSSED_FILE), VECTORS_PATH, MODEL_PATH)
	double_terms_list = get_double_terms(CROSSED_FILE)

	lsa_file = codecs.open(LSA_VALUES_FILE, "wb", "utf-8")

	for each_double_term in double_terms_list:
		term1 = each_double_term.split("_")[0]
		term2 = each_double_term.split("_")[1]

		lsaList.append(calc_similarity(term1, term2, VECTORS_PATH))

	listSize = len(lsaList)

	auxLsaList = np.reshape(lsaList, (-1,1))

	#normalize the lsa values
	min_max_scaler = preprocessing.MinMaxScaler()
	nLsaList = min_max_scaler.fit_transform(auxLsaList)

	normLsaList = np.reshape(nLsaList, listSize)

	i = 0
	for each_double_term in double_terms_list:
		term1 = each_double_term.split("_")[0]
		term2 = each_double_term.split("_")[1]

		lsa_file.write(each_double_term+": "+str(normLsaList[i])+"\n")
		i += 1