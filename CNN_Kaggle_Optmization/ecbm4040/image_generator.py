#!/usr/bin/env/ python
# ECBM E4040 Fall 2017 Assignment 2
# This Python script contains the ImageGenrator class.

import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.interpolation import rotate


class ImageGenerator(object):
    def __init__(self, x, y,img_size = 32):
        """
        Initialize an ImageGenerator instance.
        :param x: A Numpy array of input data. It has shape (num_of_samples, height, width, channels).
        :param y: A Numpy vector of labels. It has shape (num_of_samples, ).
        """

        # TODO: Your ImageGenerator instance has to store the following information:
        # x, y, num_of_samples, height, width, number of pixels translated, degree of rotation, is_horizontal_flip,
        # is_vertical_flip, is_add_noise. By default, set boolean values to False.
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        self.x=x
        self.y=y
        self.sam,self.h,self.w,self.c=x.shape
        self.angle=0
        self.is_horizontal_flip=0
        self.is_vertical_flip=0
        self.is_add_noise=0
        self.num_pixels=0
    def next_batch_gen(self, batch_size, shuffle=True):
        """
        A python generator function that yields a batch of data indefinitely.
        :param batch_size: The number of samples to return for each batch.
        :param shuffle: If True, shuffle the entire dataset after every sample has been returned once.
                        If False, the order or data samples stays the same.
        :return: A batch of data with size (batch_size, width, height, channels).
        """

        # TODO: Use 'yield' keyword, implement this generator. Pay attention to the following:
        # 1. The generator should return batches endlessly.
        # 2. Make sure the shuffle only happens after each sample has been visited once. Otherwise some samples might
        # not be output.

        # One possible pseudo code for your reference:
        ########################################################################
        #   calculate the total number of batches possible (if the rest is not sufficient to make up a batch, ignore)
        #   while True:
        #       if (batch_count < total number of batches possible):
        #           batch_count = batch_count + 1
        #           yield(next batch of x and y indicated by batch_count)
        #       else:
        #           shuffle(x)
        #           reset batch_count
        
        
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        batch_cnt=self.sam/batch_size
        
        batch_cnt_temp=0
        while True:
            if(batch_cnt_temp<batch_cnt):
                batch_cnt_temp+=1
                yield(self.x[batch_cnt_temp*batch_size:(batch_cnt_temp+1)*batch_size],self.y[batch_cnt_temp*batch_size:(batch_cnt_temp+1)*batch_size])
            else:
                np.random.shuffle(self.x)
                np.random.shuffle(self.y)
                batch_cnt=self.sam/batch_size
        
                batch_cnt_temp=0
                      

    def show(self):
        """
        Plot the top 16 images (index 0~15) of self.x for visualization.
        """
        #raise NotImplementedError
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        r = 4
        img_li=[]
        for i in range(16):
            img_li.append(self.x[i,:,:,:])
        f, axarr = plt.subplots(r,r,figsize=(8,8))
        for i in range(r):
            for j in range(r):
                img = img_li[r*i+j]
                axarr[i][j].imshow(img)

    def translate(self, shift_height, shift_width):
        """
        Translate self.x by the values given in shift.
        :param shift_height: the number of pixels to shift along height direction. Can be negative.
        :param shift_width: the number of pixels to shift along width direction. Can be negative.
        :return:
        """

        # TODO: Implement the translate function. Remember to record the value of the number of pixels translated.
        # Note: You may wonder what values to append to the edge after the translation. Here, use rolling instead. For
        # example, if you translate 3 pixels to the left, append the left-most 3 columns that are out of boundary to the
        # right edge of the picture.
        # Hint: Numpy.roll (https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.roll.html)
        #raise NotImplementedError
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        
        self.x=np.roll(self.x,shift_height,axis=2)
        self.x=np.roll(self.x,shift_width,axis=1)

        self.num_pixels=shift_height+shift_width

    def rotate(self, angle=0.0):
        """
        Rotate self.x by the angles (in degree) given.
        :param angle: Rotation angle in degrees.
        
        - https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.ndimage.interpolation.rotate.html
        """
        # TODO: Implement the rotate function. Remember to record the value of rotation degree.
        #raise NotImplementedError
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        self.x=rotate(self.x,angle,axes=(1,2),reshape=False)
        self.angle=angle

    def flip(self, mode='h'):
        """
        Flip self.x according to the mode specified
        :param mode: 'h' or 'v' or 'hv'. 'h' means horizontal and 'v' means vertical.
        """
        # TODO: Implement the flip function. Remember to record the boolean values is_horizontal_flip and
        # is_vertical_flip.
        #raise NotImplementedError
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        if(mode=="h"):
            dire=1
            self.is_horizontal_flip=1
            self.x=np.flip(self.x,dire)
        elif(mode=="v"):
            dire=2
            self.is_vertical_flip=1
            self.x=np.flip(self.x,dire)
        elif(mode=="both"):
            self.is_vertical_flip=1
            self.is_horizontal_flip=1
            self.x=np.flip(self.x,1)
            self.x=np.flip(self.x,2)
             
        
        
        
    def add_noise(self, portion, amplitude):
        """
        Add random integer noise to self.x.
        :param portion: The portion of self.x samples to inject noise. If x contains 10000 sample and portion = 0.1,
                        then 1000 samples will be noise-injected.
        :param amplitude: An integer scaling factor of the noise.
        """
        # TODO: Implement the add_noise function. Remember to record the boolean value is_add_noise. Any noise function
        # is acceptable.
        #raise NotImplementedError
        #######################################################################
        #                                                                     #
        #                                                                     #
        #                         TODO: YOUR CODE HERE                        #
        #                                                                     #
        #                                                                     #
        #######################################################################
        temp=int(self.sam*portion)
        
        noise=np.random.normal(0,amplitude,(temp,self.h,self.w,self.c))
        
       
        temp_1=np.arange(self.sam)
        self.x[temp_1[:temp]]=self.x[temp_1[:temp]]+noise
        self.is_add_noise=1
        
        
