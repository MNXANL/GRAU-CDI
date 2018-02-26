# -*- coding: utf-8 -*-
"""
NOTA: Aquí (ab)uso las funciones de orden superior de Python!
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p, tolerancia = 10**(-5)):
    
    ''' Check si 0 <= p[i] <= 1 '''
    bool1 = all( map((lambda x: 0 <= x and x <= 1), p) )
    
    ''' Check si sum(p[i]) == 1 usando tolerancias '''
    sum_abs = math.fsum(p) - 1
    bool2 = sum_abs <= tolerancia
    return bool1 and bool2


'''
Dado un código C y una ddp p, hallar la longitud media del código.
'''

def LongitudMedia(C, p):
    acc = 0
    for i in range(0, len(p)):
        acc += p[i] * len(C[i])
    return acc
        

    
'''
Dada una ddp p, hallar su entropía.
'''
def H1(p):
    bits = 0.0
    for Pi in p:
        if Pi != 0:
            bits += (-1 * Pi * math.log(Pi, 2))
    return bits


'''
Dada una lista de frecuencias n, hallar su entropía.
'''
def H2(n):
    SUM_VALS = sum(n)
    Probs = map((lambda x: x/SUM_VALS), n)
    return H1(Probs)




'''
Ejemplos
'''
C = ['001', '101', '11', '0001', '000000001', '0001', '0000000000']
p = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1, 0]
n = [5, 2, 1, 1, 1]

print( es_ddp(p, 10**(-5)) )
print(H1(p))
print(H2(n))
print(LongitudMedia(C,p))

''' 
-------------------------------------------------------------------------------
 

Dibujar H(p, 1-p)
'''
def DrawH(step = 0.01):
    X = list()
    Y = list()
    for p in np.arange(0.0, 1.0, step):
        Z = [p, 1-p]
        X.append(p)
        Y.append(H1(Z))
    plt.plot(X, Y)
        
DrawH()

'''
Hallar aproximadamente el máximo de  H(p, q, 1-p-q)
'''
def MaxH(step = 0.01):
    
    Max = 0.0
    #X = list()
    #Y = list()
    #Z = list()
    for p in np.arange(0.0, 1.0, step):
        for q in np.arange(0.0, 1.0, step):
            if (1-p-q >= 0):
                Z = [p, q, 1-p-q]
                entropy = H1(Z)
                #X.append(p)
                #Y.append(q)
                #Z.append(entropy)
                if Max < entropy:  Max = entropy
    
    return Max
        
print("max{ H(p, q, 1-p-q) } = ", MaxH())


