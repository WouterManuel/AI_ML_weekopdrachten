import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras

# OPGAVE 1a
def plotImage(img, label):
    # Deze methode krijgt een matrix mee (in img) en een label dat correspondeert met het 
    # plaatje dat in de matrix is weergegeven. Zorg ervoor dat dit grafisch wordt weergegeven.
    # Maak gebruik van plt.cm.binary voor de cmap-parameter van plt.imgshow.

    plt.xlabel(label)
    plt.imshow(img, cmap=plt.cm.binary)
    plt.show()

# OPGAVE 1b
def scaleData(X):
    # Deze methode krijgt een matrix mee waarin getallen zijn opgeslagen van 0..m, en hij 
    # moet dezelfde matrix retourneren met waarden van 0..1. Deze methode moet werken voor 
    # alle maximal waarde die in de matrix voorkomt.
    # Deel alle elementen in de matrix 'element wise' door de grootste waarde in deze matrix.

    return X/np.amax(X)

# OPGAVE 1c
def buildModel():
    # Deze methode maakt het keras-model dat we gebruiken voor de classificatie van de mnist
    # dataset. Je hoeft deze niet abstract te maken, dus je kunt er van uitgaan dat de input
    # layer van dit netwerk alleen geschikt is voor de plaatjes in de opgave (wat is de 
    # dimensionaliteit hiervan?).
    # Maak een model met een input-laag, een volledig verbonden verborgen laag en een softmax
    # output-laag. Compileer het netwerk vervolgens met de gegevens die in opgave gegeven zijn
    # en retourneer het resultaat.

    model = keras.Sequential()
    # input laag
    model.add(keras.layers.Flatten(input_shape=(28,28)))

    # hidden layer
    model.add(keras.layers.Dense(128, activation='relu'))

    # output layer
    model.add(keras.layers.Dense(10, activation='softmax')) 
    
    # tijd om te compileren 
    model.compile(loss=keras.losses.sparse_categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
    return model


# OPGAVE 2a
def confMatrix(labels, pred):
    # Retourneer de econfusion matrix op basis van de gegeven voorspelling (pred) en de actuele
    # waarden (labels). Check de documentatie van tf.math.confusion_matrix

    return tf.math.confusion_matrix(labels, pred, num_classes=10)

# OPGAVE 2b
def confEls(conf, labels): 
    # Deze methode krijgt een confusion matrix mee (conf) en een set van labels. Als het goed is, is 
    # de dimensionaliteit van de matrix gelijk aan len(labels) × len(labels) (waarom?). Bereken de 
    # waarden van de TP, FP, FN en TN conform de berekening in de opgave. Maak vervolgens gebruik van
    # de methodes zip() en list() om een list van len(labels) te retourneren, waarbij elke tupel 
    # als volgt is gedefinieerd:
    #     (categorie:string, tp:int, fp:int, fn:int, tn:int)
    # Check de documentatie van numpy diagonal om de eerste waarde te bepalen.
    
    resultList = list()

    # alle true positives in de confusion matrix 
    tp = np.diagonal(conf)

    for i in range(len(labels)):
        tp_i = tp[i]
        fp_i = sum(conf[:, i].numpy() - tp_i)
        fn_i = sum(conf[i, :].numpy() - tp_i)
        tn_i = sum(sum(conf.numpy() -  tp_i - fp_i - fn_i))

        resultList.append((labels[i], tp_i, fp_i, fn_i, tn_i))
    
    return resultList 

# OPGAVE 2c
def confData(metrics):
    # Deze methode krijgt de lijst mee die je in de vorige opgave hebt gemaakt (dus met lengte len(labels))
    # Maak gebruik van een list-comprehension om de totale tp, fp, fn, en tn te berekenen en 
    # bepaal vervolgens de metrieken die in de opgave genoemd zijn. Retourneer deze waarden in de
    # vorm van een dictionary (de scaffold hiervan is gegeven).

    # VERVANG ONDERSTAANDE REGELS MET JE EIGEN CODE
    
    tp = sum([n[1] for n in metrics])
    fp = sum([n[2] for n in metrics])
    fn = sum([n[3] for n in metrics])
    tn = sum([n[4] for n in metrics])

    print(tp, fp, fn, tn)

    # BEREKEN HIERONDER DE JUISTE METRIEKEN EN RETOURNEER DIE 
    # ALS EEN DICTIONARY
    rv = {'tpr':0, 'ppv':0, 'tnr':0, 'fpr':0 }

    # true positive rate : zegt iets over de verhouding tussen correct geclassificeerde kledingstukken
    # en het totaal aantal kledingstukken dat tot die klasse behoren
    rv['tpr'] = tp/(tp+fn)
    
    # positive predictive value: hoeveel van de voorspelde kledingstukken ook daadwerkelijk 
    # hetgene is wat het model beweert
    rv['ppv'] = tp/(tp+fp)

    # true negative rate: verhouding tussen foutief geclassificeerde kledingstukken van het totaal
    rv['tnr'] = tn/(tn+fp)

    # false positive rate: verhouding tussen positief geclassificeerde kledingstukken van het totaal
    rv['fpr'] = fp/(fp+tn)

    return rv
