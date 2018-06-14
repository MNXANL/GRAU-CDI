# COMPRESION SIN PERDIDAS

# A QUE TRANSFORMACION SE CORRESPONDEN LOS BLOQUES DE LA IMAGEN ADJUNTA

import numpy as np
from scipy import misc
from math import sqrt
from math import log2
import matplotlib.pyplot as plt

Z = (1 / sqrt(2))

c1 = np.array([ [Z, Z, 0, 0],
				[Z,-Z, 0, 0],
				[0, 0, Z, Z],
				[0, 0, Z,-Z]])

c2 = np.array([ [1, 0, 0, 0],
				[0, 1, 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]])

c3 = np.array([ [1, 1, 1, 1],
				[1, 1,-1,-1],
				[1,-1,-1, 1],
				[1,-1, 1,-1]])

c4 = np.array([ [0, 0, 0, 1],
				[0, 0, 1, 0],
				[0, 1, 0, 0],
				[1, 0, 0, 0]])

def idct_bloque(p):
	c = c1
	ct = np.transpose(c)
	return (np.tensordot(np.tensordot(ct, p, axes=([1],[0])), c, axes = ([1],[0]))).reshape(-1)



def doIT01():
	fig = plt.figure()
	array = np.zeros((4,4))
	array = array.astype(int)
	for i in range(4):
		for j in range(4):
			array[i][j] = 1
			m = idct_bloque(array)
			fig.add_subplot(4, 4, i*4+j+1 ).axis('off')
			plt.imshow((m.reshape((4,4))))
			array[i][j] = 0
	plt.show()
	
doIT01() 


## IMAGEN 1024X1024 PIXELES CON ESCALA DE 64 GRISES. COMPRIMIRLA USANDO DICCIONARIO 256 ENTRADAS CUYAS PALARAS SON BLOQUES DE 16X16 PIXELES


def ratio_de_compresion(pixeles, escala, entradas, pixelesB):
	num = pixeles * pixeles * log2(escala)
	den = (pixeles / pixelesB) * (pixeles / pixelesB) * log2(entradas) + entradas * pixelesB * pixelesB * log2(escala)
	return (num/den)

print("RATIO DE COMPRESION ->", ratio_de_compresion(64, 256, 1024, 4) )


## MATRIX TRANSPOSE

from numpy import array
from numpy.linalg import inv
from math import sqrt #(at line 7)

def transpose_matrix():
	matriz = array([
	[sqrt(11)/11, sqrt(11)/11, 3 * sqrt(11)/11],
	[-sqrt(2)/2, sqrt(2)/2, 0],
	[-3 * sqrt(22)/22, -3 * sqrt(22)/22, sqrt(22)/11]])

	inv_mat = inv(matriz)
    
	print ("Inverse matrix:\n", inv_mat, "\n")
	print ("Transposed std matrix:\n", matriz.transpose())
	print ("\nTransposed inv matrix:\n", inv_mat.transpose())
        
transpose_matrix()
