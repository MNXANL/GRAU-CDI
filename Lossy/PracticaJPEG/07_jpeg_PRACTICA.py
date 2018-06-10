# -*- coding: utf-8 -*-

import numpy as np
import scipy
import scipy.ndimage
import math 
import time 
pi=math.pi

import matplotlib.pyplot as plt
from scipy.fftpack import dct

        
"""
Matrices de cuantización, estándares y otras funciones auxiliares
"""

    
Q_Luminance=np.array([
[16 ,11, 10, 16,  24,  40,  51,  61],
[12, 12, 14, 19,  26,  58,  60,  55],
[14, 13, 16, 24,  40,  57,  69,  56],
[14, 17, 22, 29,  51,  87,  80,  62],
[18, 22, 37, 56,  68, 109, 103,  77],
[24, 35, 55, 64,  81, 104, 113,  92],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 99]])

Q_Chrominance=np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]])

def Q_matrix(r=1):
    m=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            m[i,j]=(1+i+j)*r
    return m


#############################################

def dct_matrix(x, y):
    # Aux calcs
    sqMin2 = 1/np.sqrt(2)
    sqInv = np.sqrt(2/x)
    DCT=np.zeros((x, y))
    for i in range(x):
        for j in range(y):
            cosine = np.cos(((2*j + 1)*i*pi)/ (2*x) )
            DCT[i][j] = sqInv * cosine
            if i == 0:
                DCT[i][j] *= sqMin2
    return DCT


def reshape(x, y, imagen):
    pos = 0
    newMat = np.zeros( ((x*y)//64, 8,8 ) )
    for i in range(0, y//8):
        for j in range(0, x//8):
            x1 = j*8 ; x2 = x1+8
            y1 = i*8 ; y2 = y1+8

            newMat[pos] = imagen[x1:x2, y1:y2].reshape(8, 8)
            pos = pos+1
    return newMat



def inv_reshape(x, y, imagen):
    pos = 0
    newMat = np.zeros((x, y))
    for i in range(0, y//8):
        for j in range(0, x//8):
            x1 = j*8 ; x2 = x1+8
            y1 = i*8 ; y2 = y1+8

            newMat[x1:x2, y1:y2] = imagen[pos]
            pos = pos+1
    return newMat



def SetMatrix(X, Y, imagen):

    #Reescalado directo a múltiplos de 8
    Xq = X + 8*((X&7)>0) -(X&7)
    Yq = Y + 8*((Y&7)>0) -(Y&7)
        
    imagen_clone     = np.zeros((Xq, Yq ))
    imagen_clone[:X, :Y] = imagen

    for it in range (Xq-X):
        imagen_clone[X+it] = imagen[-1]     


    imagen_new = np.zeros((Xq, Yq))
    imagen_new[:Xq, :Y] = imagen_clone

    for it in range (Yq-Y):
        imagen_new[:, Y+it] = imagen_clone[:, -1]      

    return imagen_new, Xq, Yq


def RGB_to_YCbCr(imagen): #, Xi, Yi):
    Xi, Yi, Zi = imagen.shape
    Y  = np.zeros((Xi, Yi))
    Cb = np.zeros((Xi, Yi))
    Cr = np.zeros((Xi, Yi))
    for i in range(Xi):
        for j in range(Yi):
            R = imagen[i, j, 0]
            G = imagen[i, j, 1]
            B = imagen[i, j, 2]

            ColY  = (75/256)*R + (150/256)*G + (29/256)*B
            ColCb = -(44/256)*R-(87/256)*G+(131/256)*B+128
            ColCr =  (131/256)*R-(110/256)*G-(21/256)*B+128

            Y [i, j]  = ColY
            Cb[i, j] = ColCb
            Cr[i, j] = ColCr
    return (Y, Cb, Cr)



"""
Implementar la DCT (Discrete Cosine Transform) 
y su inversa para bloques NxN

dct_bloque(p,N)
idct_bloque(p,N)

p bloque NxN

"""

def dct_bloque(p):
    x, y = p.shape
    c = dct_matrix(x, y)
    ct = np.transpose(c)
    return (np.tensordot(
        np.tensordot(c, p, axes=([1],[0])), ct, axes = ([1],[0]))
    )

def idct_bloque(p):
    x, y = p.shape
    c = dct_matrix(x, y)
    ct = np.transpose(c)
    RES = np.tensordot(np.tensordot(ct , p, axes=([1][0])), c, axes=([1][0]))
    return RES

    return (np.tensordot
        (np.tensordot(ct, p, axes=([1],[0])), c, axes = ([1],[0]))
    )






"""
Reproducir los bloques base de la transformación para los casos N=4,8
Ver imágenes adjuntas.
"""
def blockTransform():
    NList = [4, 8]
    for N in NList:
        Mat = dct_matrix(N, N)
        fig = plt.figure()

        for Row in range(N):
            for Col in range(N):
                MT = np.transpose(Mat[Col])
                img = np.tensordot(Mat[Row], MT, 0)

                fig.add_subplot(N, N,  Row*N + Col + 1 ).axis('off')
                plt.imshow(img) 
        plt.show()

    print('Sal de la ventana para continuar con el programa!') 


"""
Implementar la función jpeg_gris(imagen_gray) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen de grises 'imagen_gray' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error
Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))

"""

def jpeg_gris(imagen_gray):
    X, Y = imagen_gray.shape
    imagen_unsquared, Xq, Yq = SetMatrix(X, Y, imagen_gray)
    BlockImage = reshape(Xq, Yq, imagen_unsquared)
    

    print("    DCT")
    BlockImage -= 128

    NB = (Xq*Yq) // 64
    for i in range(NB):
        BlockImage[i] = dct_bloque(BlockImage[i])
    


    ImagenCuantizada = inv_reshape(X,Y,BlockImage)[:X][:Y]
    coef = X*Y
    coefNulo = (ImagenCuantizada == 0.00000).sum()
    CRatio = coef/(coef-coefNulo)
    

    print("    Cuantizacion")
    for i in range(NB):
        for j in range(8):
            for k in range(8):
                BlockImage[i, j, k] = BlockImage[i, j, k]//Q_Luminance[j, k]

    ImagenQ = inv_reshape(Xq, Yq, BlockImage)[:X][:Y]



    print("    Invertir cambios")
    for i in range(NB):
        BlockImage[i] = idct_bloque(BlockImage[i])



    Xq, Yq = imagen_unsquared.shape
    imagen_inv = inv_reshape(Xq, Yq, BlockImage)
    imagen_jpeg = imagen_inv[:X, :Y]
    
    print("    Mostrando")
    plt.imshow(imagen_jpeg, cmap=plt.cm.gray) 
    plt.xticks([])
    plt.yticks([])
    print('Sal de la ventana para continuar con el programa!')
    plt.show() 

    # Ratio compresion
    CoeficienteNulo = (0.0==ImagenQ).sum()
    Coeficientes = Xq*Yq
    Diff = Coeficientes-CoeficienteNulo
    Ratio = Coeficientes/Diff

    Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))
    print('\n\nSigma grises =>', Sigma, '\t| Ratio =>', Ratio)
    return imagen_gray

"""
Implementar la función jpeg_color(imagen_color) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen RGB 'imagen_color' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error para cada una de las componentes RGB
Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

"""
def jpeg_color(imagen_color):
    ## 1. RGB -> YCbCr
    X, Y, Col = imagen_color.shape


    print("    Conversion RGB -> YCbCr")
    (Yc, Cb, Cr) = RGB_to_YCbCr(imagen_color)

    

    print('    Division en bloques')
    ## 2. Div 8x8 + ajustes
    Matrix_Y  ,_ ,_ = SetMatrix(X, Y, Yc)
    Matrix_Cb ,_ ,_ = SetMatrix(X, Y, Cb)
    Matrix_Cr ,_ ,_ = SetMatrix(X, Y, Cr)
    Xq, Yq = Matrix_Y.shape



    Matrix_Y  = reshape(Xq, Yq, Matrix_Y)
    Matrix_Cb = reshape(Xq, Yq, Matrix_Cb)
    Matrix_Cr = reshape(Xq, Yq, Matrix_Cr)

    
    print("    DCT")
    Matrix_Y  -= 128
    Matrix_Cb -= 128
    Matrix_Cr -= 128

    NB = (Xq*Yq) // 64


    ## 3.2 Aplicacion DCT
    for i in range(NB):
        Matrix_Y[i]  = dct_bloque(Matrix_Y[i])
        Matrix_Cb[i] = dct_bloque(Matrix_Cb[i])
        Matrix_Cr[i] = dct_bloque(Matrix_Cr[i])

    

    
    print("    Cuantizacion")
    for i in range(NB):
        for j in range(8):
            for k in range(8):
                Matrix_Y[i, j, k]  = Matrix_Y[i, j, k]//Q_Luminance[j, k]
                Matrix_Cb[i, j, k] = Matrix_Cb[i, j, k]//Q_matrix()[j, k]
                Matrix_Cr[i, j, k] = Matrix_Cr[i, j, k]//Q_Chrominance[j, k]
    
    


    # Ratio compresion (coeficientes)
    CoeficienteNulo = (0.0==Matrix_Y).sum() + (0.0==Matrix_Cb).sum() + (0.0==Matrix_Cr).sum()
    Coeficientes = X*Y*Col
    
    



    
    print("    Invertir cambios")
    for i in range(NB):
        Matrix_Y[i]  = idct_bloque(Matrix_Y[i])
        Matrix_Cb[i] = idct_bloque(Matrix_Cb[i])
        Matrix_Cr[i] = idct_bloque(Matrix_Cr[i])



    imagen_jpeg = np.zeros((X, Y, Col))
    for i in range(X):
        for j in range(Y):
            Yx  = Yc[i][j]  ;  Cbx = Cb[i][j]  ;  Crx = Cr[i][j]

            Col_R = Yx+(1.371*(Crx-128))
            Col_G = Yx-(0.698*(Crx-128))-(0.336*(Cbx-128))
            Col_B = Yx+(1.732*(Cbx-128))

            imagen_jpeg[i][j][0] = Col_R
            imagen_jpeg[i][j][1] = Col_G
            imagen_jpeg[i][j][2] = Col_B



    
    ## 6. Epilogo: mostrar resultado + sigma
    print("    Mostrando")
    plt.imshow(imagen_jpeg.astype(np.uint8))
    plt.xticks([])
    plt.yticks([])
    print('Sal de la ventana para acabar el programa!')
    plt.show() 


    # Ratio compresion (calculo)
    Diff  = Coeficientes-CoeficienteNulo
    Ratio = Coeficientes/Diff

    Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))
    print('\n\nSigma colour =>', sum(Sigma[0:2]), '\t| Ratio =>', Ratio)
    
    return imagen_jpeg



###########################################################################
###########################################################################


"""
#--------------------------------------------------------------------------
Transformacion de BLOQUES
#--------------------------------------------------------------------------
"""

print("TRANSFORMACION POR BLOQUES")
blockTransform()


"""
#--------------------------------------------------------------------------
Imagen de GRISES
#--------------------------------------------------------------------------
"""


### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al 
### restar 128 puede devolver un valor positivo mayor que 128

print("\n\nIMAGEN DE GRISES")
mandril_gray=scipy.ndimage.imread('./mandril_gray.png').astype(np.int32)

start= time.clock()
mandril_jpeg=jpeg_gris(mandril_gray)
end= time.clock()
print("tiempo",(end-start))


"""
#--------------------------------------------------------------------------
Imagen COLOR
#--------------------------------------------------------------------------
"""
## Aplico.astype pero después lo convertiré a 
## uint8 para dibujar y a int64 para calcular el error

print("\n\nIMAGEN DE COLORES")
mandril_color=scipy.misc.imread('./mandril_color.png').astype(np.int32)



start= time.clock()
mandril_jpeg=jpeg_color(mandril_color)     
end= time.clock()
print("tiempo",(end-start))

