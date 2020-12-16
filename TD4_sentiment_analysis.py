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
    aspectTerms = []
    for sentence in sentences:
        if(sentence.tag == "aspectTerms"):
            for aspectTerm in sentence:
                #On récupère les aspectTerms
                aspectTerms.append([aspectTerm.attrib.get('term'),aspectTerm.attrib.get('polarity'),aspectTerm.attrib.get('from'),aspectTerm.attrib.get('to')])
        if(sentence.tag == "aspectCategories"):
            for aspectCategorie in sentence:
                #On récupère les aspectCategories
                liste_reponses_aspectCategories.append([aspectCategorie.attrib.get('category'),aspectCategorie.attrib.get('polarity')])
    liste_reponses_aspectTerms.append(aspectTerms)
    #print(question)
    #print(token)
    #print(tag)
reviews_manually_tagged = [[[]]]
for x in range(50):
    to_append = [[]]
    for y in range(len(reviews_tagged[x])):
        couple = []
        negation = re.search("(\"|Not\\b|\\w+'t|no\\b|\")", reviews_tagged[x][y][0], re.IGNORECASE)
        if negation:
            #print(reviews_tagged[x][y][0])
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
                neg = (list(swn.senti_synsets(couple[0],'n'))[0]).neg_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "VB" and len(list(swn.senti_synsets(couple[0],'v'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'v'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'v'))[0]).neg_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "JJ" and len(list(swn.senti_synsets(couple[0],'a'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'a'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'a'))[0]).neg_score() # score de polarité negatif du mot
            elif(reviews_tagged[x][y][1] == "RB" and len(list(swn.senti_synsets(couple[0],'r'))) > 0):
                pos = (list(swn.senti_synsets(couple[0],'r'))[0]).pos_score() # score de polarité positif du mot
                neg = (list(swn.senti_synsets(couple[0],'r'))[0]).neg_score() # score de polarité negatif du mot
            #print(couple[0] + " pos : " + str(pos) + " neg : " + str(neg))
            res = 0
            res = pos-neg
            couple.append(res)
            
        to_append.append(couple)
    to_append.pop(0)
    reviews_manually_tagged.append(to_append)
reviews_manually_tagged.pop(0)


def polarity(phrase):
    res = 0
    for x in range(len(phrase)):
        if(phrase[x][1] != "NEG"):
            res += phrase[x][1]
    if(res > 0):
        return "positif"
    if(res < 0):
        return "negatif"
    if(res == 0):
        return "neutral"

def sentence_sections():
    ensemble_phrases = []
    # Itération sur les phrases
    for x in range(len(reviews_manually_tagged)):
        phrase = []
        section = []
        # Itération sur les mots
        for y in range(len(reviews_manually_tagged[x])):  
            if reviews_manually_tagged[x][y][0] == ",":
                # Analyse de la section de la phrase
                phrase.append(section)
                section = []
            elif reviews_manually_tagged[x][y][0] == ".":
                phrase.append(section)
                section = []
                ensemble_phrases.append(phrase)
            else:
                section.append(reviews_manually_tagged[x][y])
    return ensemble_phrases

sentences_section = sentence_sections()
for x in range(6):
    print(liste_reponses_aspectTerms[x])
# reponse = ["thomas","positif"]
#sentences_section = [[[["The",0],["staff",1]],[["doctor",0],["staff",-1]]],[[["coucou",0],["food",0]]]]
reponse = []
for x in range(len(sentences_section)):
    for k in range(len(liste_reponses_aspectTerms[x])):
        # On cherche l'aspect term dans le phrase 
        # La phrase est coupé en section
        if(len(sentences_section[x]) > 1):
            # Itération sur les sections de phrase
            for y in range(len(sentences_section[x])):
                # Itération sur les mots de la section de la phrase
                for w in range(len(sentences_section[x][y])):
                    if(liste_reponses_aspectTerms[x][k][0] == sentences_section[x][y][w][0]):
                        # On récupère la positivité de la phrase 
                        reponse.append([sentences_section[x][y][w][0],polarity(sentences_section[x][y])])
        else:
            # Itération sur les mots de la section de la phrase
            for w in range(len(sentences_section[x][0])):
                if(liste_reponses_aspectTerms[x][k][0] == sentences_section[x][0][w][0]):
                    # On récupère la positivité de la phrase 
                    reponse.append([sentences_section[x][0][w][0],polarity(sentences_section[x][0])])
print("reponse :")
print(reponse)

# Evaluation
totalAspectTerms = len(liste_reponses_aspectTerms)
justeAspectTerms = 0
for x in range(len(reponse)):
    for y in range(len(liste_reponses_aspectTerms[x])):
        if(liste_reponses_aspectTerms[x][y][0] == reponse[x][0]):
            if(liste_reponses_aspectTerms[x][y][1] == reponse[x][1]):
                justeAspectTerms += 1
print(justeAspectTerms)
print(totalAspectTerms)
print(len(dataset))
precision = justeAspectTerms / totalAspectTerms
rappel = justeAspectTerms / len(dataset)
print(rappel)
print(precision)
print("Résultat de l'évaluation : " + 2*((precision*rappel)/(precision+rappel)))
    


        
        