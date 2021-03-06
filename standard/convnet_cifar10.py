# -*- coding: utf-8 -*-

""" Convolutional network applied to CIFAR-10 dataset classification task.

References:
    Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

Links:
    [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)

"""
from __future__ import division, print_function, absolute_import

import sys
#assert len(sys.argv) == 2, "needs output model name"
import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation

import os
# Data loading and preprocessing
from tflearn.datasets import cifar10
import numpy as np



(X, Y), (X_test, Y_test) = cifar10.load_data()
X, Y = shuffle(X, Y)
Y = to_categorical(Y, 10)
Y_test = to_categorical(Y_test, 10)

print (type(X))
print (type(Y))
print (X.shape)
print (Y.shape)
# Real-time data preprocessing
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

# Real-time data augmentation
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=15.)

# Convolutional network building
network = input_data(shape=[None, 32, 32, 3],
                     data_preprocessing=img_prep,
                     data_augmentation=img_aug)
network = conv_2d(network, 32, 3, activation='relu', name="conv_layer_1")
network = conv_2d(network, 64, 3, activation='relu', name="conv_layer_2")
network = max_pool_2d(network, 2)
network = conv_2d(network, 64, 3, activation='relu', name="conv_layer_3")
network = conv_2d(network, 32, 3, activation='relu', name="conv_layer_4")
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     #loss='mean_square',
                     learning_rate=0.0001)
print (network)
# Train using classifier

model = tflearn.DNN(network, tensorboard_verbose=0)
model.fit(X, Y, n_epoch=20, shuffle=True, validation_set=(X_test, Y_test),
          show_metric=True, batch_size=96, run_id='cifar10_cnn')
model.save("current_best_%s.tfl"%sys.argv[1])
