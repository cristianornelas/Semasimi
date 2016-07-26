import codecs

def remove_garbage(ignore, terms):
	
	#List with the POS that aren't relevant to semantic similarity
	CONDITIONS = ["N", "NPROP", "ADJ", "V", "PCP", "ADV", "ADV-KS", "ADV-KS-REL", "NUM"]
	cleaned_list = []

	#Store all the relevant terms from text into a list
	count = 0
	for x in terms:
		count += 1
		if count > ignore:
			aux = x.split("\t")
			aux1 = aux[1].split(" ")
			if aux1[0] in CONDITIONS:
				cleaned_list.append(aux[2].rstrip())

	return cleaned_list

def cross_texts(pText1, pText2, pOutput):

	FILE_TEXT1 = pText1
	FILE_TEXT2 = pText2
	FILE_OUTPUT = pOutput

	file1 = codecs.open(FILE_TEXT1, "r", "utf-8")
	file2 = codecs.open(FILE_TEXT2, "r", "utf-8")
	file3 = codecs.open(FILE_OUTPUT, "wb", "utf-8")

	content_file1 = file1.readlines()
	content_file2 = file2.readlines()

	#exclude the first seven elements cause they do not contribute in anything
	list1 = remove_garbage(7, content_file1)
	list2 = remove_garbage(7, content_file2)

	#Cross each term from text1 with all terms from text2
	for x in list1:
		for y in list2:
			file3.write(x + ": \n".encode("utf-8"))
			file3.write(y + ": \n".encode("utf-8"))
			file3.write(x + "_" + y + ":\n".encode("utf-8"))

	file1.close()
	file2.close()
	file3.close()