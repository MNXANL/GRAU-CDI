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
plt.show() 
        
"""
Mostrar la imagen habiendo cuantizado los valores de los píxeles en
2**k niveles, k=1..8

Para cada cuantización dar la ratio de compresión y Sigma

Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)
"""




imagenOriginal = misc.ascent() #Leo la imagen
(n,m)=imagenOriginal.shape # filas y columnas de la imagen
for k in range(2, 9):
    #imagenCuantizada = plt.imshow(imagenOriginal, cmap=plt.cm.gray)
    
    # Marcar los puntos 
    XT, XL = plt.xticks(np.arange(0, n, step=2**k))
    YT, YL = plt.yticks(np.arange(0, m, step=2**k))
    
    # Calcular los nuevos puntos
    #JUMP = 2**k
    #for i in range (1, (n//JUMP)+1):
    #Ini =  JUMP*(i-1)
    #Fin = (JUMP*i)-1

    #imagenParcial = imagenOriginal[Ini:Fin]
    imagenCuantizada = misc.ascent()


    # Setup del array de niveles
    Lvl = 2**k
    array = [ i*((n//Lvl) -1)    for i in range(0, Lvl)] ; array[0] = 0 ; array += [511] 
    
    
    for i in range(0, n):
        for j in range(0, n):
            pixel = imagenCuantizada[i][j]
            N = math.floor( (pixel* Lvl)/n ) 
            NewPixel = array[N]
            imagenCuantizada[i][j] = NewPixel

    Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)
    print('Sigma for k =', k, "->", Sigma)
    plt.subplot(330 + k-1)
    plt.imshow(imagenCuantizada, cmap=plt.cm.gray)
    
    
plt.show() 



#%%
'''
Mostrar la imagen cuantizando los valores de los pixeles de cada bloque
[N_Bloque x N_Bloque] en 2^k niveles, siendo n_bloque=8 y k=2

Calcular Sigma y la ratio de compresión (para cada bloque 
es necesario guardar 16 bits extra para los valores máximos 
y mínimos del bloque, esto supone 16/n_bloque**2 bits más por pixel).

'''

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