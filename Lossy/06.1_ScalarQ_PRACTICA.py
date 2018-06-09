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

    Lvl = 2**k

    # Setup del array de niveles
    array = [ i*((n//Lvl) -1)    for i in range(0, Lvl)] ; array[0] = 0 ; array += [511] 
    
    i = 0
    for i in range(0, n):
        for j in range(0, n):
            pixel = imagenCuantizada[i][j]
            N = math.floor( (pixel* Lvl)/n ) 
            NewPixel = array[N]
            imagenCuantizada[i][j] = NewPixel

    Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)

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

block = np.array([[[]]])

for i in range(0, Nb):
    for j in range(0, Nb):
       for k in range(0, LS):
            line = imagenOriginal [i*LS] [ j*LS + k : j*LS + ((k+1)*LS)-1]
            line = np.expand_dims(np.expand_dims(line, 0), 0)
            #block[i][j] += 
            block = np.append(block, np.expand_dims(line, 0))

            #print(i, j, ' --> ', i*Nb, Nb*j,'..', ((j+1)*Nb)-1 )
            #print('\n')
        #print('\n')
        MIN = np.amin(block)
        MAX = np.amax(block)
    #print('\n')

# Calcular los nuevos puntos
#JUMP = 2**k
#for i in range (1, (n//JUMP)+1):
#Ini =  JUMP*(i-1)
#Fin = (JUMP*i)-1

#imagenParcial = imagenOriginal[Ini:Fin]
imagenCuantizada = misc.ascent()
'''
Min = amin(block)
Max = amax(block)
array = [ i*(n//k-1)    for i in range(0, 2)] ;     array[0] = 0
array += [Max]

i = 0
for i in range(0, n):
    for j in range(0, n):
        pixel = imagenCuantizada[i][j]
        N = math.floor( (pixel* k)/n ) 
        NewPixel = array[N]

        imagenCuantizada[i][j] = NewPixel
        #print(N, ':\t', p1, '-->\t', pixel)

    #print(i, 'Ite:', Ini, '\t', Fin, '\nArray =', imagenCuantizada,'\n\n')
Sigma = np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)
print(Sigma, 'ARRAY =', array, )


plt.subplot(330 + k-1)
plt.imshow(imagenCuantizada, cmap=plt.cm.gray)

    
plt.show() 



      
imagen3 = misc.ascent() #Leo la imagen
(n,m)=imagen3.shape # filas y columnas de la imagen
IMAGE = plt.imshow(imagen3, cmap=plt.cm.gray)

plt.imshow(imagen3, cmap=plt.cm.gray)

print("N = \n\n", n, '\n\n')
    
plt.show() 



'''

           
