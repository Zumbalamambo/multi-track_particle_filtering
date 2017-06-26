# -*- coding: utf-8 -*-

__author__  = 'foresterd'
__date__    = '15 May 2017'

'''
clips the upper x-percential and the lower y-percentile values of a 2d numpy array.
'''

import numpy as np

def clip(in_image, lp = 0.5, up = 99.0):

    Img = in_image.copy()
    dtype = Img.dtype
    vmin = np.percentile(np.percentile(Img, lp, axis=0), lp).astype(dtype)
    vmax = np.percentile(np.percentile(Img, up, axis=0), up).astype(dtype)
    Img[Img<vmin] = vmin
    Img[Img>vmax] = vmax
    
    return Img