import cv2
from model import load_model
import numpy as np 
from scipy.misc import imresize
from test import mean_squared_loss
from keras.models import load_model
import argparse


rval=True
print('Loading model')
model=load_model('AnomalyDetector.h5')
print('Model loaded')
# vc=cv2.VideoCapture(0)
threshold=0.0006

def check_for_anomalies(vc):
    
    imagedump=[]

    for i in range(10):
        rval,frame=vc.read()
        frame=imresize(frame,(227,227,3))

        #Convert the Image to Grayscale


        gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
        gray=(gray-gray.mean())/gray.std()
        gray=np.clip(gray,0,1)
        imagedump.append(gray)


    imagedump=np.array(imagedump)

    imagedump.resize(227,227,10)
    imagedump=np.expand_dims(imagedump,axis=0)
    imagedump=np.expand_dims(imagedump,axis=4)

    output=model.predict(imagedump)



    loss=mean_squared_loss(imagedump,output)


    if loss>threshold:
        result = 'Anomalies Detected'
    else:
        result = 'No Anomalies'
    
    return result


