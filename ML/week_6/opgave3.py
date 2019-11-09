import tensorflow as tf 
import numpy as np
import os
from tensorflow import keras


# we are using an DataImageGenerator instance to use the Fundus data in our model
datagen = keras.ImageDataGenerator()
datagen.flow_from_directory("Fundus-data") 

 # load datasets
 X, y = np.load(os.listdir("Fundus-data"))
# preprocessing images in fundus-data folder 
for data_sets in os.listdir("Fundus-data"):
