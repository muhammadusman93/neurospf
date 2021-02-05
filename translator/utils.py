from keras import *
from keras import backend as K
import numpy as np
from PIL import Image
import copy
import sys
import cv2


the_dec_pos=0
MIN=-100000
DIM=50
#ssc_ratio=0.005 #0.1 #0.05 #0.01

## some DNN model has an explicit input layer
def is_input_layer(layer):
  return str(layer).find('InputLayer')>=0

def is_conv_layer(layer):
  return str(layer).find('conv')>=0 or str(layer).find('Conv')>=0

def is_dense_layer(layer):
  return str(layer).find('dense')>=0 or str(layer).find('Dense')>=0

def is_activation_layer(layer):
  return str(layer).find('activation')>=0 or str(layer).find('Activation')>=0

def act_in_the_layer(layer):
  try:
    act=str(layer.activation)
    if act.find('relu')>=0: return 'relu'
    elif act.find('softmax')>=0: return 'softmax'
    else: return ''
  except:
    return ''

def is_maxpooling_layer(layer):
  return str(layer).find('MaxPooling')>=0 

def is_flatten_layer(layer):
  return str(layer).find('flatten')>=0 or str(layer).find('Flatten')>=0

def is_dropout_layer(layer):
  return False ## we do not allow dropout

def get_activation(layer):
  if str(layer.activation).find('relu')>=0: return 'relu'
  elif  str(layer.activation).find('linear')>=0: return 'linear'
  elif  str(layer.activation).find('softmax')>=0: return 'softmax'
  else: return ''

