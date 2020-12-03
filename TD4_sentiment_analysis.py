# Hugo BERANGER - Thomas GAUCI - M2 MIAGE IA

# install nltk and SPARQLWrapper
import xml.etree.ElementTree as ET
import nltk
import re

tree = ET.parse('Restaurants_Train.xml')
root = tree.getroot()

# Extracting reviews and tokenizing them
reviews_raw = []
reviews_tokenized = []
reviews_tagged = []

# Data contenant les réponses des polarités
liste_reponses_aspectTerms = []
liste_reponses_aspectCategories = []
dataset = root.findall('.//sentence')
for sentences in dataset:
    question = sentences.find('text').text
    reviews_raw.append(question)

    token = nltk.word_tokenize(question)
    reviews_tokenized.append(token)

    tag = nltk.pos_tag(token)
    reviews_tagged.append(tag)
    for sentence in sentences:
        if(sentence.tag == "aspectTerms"):
            for aspectTerm in sentence:
                #On récupère les aspectTerms
                liste_reponses_aspectTerms.append([aspectTerm.attrib.get('term'),aspectTerm.attrib.get('polarity'),aspectTerm.attrib.get('from'),aspectTerm.attrib.get('to')])
        if(sentence.tag == "aspectCategories"):
            for aspectCategorie in sentence:
                #On récupère les aspectCategories
                liste_reponses_aspectCategories.append([aspectCategorie.attrib.get('category'),aspectCategorie.attrib.get('polarity')])
                

    #print(question)
    #print(token)
    #print(tag)

reviews_manually_tagged = [[[]]]
for x in range(0):
    to_append = [[]]
    for y in range(len(reviews_tagged[x])):
        couple = []
        negation = re.search("(\"|Not\\b|\\w+'t|no\\b|\")", reviews_tagged[x][y][0], re.IGNORECASE)
        if negation:
            print(reviews_tagged[x][y][0])
            #Ajoute le mot
            couple.append(reviews_tagged[x][y][0])
            #Ajoute son aspect
            couple.append("NEG")
        else:
            #Ajoute le mot
            couple.append(reviews_tagged[x][y][0])
            #Ajoute sa polarité (analyse avec sentiword si il est positif ou negatif)
            couple.append('')
        to_append.append(couple)
    reviews_manually_tagged.append(to_append)




        
        