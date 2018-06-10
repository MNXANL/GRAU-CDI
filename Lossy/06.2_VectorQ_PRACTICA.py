# -*- coding: utf-8 -*-
"""

"""

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.cluster.vq import vq, kmeans

#%%
lena=scipy.misc.imread('./Images/lena_gray_512.png')
(n,m)=lena.shape # filas y columnas de la imagen
plt.figure()    
plt.imshow(lena, cmap=plt.cm.gray)
plt.show()





LenaPIC = misc.imread('./Images/lena_gray_512.png')
PeprPIC = misc.imread('./Images/peppers_gray.png')

#%%
   
"""
Usando K-means http://docs.scipy.org/doc/scipy/reference/cluster.vq.html
crear un diccionario cuyas palabras sean bloques 8x8 con 512 entradas 
para la imagen de Lena.

Dibujar el resultado de codificar Lena con dicho diccionario.

Calcular el error, la ratio de compresión y el número de bits por píxel
"""

def Blocking(img):
    (n, m) = img.shape

    BS =8
    BS2=64
    Blocks = np.zeros(( (n*m)//BS2, BS2 )) 

    for i in range(0, n, BS):
        for j in range(0, m, BS):

            Bloc = img[i:i + BS, j:j + BS]
            Blocks[int(i * n / (BS * BS) + j / BS), :] = np.reshape(Bloc, BS * BS)

    return Blocks


def callKmeans(path):
    img = misc.imread(path)
    (n, m) = img.shape
    convertedimg = img.astype(float)
    # bloques
    BS = 8
    bloques = np.zeros((int(n * m / (BS * BS)), BS * BS))
    print(len(bloques))
    for i in range(0, n, BS):
        for j in range(0, m, BS):
            bloque = img[i:i + BS, j:j + BS]
            bloques[int(i * n / (BS * BS) + j / BS), :] = np.reshape(bloque, BS * BS)

    '''kmeans cojera 512 imagenes 8x8. vq seleccionara para cada bloque 8x8, la que mejor se adapta'''
    code_book, d = kmeans(bloques, 512)
    # print(code_book[0])
    dicc, valores = vq(bloques, code_book)
    nBS = int(n / BS)
    for i in range(nBS * nBS):
        bloque = code_book[dicc[i]]
        for j in range(BS * BS):
            x = int(BS * int(i / nBS) + j / BS)
            y = int(j % BS + BS * int(i % nBS))
            img[x][y] = int(bloque[j])

    plt.imshow(img, cmap=plt.cm.gray)
    plt.xticks([])
    plt.yticks([])
    plt.show()




def K_means(img):
    (x, y) = img.shape
    BS =8
    BS2=64

    bloques = Blocking(img)

    codes, dc = kmeans(bloques, 512)

    dic, valores = vq(bloques, codes)
    NBS = (n // BS)
    for i in range(NBS * NBS):
        Bloc = codes[dic[i]]
        for j in range(BS * BS):
            px = BS * (i//NBS) + (j//BS)
            py = int((j & BS-1) + BS * (i & NBS-1))

            img[px][py] = int(Bloc[j])

    plt.imshow(img, cmap=plt.cm.gray)
    plt.xticks([])
    plt.yticks([])
    plt.show()


#callKmeans('Images/lena_gray_512.png')
#callKmeans('Images/peppers_gray.png')

#K_means(LenaPIC)
"""
Hacer lo mismo con la imagen Peppers (escala de grises)

http://atenea.upc.edu/mod/folder/view.php?id=1577653
http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip
"""

#K_means(PeprPIC)

"""
Dibujar el resultado de codificar Peppers con el diccionarios obtenido
con la imagen de Lena.

Calcular el error.
"""

LenaBlocks = Blocking(LenaPIC)
PeprBlocks = Blocking(PeprPIC)




(n, m) = PeprPIC.shape

lenaLibro, d = kmeans(LenaBlocks, 512)
dicc, valores = vq(PeprBlocks, lenaLibro)

BS = 8
nBS = int(n // BS)
for i in range(nBS * nBS):
    bloque = lenaLibro[dicc[i]]
    for j in range(BS * BS):
        x = (BS * (i // nBS) + j // BS)
        y = (j%BS + BS*(i % nBS))
        PeprPIC[x][y] = int(bloque[j])

plt.imshow(PeprPIC, cmap=plt.cm.gray)
plt.xticks([])
plt.yticks([])
plt.show()