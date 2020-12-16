# Hugo BERANGER - Thomas GAUCI - M2 MIAGE IA

# install nltk and SPARQLWrapper
import xml.etree.ElementTree as ET
import nltk
import re
from nltk.corpus import sentiwordnet as swn
#nltk.download('sentiwordnet')
#nltk.download('wordnet')

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
for x in range(2):
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
            pos = 0
            neg = 0
            #Ajoute sa polarité (analyse avec sentiword si il est positif ou negatif)
            if(reviews_tagged[x][y][1] == "NN" and len(list(swn.senti_synsets(couple[0],'n'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'n'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'n'))[0]).pos_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "VB" and len(list(swn.senti_synsets(couple[0],'v'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'v'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'v'))[0]).pos_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "JJ" and len(list(swn.senti_synsets(couple[0],'a'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'a'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'a'))[0]).pos_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "RB" and len(list(swn.senti_synsets(couple[0],'r'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'r'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'r'))[0]).pos_score() # score de polarité negatif du mot
            #print(couple[0] + " pos : " + str(pos) + " neg : " + str(neg))
            res = "none"
            if(pos > neg):
                res = "positive"
            if(pos < neg):
                res = "negative"
            if(pos == neg):
                res = "neutral"
            couple.append(res)
            
        to_append.append(couple)
    reviews_manually_tagged.append(to_append)

# Amélioration : Attention on doit juste chercher la polarité des aspects terms, on peut utiliser sentiword mais après faut regarder si devant il n'y a pas un terme négatif 

# Evaluation
totalAspectTerms = len(liste_reponses_aspectTerms)
justeAspectTerms = 0
for x in range(10):
    if(liste_reponses_aspectTerms[0] == "mot"):
        if(liste_reponses_aspectTerms[1] == "polarité"):
            justeAspectTerms += 1


        
        