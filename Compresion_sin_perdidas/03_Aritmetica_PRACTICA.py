# -*- coding: utf-8 -*-


import math
import random

"""
Dado x en [0,1) dar su representacion en binario, por ejemplo
dec2bin(0.625) = '101'
dec2bin(0.0625) = '0001'

Dada la representación binaria de un real perteneciente al intervalo [0,1) 
dar su representación en decimal, por ejemplo

bin2dec('101')=0.625
bin2dec('0001')=0.0625

nb número máximo de bits

"""



def dec2bin(x, nb=100):
    val = ''
    mid = 0.5
    while (x > 0 and len(val) < nb):
        if (x < mid):
            val += '0'
        else:
            val += '1'
            x = x - mid
        mid /= 2
    return val

def bin2dec(xb):
    mid = 0.5
    val = 0
    for x in xb:
        val += int(x)*mid
        mid = mid/2
    return val


"""
Dada una distribución de probabilidad p(i), i=1..n,
hallar su función distribución:
  f(0) = 0
  f(i) = sum(p(k), k = 1..i).
"""

def cdf(p):
    f = []
    for i in range(0, len(p)):
        f.append( sum(p[0:i]) )
    f.append(1)
    return f
    

"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar el intervalo (l,u) que representa al mensaje.

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4, 0.3, 0.2, 0.1]             m       M
Arithmetic(mensaje,alfabeto,probabilidades)= 0.876   0.8776
"""

def Arithmetic(mensaje, alfabeto, probabilidades):
    f = cdf(probabilidades)
    fx = [0.0] * len(f)
    diff = 1
    aux1 = 0
    for msg in mensaje:
        for i in range(0, len(f)):
            fx[i] = aux1 + (f[i]*diff)
        idx = alfabeto.index(msg)
        diff = fx[idx] - fx[idx+1]
        aux1 = fx[idx]
    m = aux1
    M = aux2
    return m, M


"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar la representación binaria de x/2**(t) siendo t el menor 
entero tal que 1/2**(t)<M-m, x entero (si es posible par) tal 
que m/(2**(t)) <= x < M / (2**(t))

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
EncodeArithmetic1(mensaje,alfabeto,probabilidades)='111000001'
"""

def EncodeArithmetic1(mensaje, alfabeto, probabilidades):


"""
Dado un mensaje y su alfabeto con su distribución de probabilidad
dar el código que representa el mensaje obtenido a partir de la 
representación binaria de M y m

mensaje='ccda'
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
EncodeArithmetic2(mensaje,alfabeto,probabilidades)='111000001'

"""
    
def EncodeArithmetic2(mensaje, alfabeto, probabilidades):
    m, M = Arithmetic(mensaje, alfabeto, probabilidades)
    f1 = dec2bin(m)
    f2 = dec2bin(M)
    strng = ''
    similar = True
    i = 0
    while i < max(len(f1), len(f2)) and similar:
        if (f1[i] == f2[i]):
            strng += f1[i]
        else: similar = False
        i += 1
    return strng + '1'

"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con su distribución de probabilidad 
dar el mensaje original

code='0'
longitud=4
alfabeto=['a','b','c','d']
probabilidades=[0.4,0.3,0.2,0.1]
DecodeArithmetic(code,longitud,alfabeto,probabilidades)='aaaa'

code='111000001'
DecodeArithmetic(code,4,alfabeto,probabilidades)='ccda'
DecodeArithmetic(code,5,alfabeto,probabilidades)='ccdab'

"""

def DecodeArithmetic(code,n,alfabeto,probabilidades):


'''
Función que compara la longitud esperada del 
mensaje con la obtenida con la codificación aritmética
'''

def comparacion(mensaje,alfabeto,probabilidades):
    p=1.
    indice=dict([(alfabeto[i],i+1) for i in range(len(alfabeto))])
    for i in range(len(mensaje)):
        p=p*probabilidades[indice[mensaje[i]]-1]
    aux=-math.log(p,2), len(EncodeArithmetic1(mensaje,alfabeto,probabilidades)), len(EncodeArithmetic2(mensaje,alfabeto,probabilidades))
    print('Información y longitudes:',aux)    
    return aux
        
        
'''
Generar 10 mensajes aleatorios de longitud 10<=n<=20 aleatoria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e', codificarlo y compararlas longitudes 
esperadas con las obtenidas.
'''

alfabeto=['a','b','c','d','e']
probabilidades=[0.5,0.2,0.15,0.1,.05]
U = 50*'a'+20*'b'+15*'c'+10*'d'+5*'e'
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

l_max=20

for _ in range(10):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x
    print('---------- ',mensaje)    
    C=comparacion(mensaje,alfabeto,probabilidades)
    print(C)

    
        
        
'''
Generar 10 mensajes aleatorios de longitud 10<=n<=100 aleatoria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''
alfabeto=['a','b','c','d','e']
probabilidades=[0.5, 0.2, 0.15, 0.1, 0.05]
U = 50*'a'+20*'b'+15*'c'+10*'d'+5*'e'
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

l_max=100

for _ in range(10):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x
    print('---------- ',mensaje)    
    C = EncodeArithmetic1(mensaje,alfabeto,probabilidades)
    print(C)

    



    
