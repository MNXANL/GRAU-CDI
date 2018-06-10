# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import scipy
from scipy.fftpack import dct
import scipy.ndimage
import math
import time 
pi=math.pi




import matplotlib.pyplot as plt




        
"""
Matrices de cuantización, estándares y otras
"""

    
Q_Luminance=np.array([
[16 ,11, 10, 16, 124, 140, 151, 161],
[12, 12, 14, 19, 126, 158, 160, 155],
[14, 13, 16, 24, 140, 157, 169, 156],
[14, 17, 22, 29, 151, 187, 180, 162],
[18, 22, 37, 56, 168, 109, 103, 177],
[24, 35, 55, 64, 181, 104, 113, 192],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 199]])

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
    Xq=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            Xq[i,j]=(1+i+j)*r
    return Xq

"""
Implementar la DCT (Discrete Cosine Transform) 
y su inversa para bloques NxN

dct_bloque(p,N)
idct_bloque(p,N)

p bloque NxN

"""
def getC(Xq,Yq):
    N = Xq
    C = np.zeros((Xq,Yq))
    for i in range(Xq):
        for j in range(Yq):
                aux1 = np.sqrt(2/N)
                aux2=(2*j+1)*i*pi
                aux2 /= (2*N)
                aux2 = np.cos(aux2)
                if(i==0): C[i,j]=aux1*aux2*(1/np.sqrt(2))
                else:C[i,j]=aux1*aux2
    return C
            
def dct_bloque(p):
    Xq,Yq=p.shape
    C = getC(Xq,Yq)
    Yq = np.tensordot(np.tensordot(C,p,axes=([1][0])),np.transpose(C),axes=([1][0]))
    return Yq
    
def idct_bloque(p):
    Xq,Yq=p.shape
    C=getC(Xq,Yq)
    Yq = np.tensordot(np.tensordot(np.transpose(C),p,axes=([1][0])),C,axes=([1][0]))
    return Yq
    

"""
Reproducir los bloques base de la transformación para los casos N=4,8
Ver imágenes adjuntas.
"""


"""
Implementar la función jpeg_gris(imagen_gray) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen de grises 'imagen_gray' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error
Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


En este caso optimizar la DCT 
http://docs.scipy.org/doc/numpy-1.10.1/reference/routines.linalg.html
"""

def reshape1(Xq,Yq,image):
    res = np.zeros(((Xq*Yq)//64,8,8))
    z=0
    for n1 in range(int(Yq/8)):
        for n2 in range(int(Xq/8)):      
            bx1=n2*8
            bx2=bx1+8
            bz1=n1*8
            bz2=bz1+8
            res[z]= image[bx1:bx2,bz1:bz2].reshape(8,8)
            z+=1
    return res

def reshape2(Xq,Yq,image):
    res = np.zeros((Xq,Yq))
    z=0
    for n1 in range(int(Yq/8)):
        for n2 in range(int(Xq/8)):
            bx1=n2*8
            bx2=bx1+8
            bz1=n1*8
            bz2=bz1+8
            res[bx1:bx2,bz1:bz2] = image[z]
            z+=1
    return res

def jpeg_gris(imagen_gray):
    #Paso 1 no es necesario. Pixel=Y
    #Paso 2: Ajustar el tamaño de la imagen y dividir en bloques 8x8
    OrigM,OrigN = imagen_gray.shape
    Xq = OrigM
    Yq= OrigN
    if OrigM%8!=0:Xq+= 8-(OrigM%8)
    if OrigN%8!=0: Yq+=8-(OrigN%8)
    imagen_reshaped = np.zeros((Xq,Yq))
    aux1 = np.zeros((Xq,OrigN))
    aux1[:OrigM,:OrigN] = imagen_gray
    for i in range(Xq-OrigM):
        aux1[OrigM+i]=imagen_gray[-1]

    imagen_reshaped[:Xq,:OrigN]=aux1
    for j in range(Yq-OrigN):
        imagen_reshaped[:,OrigN+j]= aux1[:,-1]

    ImageInBlocs = reshape1(Xq,Yq,imagen_reshaped)
            
    #Paso 3: Se desplaza la imagen 128 y se aplica DCT sobre los bloques de la imagen
    ImageInBlocs -= 128
    numBloc=int((Xq*Yq)/(8*8))
    for i in range(numBloc):
        ImageInBlocs[i]=dct_bloque(ImageInBlocs[i])
        
    #Paso 4: Se cuantizan los valores de los bloques
    for i in range(numBloc):
        for w in range(8):
            for z in range(8):
                ImageInBlocs[i,w,z] /= Q_Luminance[w,z]
                ImageInBlocs[i,w,z] = round(ImageInBlocs[i,w,z],0)
                
    #Compresion ratio:
    ImagenCuantizada = reshape2(Xq,Yq,ImageInBlocs)[:OrigM,:OrigN]
    coef = Xq*Yq
    coefNul= (ImagenCuantizada == 0.).sum()
    CRatio = coef/(coef-coefNul)
    
    
    #Reversion de los cambios hechos sobre la imagen
    #Paso 1: Se aplica iDCT a los bloques de la imagen
    for i in range(numBloc):
        ImageInBlocs[i] = idct_bloque(ImageInBlocs[i])
        
    #Paso 2: Reshape de la imagen cuantizada
    Xq,Yq = imagen_reshaped.shape
    imagenInv = reshape2(Xq,Yq,ImageInBlocs)
    
    #Paso 3: eliminar las filas y columnas de más
    imagen_jpeg = imagenInv[:OrigM,:OrigN]
    
    #Pintar imagen
    plt.imshow(imagen_jpeg, cmap=plt.cm.gray) 
    plt.xticks([])
    plt.yticks([])
    plt.show() 
    
    #Calcular error:
    Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))
    print("Error for gray image:",Sigma)
    print("Compression ratio for gray image:",CRatio)
    return imagen_jpeg
    

"""
Implementar la función jpeg_color(imagen_color) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen RGB 'imagen_color' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error para cada una de las componentes RGB
Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))


En este caso optimizar la DCT 
http://docs.scipy.org/doc/numpy-1.10.1/reference/routines.linalg.html
"""
    
def Ajustar_matriz(OrigM,OrigN,imagen):
    Xq = OrigM
    Yq= OrigN
    if OrigM%8!=0:Xq+= 8-(OrigM%8)
    if OrigN%8!=0: Yq+=8-(OrigN%8)
    res = np.zeros((Xq,Yq))
    aux1 = np.zeros((Xq,OrigN))
    aux1[:OrigM,:OrigN] = imagen
    for i in range(Xq-OrigM):
        aux1[OrigM+i]=imagenY[-1]
    res[:Xq,:OrigN]=aux1
    for j in range(Yq-OrigN):
        res[:,OrigN+j]= aux1[:,-1]
    return res

def jpeg_color(imagen_color):
    #Compresión de la imagen
    #Paso 1: Transformación del espacio de colores:
    OrigM,OrigN,OrigC = imagen_color.shape
    imagenY = np.zeros((OrigM,OrigN))
    imagenCb = np.zeros((OrigM,OrigN))
    imagenCr = np.zeros((OrigM,OrigN))
    for i in range(OrigM):
        for j in range(OrigN):
            R = imagen_color[i,j,0]
            G = imagen_color[i,j,1]
            B = imagen_color[i,j,2]
            Y = (75/256)*R+(150/256)*G+(29/256)*B
            Cb = -(44/256)*R-(87/256)*G+(131/256)*B+128
            Cr = (131/256)*R-(110/256)*G-(21/256)*B+128
            imagenY[i,j]=Y
            imagenCb[i,j]=Cb
            imagenCr[i,j]=Cr
            
    #Paso 2: Ajustar tamaño de la matriz, añadir filas y columnas extra
    Matrix_Y = Ajustar_matriz(OrigM,OrigN,imagenY)
    Xq,Yq = Matrix_Y.shape

    Matrix_Y = reshape1(Xq,Yq,Matrix_Y)

    Matrix_Cb = Ajustar_matriz(OrigM,OrigN,imagenCb)
    Matrix_Cb = reshape1(Xq,Yq,Matrix_Cb)

    Matrix_Cr = Ajustar_matriz(OrigM,OrigN,imagenCr)
    Matrix_Cr = reshape1(Xq,Yq,Matrix_Cr)
    
    #Paso 3: desplazar 128 y aplicar dct a los bloques de la imagen
    Matrix_Y -=128
    Matrix_Cb -=128
    Matrix_Cr -=128
    numBloc=int((Xq*Yq)/(8*8))



    print(Matrix_Cb)




    for i in range(numBloc):
        Matrix_Y[i]=dct_bloque(Matrix_Y[i])
        Matrix_Cb[i]=dct_bloque(Matrix_Cb[i])
        Matrix_Cr[i]=dct_bloque(Matrix_Cr[i])
    



    print('SHAPE 1  ', Matrix_Y.shape)
    print('SHAPE 2  ', Matrix_Cb.shape)
    print('SHAPE 3  ', Matrix_Cr.shape)


    #Paso 4: Cuantización de los valores:
    Q = Q_matrix()
    for i in range(numBloc):
        for w in range(8):
            for z in range(8):
                Matrix_Y[i,w,z] /= Q_Luminance[w,z]
                Matrix_Y[i,w,z] = round(Matrix_Y[i,w,z],0)
                Matrix_Cb[i,w,z] /= Q[w,z]
                Matrix_Cb[i,w,z] = round(Matrix_Cb[i,w,z],0)
                Matrix_Cr[i,w,z] /= Q_Chrominance[w,z]
                Matrix_Cr[i,w,z] = round(Matrix_Cr[i,w,z],0)
    
    #Calculo de la ratio de compresión aproximada:
    coef = OrigM*OrigN*OrigC
    coefNul = (Matrix_Y == 0).sum()+(Matrix_Cb == 0).sum()+(Matrix_Cr ==0).sum()
    CRatio = coef/(coef-coefNul)
    






    
    #Proceso inverso:
    #Paso 1: iDCT a los bloques
    for i in range(numBloc):
        Matrix_Y[i]=idct_bloque(Matrix_Y[i])
        Matrix_Cb[i]=idct_bloque(Matrix_Cb[i])
        Matrix_Cr[i]=idct_bloque(Matrix_Cr[i])
        
    #Paso 2: Reshape de la matriz
    imagenY_inv = reshape2(Xq,Yq,Matrix_Y)
    imagenCb_inv = reshape2(Xq,Yq,Matrix_Cb)
    imagenCr_inv = reshape2(Xq,Yq,Matrix_Cr)
    
    #Paso3: Cambio al espacio de color RGB
    imagen_jpeg = np.zeros((OrigM,OrigN,OrigC))
    for i in range(OrigM):
        for j in range(OrigN):
            Y = imagenY[i,j]
            Cb = imagenCb[i,j]
            Cr = imagenCr[i,j]
            R = Y+(1.371*(Cr-128))
            G = Y-(0.698*(Cr-128))-(0.336*(Cb-128))
            B = Y+(1.732*(Cb-128))
            imagen_jpeg[i,j,0]=R
            imagen_jpeg[i,j,1]=G
            imagen_jpeg[i,j,2]=B
            
    #Paso 4: Pintar imagen       
    plt.imshow(imagen_jpeg.astype(np.uint8)) 
    plt.xticks([])
    plt.yticks([])
    plt.show() 
    
    #Calculo del error:
    imagen_jpeg = imagen_jpeg.astype(np.int64)
    Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))
    print("Error de la imagen a color: ",Sigma)
    print("Ratio de compresion de la imagen a color:",CRatio)
    
    return imagen_jpeg
"""
#--------------------------------------------------------------------------
Imagen de GRISES

#--------------------------------------------------------------------------
"""


### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al 
### restar 128 puede devolver un valor positivo mayor que 128


"""
#--------------------------------------------------------------------------
Imagen COLOR
#--------------------------------------------------------------------------
"""
## Aplico.astype pero después lo convertiré a 
## uint8 para dibujar y a int64 para calcular el error

mandril_color=scipy.misc.imread('./mandril_color.png').astype(np.int32)

start= time.clock()
mandril_jpeg=jpeg_color(mandril_color)     
end= time.clock()
print("tiempo",(end-start))
     
       









