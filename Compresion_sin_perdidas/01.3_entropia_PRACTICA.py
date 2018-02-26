# -*- coding: utf-8 -*-
"""
NOTA: Aquí (ab)uso las funciones de orden superior de Python!
"""
import math
import numpy as np
import matplotlib.pyplot as plt


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p, tolerancia = 10**(-5)):
    
    bool1 = all(map((lambda x: 0 <= x and x <= 1), p))
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

''' --------------------------------------------------------------- '''

'''
Dibujar H(p, 1-p)
'''



'''
Hallar aproximadamente el máximo de  H(p, q, 1-p-q)
'''



