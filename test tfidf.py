from math import *
from nltk.corpus import stopwords


def calculer_tf(documents):
    tf = []
    df = {}
    sw = stopwords.words('english')
    cur_index = 0
    for document in documents:
        tf.append({})
        for mot in document:
            if mot in tf[cur_index] and mot not in sw:
                tf[cur_index][mot] = tf[cur_index][mot] + 1
            elif mot not in sw:
                tf[cur_index][mot] = 1
                if mot in df:
                    df[mot] += 1
                else:
                    df[mot] = 1
            
        cur_index += 1
    return tf, df


def calculer_idf(documents,df):
    idf = {}
    for mot in df:
        #Ajout de 1 pour éviter le 0
        idf[mot] = 1 + log(len(documents) / df[mot],2)
    return idf

def calculer_tf_idf(tf,idf):
    tfidf = []
    for i in range(0,len(tf)):
        tfidf.append({})
        for mot in tf[i]:
            tfidf[i][mot] = tf[i][mot]*idf[mot]
    return tfidf

test = ["Je suis Jonathan j'adore le football je soutiens le Brésil","Jonathan aime le Brésil et regarde les matchs du Brésil",
"Jonathan aime l'Allemagne mais Jonathan ne regarde pas les matchs de l'Allemagne",
"le Brésil joue contre le Brésil Jonathan ne sait pas qui il doit soutenir"]

test = ["I am Jonathan I like football I support Brazil","Jonathan likes Brazil and watches Brazil 's matches",
"Jonathan likes Germany but Jonathan does not watch Germany 's matches",
"Brazil plays against Brazil Jonathan does not know who Jonathan must support"]

i = 0
while i < len(test): 
    test[i] = test[i].split(" ")
    i += 1

#print(test)
print("tf")
print(calculer_tf(test)[0])
print("df")
print(calculer_tf(test)[1])
print("idf")
print(calculer_idf(test,calculer_tf(test)[1]))
print("tf*idf")
print(calculer_tf_idf(calculer_tf(test)[0],calculer_idf(test,calculer_tf(test)[1])))
