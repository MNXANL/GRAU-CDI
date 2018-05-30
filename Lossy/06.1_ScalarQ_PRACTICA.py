# -*- coding: utf-8 -*-

from scipy import misc
import numpy as np
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

Sigma=np.sqrt(sum(sum((imagenOriginal-imagenCuantizada)**2)))/(n*m)

"""
imagen2 = misc.ascent() #Leo la imagen
(n,m)=imagen2.shape # filas y columnas de la imagen
for k in range(1, 8):
    IMAGE = plt.imshow(imagen2, cmap=plt.cm.gray)
    
    # Marcar los puntos 
    XT, XL = plt.xticks(np.arange(0, n, step=2**k))
    YT, YL = plt.yticks(np.arange(0, m, step=2**k))
    
    # Calcular los nuevos puntos
    #for i in range (0, n*m):
        
    plt.subplot(331 + k)
    plt.imshow(imagen2, cmap=plt.cm.gray)
    
    print("N = \n\n", n, '\n\n')
    
plt.show() 



#%%
'''
Mostrar la imagen cuantizando los valores de los pixeles de cada bloque
n_bloque x n_bloque en 2^k niveles, siendo n_bloque=8 y k=2

Calcular Sigma y la ratio de compresión (para cada bloque 
es necesario guardar 16 bits extra para los valores máximos 
y mínimos del bloque, esto supone 16/n_bloque**2 bits más por pixel).

'''


      
imagen3 = misc.ascent() #Leo la imagen
(n,m)=imagen3.shape # filas y columnas de la imagen
IMAGE = plt.imshow(imagen3, cmap=plt.cm.gray)

# Marcar los puntos 
Nb = n/4 # n block
Mb = m/4
XT, XL = plt.xticks(np.arange(0, n, step = Nb))
YT, YL = plt.yticks(np.arange(0, m, step = Mb))

for i in range(0, 4):
    for j in range(0, 4):
        print('Hi')

plt.imshow(imagen3, cmap=plt.cm.gray)

print("N = \n\n", n, '\n\n')
    
plt.show() 





           
