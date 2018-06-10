# -*- coding: utf-8 -*-

from scipy import misc
import numpy as np
import math
import matplotlib.pyplot as plt


import scipy.ndimage
from scipy.cluster.vq import vq, kmeans

#%%
imagen = misc.ascent() #Leo la imagen
(n,m)=imagen.shape # filas y columnas de la imagen
plt.imshow(imagen, cmap=plt.cm.gray) 
plt.xticks([])
plt.yticks([])



























"""
Mostrar la imagen habiendo cuantizado los valores de los píxeles en
2**k niveles, k=1..8

Para cada cuantización dar la ratio de compresión y Sigma

Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)
"""

imagenOriginal = misc.ascent() #Leo la imagen
(n,m)=imagenOriginal.shape # filas y columnas de la imagen
    #imagenCuantizada = plt.imshow(imagenOriginal, cmap=plt.cm.gray)
    

# Line sizes 
LS = n//8

# Marcar los puntos 
Nb = n//LS # n block
Mb = m//LS

XT, XL = plt.xticks(np.arange(0, n, step = Nb))
YT, YL = plt.yticks(np.arange(0, m, step = Mb))

block = []
imagenCuantizada = misc.ascent()
#for i in range(0, Nb):
#    for j in range(0, Nb):
for ii in range(0, Nb):
    for jj in range(0, Nb):
        for kk in range(0, LS):
            line = imagenCuantizada[ii*LS][ jj*LS + kk : jj*LS + ((kk+1)*LS)-1]
            
            linelist = line.tolist()
            #print(i*LS,'|',   j*LS + kk, ' -> ', j*LS , ((j+1)*LS)-1)
            #block[i][j] += 
            block += [linelist]
        res = np.array(block)
        MIN = np.amin(res)
        MAX = np.amax(res)

        Lvl = 2**4
        array = [ i*((n//Lvl) -1)    for i in range(0, Lvl)] ; array[0] = 0 ; array += [511] 
        print( len(block), array    )
        #print( block )
        for i in range(0, Nb):
            for j in range(0, Nb):
                pixel = block[i][j]
                N = math.floor( (pixel* Lvl)/n )

                NewPixel = array[N]
                imagenCuantizada[i*LS][j*LS] = NewPixel
        print('------------------------------')
        #print(i, j, ' --> ', i*Nb, Nb*j,'..', ((j+1)*Nb)-1 )
        #print('\n')
        #print('\n')
    #print('\n')

plt.subplot(121), plt.imshow(imagenOriginal,   cmap=plt.cm.gray)
plt.subplot(122), plt.imshow(imagenCuantizada, cmap=plt.cm.gray)
plt.show() 

Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)
print('Sigma for k=4 ->', Sigma)