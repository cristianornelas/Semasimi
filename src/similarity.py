import sys
import codecs
import time

#returns a string with the biggest similarity to a word
def max_Sim(word, text, pMeasure_value_calculed):

	MEASURE_VALUE_CALCULED = pMeasure_value_calculed

	#receive the file with the word to word similarity calculated
	#open it and store its value into a list	
	text_file = codecs.open(MEASURE_VALUE_CALCULED, "r", "utf-8")	
	measure_value_content = text_file.readlines()
	biggest = -1	#variable that holds the biggest similarity value
	aux1 = ""	#variable that holds the corresponding pair of terms to the biggest similarity

	#Search in the similarity file, which word is more similar to the the word passed by parameter
	for each_word in text:
		for each_line in measure_value_content:
			aux = word.rstrip() + "_" +each_word.rstrip()	#concatenates the word passed by parameter with each word of the text
			if aux.lower() in each_line.lower():	#if it is in the line, verifies if its measure_value value
				tempWord = each_line.split(": ")[0] 
				measure_value = float(each_line.split(": ")[1])
				if measure_value > biggest:	#if it is bigger, than swap the biggest variable
					biggest = measure_value
					aux1 = tempWord

	#return a string term1_term2: biggest_similarity
	return aux1 + ": " + str(biggest)

#return a float with the the specificity of the word
def find_specificity(word, pSpecificity_file):

	SPECIFICITY_FILE = pSpecificity_file
	
	specificity = codecs.open(SPECIFICITY_FILE, "r", "utf-8")

	content_specificity = specificity.readlines()
	spec_value = -1.0

	#use the > symbol to delimiter the begining of the word and : to delimeter the end of it
	#this way there will be no problem with words that are substring to others
	aux = ">" + word.rstrip() + ": "
	for x in content_specificity:
		if aux.lower() in x.lower():
			spec_value = float(x.split(": ")[1])

	return spec_value


def calc_similarity(pText1, pText2, measure_valueFile, pSpecFile, pOutputFile):

	MEASURE_VALUE_CALCULED = measure_valueFile	
	SPECIFICITY_FILE = pSpecFile

	#Create a list with the POS that are irrelevant to semantic similarity
	CONDITIONS = ["PREP", "X", "ART", "KC", "PRO-KS-REL"]

	#The files with the two texts that are being compared
	TEXT1_FILE = pText1
	TEXT2_FILE = pText2

	#The list that will store the words from the two texts without the words that aren't relevant
	list1 = []
	list2 = []

	file1 = codecs.open(TEXT1_FILE, "r", "utf-8")
	file2 = codecs.open(TEXT2_FILE, "r", "utf-8")

	#Store the lines from each of the text files in lists
	content_file1 = file1.readlines()
	content_file2 = file2.readlines()

	#Store in its lists the words that are relevant
	#NAO ESQUECER DE TIRAR O IF COUNT > 7, TA AI PQ O TEXTOS TEM 7 LINHAS INUTEIS
	count = 0
	for x in content_file1:
		count += 1
		if count > 7:
			aux = x.split("\t")
			if not any(x in aux[1] for x in CONDITIONS):
				list1.append(aux[2])
	count = 0
	for x in content_file2:
		count += 1
		if count > 7:
			aux = x.split("\t")
			if not any(x in aux[1] for x in CONDITIONS):
				list2.append(aux[2])

	#Initialize the variables that will store the sum of all similarity and specificity
	measure_value_specif_sum = 0.0
	specif_sum = 0.0
	for each_word in list1:
		#For each word of text1, finds its specificity and the max similarity word in text2
		maxSimLine = max_Sim(each_word, list2, MEASURE_VALUE_CALCULED)
		specificity = find_specificity(each_word, SPECIFICITY_FILE)

		#Split the similarity value from the pair of terms
		maxSimTerms = maxSimLine.split(": ")[0]
		if maxSimLine.find("UNKNOWN") == -1:
			max_sim_measure_value = float(maxSimLine.split(": ")[1])
			
			#Sum all the maxSims * specificity
			measure_value_specif_sum += max_sim_measure_value * specificity

			#Sum all the specificities
			specif_sum += specificity

	#Calculate the first term of the equation
	first_term = measure_value_specif_sum / specif_sum

	#Initialize the variables that will store the sum of all similarity and specificity
	measure_value_specif_sum = 0.0
	specif_sum = 0.0
	for each_word in list2:
		#For each word of text2, finds its specificity and the max similarity word in text1
		maxSimLine = max_Sim(each_word, list1, MEASURE_VALUE_CALCULED)
		specificity = find_specificity(each_word, SPECIFICITY_FILE)
		
		#Split the similarity value from the pair of terms
		maxSimTerms = maxSimLine.split(": ")[0]
		if maxSimLine.find("UNKNOWN") == -1:
			max_sim_measure_value = float(maxSimLine.split(": ")[1])
			
			#Sum all the maxSims * specificity
			measure_value_specif_sum += max_sim_measure_value * specificity

			#Sum all the specificities
			specif_sum += specificity

	#Calculate the second term of the equation
	second_term = measure_value_specif_sum / specif_sum

	result = (first_term + second_term) / 2.0

	finalOutput = codecs.open(pOutputFile, "a")
	finalOutput.write("%s_%s: %f\n" % (pText1, pText2, result))
	#print "The result is: %f" % result