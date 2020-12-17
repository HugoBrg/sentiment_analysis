# TLN

Ecriture d'un petit programme qui obtien la polarité des aspects terms en fonction de la phrase

# Commentaires
Nous avons choisi la solution de découper les phrases afin d'obtenir les polarités des sections de phrase. 
Cette solution est intéréssante mais nous avons un gros problème qui est la syntaxe du texte dans le xml. Nous sommes assez sensible à la typographie et une phrase trop spécifique nous provoque un bug dans notre programme. Nous avons réussi seulement sur l'ensemble restaurant_train en modifiant certains textes du xml. Sans cela notre soucis est que nos listes d'aspect terms sont décalés l'une en fonction de l'autre lorsqu'on vérifie notre liste d'aspect terms avec la réponse des polarités. 

# Lancement 
```bash
git clone https://github.com/HugoBrg/sentiment_analysis
cd /sentiment_analysis
python3 TD4_sentiment_analysis.py
```

# Librairies 
 - https://docs.python.org/3/library/xml.etree.elementtree.html
 - https://pypi.org/project/nltk/

