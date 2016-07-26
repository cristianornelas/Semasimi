from os import listdir
from os.path import isfile, join
import preprocessing
import frequency
import specificity
import pmi
import sys
import lsa
import codecs
import similarity

if len(sys.argv) == 1:
	print "For usage instructions, please use [python program.py --pmi] in case of pmi or [python program.py --lsa] in case of lsa"
else:
	if sys.argv[1] == "--pmi":
		if len(sys.argv) == 2:
			print "Usage is: python program.py --pmi [arg1] [arg2] [arg3] [arg4] [arg5] [arg6]"
			print "[arg1] = Path to the texts folder"
			print "[arg2] = Path to the file with the crossed terms"
			print "[arg3] = Path to the xml file produced by Wikiforia [https://github.com/marcusklang/wikiforia]"
			print "[arg4] = Path to the output file with the frequency of the terms"
			print "[arg5] = Path to the output file with the specificity of each word"
			print "[arg6] = Path to the output file with the pmi calculated for each term"
			print "[arg7] = Path to the folder with the similarity between all the texts"
		else:
			textFolder = sys.argv[2]
			auxListFiles = [f for f in listdir(textFolder) if isfile(join(textFolder, f))]

			listFiles = []

			for x in auxListFiles:
				if ".ann" in x:
					listFiles.append(x)

			for i in range(0, len(listFiles)):
				for j in range(i, len(listFiles)):
					if(listFiles[i] != listFiles[j]):
						print "%s - %s" % (textFolder+listFiles[i],textFolder+listFiles[j])
						#argv[2] = Path to the folder with the texts[INPUT]
						#argv[3] = Path to the file with the crossed terms [OUTPUT]
						preprocessing.cross_texts(textFolder+listFiles[i], textFolder+listFiles[j], sys.argv[3])

						#argv[4] = Path to the xml file produced by Wikiforia [https://github.com/marcusklang/wikiforia] [INPUT]
						#argv[3] = Path to the file with the crossed terms [INPUT]
						#argv[5] = Path to the output file with the frequency of the terms [OUTPUT]
						frequency.count_terms(sys.argv[4], sys.argv[3], sys.argv[5])

						#argv[5] = Path to the output file with the frequency of the terms [INPUT]
						#argv[6] = Path to the output file with the specificity of each word [OUTPUT]
						specificity.calc_specificity(sys.argv[5], sys.argv[6])

						#argv[5] = Path to the output file with the frequency of the terms [INPUT]
						#argv[7] = Path to the output file with the pmi calculated for each term [OUTPUT]
						pmi.calc_pmi(sys.argv[5], sys.argv[7])

						#argv[2] = Path to the folder with the texts [INPUT]
						#argv[7] = Path to the output file with the pmi calculated for each term [INPUT]
						#argv[6] = Path to the output file with the specificity of each word [INPUT]
						#argv[8] = Path to the folder with the similarity between all the texts
						similarity.calc_similarity(textFolder+listFiles[i], textFolder+listFiles[j], sys.argv[7], sys.argv[6], sys.argv[8])

	elif sys.argv[1] =='--lsa':
		if len(sys.argv) == 2:
			print "Usage is: python program.py --lsa [arg1] [arg2] [arg3] [arg4] [arg5] [arg6] [arg7] [arg8] [arg9]"
			print "[arg1] = Path to the texts folder"
			print "[arg2] = Path to the file with the crossed terms"
			print "[arg3] = Path to the xml file produced by Wikiforia [https://github.com/marcusklang/wikiforia]"
			print "[arg4] = Path to the output file with the frequency of the terms"
			print "[arg5] = Path to the output file with the specificity of each word"
			print "[arg6] = Path to the model"
			print "[arg7] = Path to the vectors directory"
			print "[arg8] = Path to the file with the value of similarity between words" 
			print "[arg9] = Path to the file with the similarity between all the texts"
		else:
			textFolder = sys.argv[2]
			auxListFiles = [f for f in listdir(textFolder) if isfile(join(textFolder, f))]

			listFiles = []

			for x in auxListFiles:
				if ".ann" in x:
					listFiles.append(x)


			for i in range(0, len(listFiles)):
				for j in range(i, len(listFiles)):
					if(listFiles[i] != listFiles[j]):
						print "%s - %s" % (textFolder+listFiles[i],textFolder+listFiles[j])
						#argv[2] = Path to the folder with the texts[INPUT]
						#argv[3] = Path to the file with the crossed terms [OUTPUT]
						preprocessing.cross_texts(textFolder+listFiles[i], textFolder+listFiles[j], sys.argv[3])

						#argv[4] = Path to the xml file produced by Wikiforia [https://github.com/marcusklang/wikiforia] [INPUT]
						#argv[3] = Path to the file with the crossed terms [INPUT]
						#argv[5] = Path to the output file with the frequency of the terms [OUTPUT]
						frequency.count_terms(sys.argv[4], sys.argv[3], sys.argv[5])

						#argv[5] = Path to the output file with the frequency of the terms [INPUT]
						#argv[6] = Path to the output file with the specificity of each word [OUTPUT]
						specificity.calc_specificity(sys.argv[5], sys.argv[6])

						#argv[3] = Path to the file with the crossed terms [OUTPUT]
						#argv[7] = Path to the model [INPUT]
						#argv[8] = Path to the vectors directory [OUTPUT]
						#argv[9] = Path to the file with the lsa value between words[OUTPUT]
						lsa.calc_lsa(ys.argv[4], sys.argv[8], sys.argv[9], sys.argv[10])

						#argv[2] = Path to the texts folder [INPUT]
						#argv[9] = Path to the file with the lsa value between words[INPUT]
						#argv[6] = Path to the output file with the specificity of each word [INPUT]
						similarity.calc_similarity(stextFolder+listFiles[i], textFolder+listFiles[j], sys.argv[10], sys.argv[7])