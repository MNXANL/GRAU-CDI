# -*- coding: utf-8 -*-

import random

'''
0. Dada una codificación R, construir un diccionario para codificar m2c y otro para decodificar c2m
'''
R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

def Encode(M, m2c):
    C = ''
    for m in M:
        if m in m2c:
            C += m2c[m]
    return C

print('Ejercicio 1:', Encode('abcde', m2c))


''' 
2. Definir una función Decode(C, c2m) que, dado un mensaje codificado C y un diccionario 
de decodificación c2m, devuelva el mensaje original M.

HINT: usar la función find(string[, begin[, end]])
'''
def Decode(C,c2m):
    M = ''
    K = ''
    while len(C) > 0:
        K += C[0]
        C = C[1:]
        if K in c2m:
            M += c2m[K]
            K = ''
    return M
  

print('Ejercicio 2:', Decode('01110010101011', c2m)) # El mensaje codificado es 'abcde'

#------------------------------------------------------------------------
# Ejemplo 1
#------------------------------------------------------------------------

R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

'''
3. Generar un mensaje aleatorio M de longitud 50 con las frecuencias 
esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''


def list2str(M):
    Str = ''
    for i in M:
        Str += i
    return Str

def msg_generator():                # Freq:
    a = 'aaaaaaaaaaaaaaaaaaaaaaaaa' #   25
    b = 'bbbbbbbbbbbbbbbbbbbb'      #   20
    c = 'ccccccccccccccc'           #   15
    d = 'dddddddddd'                #   10
    e = 'eeeee'                     #    5
    ListedM = list(a+b+c+d+e)
    random.shuffle(ListedM)
    M = list2str(ListedM)
    return M

M = msg_generator()
C = Encode(M,m2c)

print('Ejercicio 3:', M, C)


''' 
4. Si 'a', 'b', 'c', 'd', 'e' se codifican inicialmente con un código de 
bloque de 3 bits, hallar la ratio de compresión al utilizar el nuevo código.  
'''

r = 0




#------------------------------------------------------------------------
# Ejemplo 2
#------------------------------------------------------------------------
R = [('a','0'), ('b','10'), ('c','110'), ('d','1110'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
5.
Codificar y decodificar 20 mensajes aleatorios de longitudes también aleatorios.  
Comprobar si los mensajes decodificados coinciden con los originales.
'''

def decode20msgs(m2c, c2m):
    M = list()
    alphabet = ['a', 'b', 'c', 'd', 'e']
    for i in range(0, 20):
        #N = random.randint(1, 100)
        N = 5
        M.append(  ''.join(random.choice(alphabet) for _ in range(N))  )
    
    for i in range(0, 20):
        Enc = Encode(M[i], m2c) 
        Dec = Decode(Enc, c2m)
        
        # Original vs decoded test
        if (Enc == Dec):
            print('Index', i, 'HIT!')
        else:
            print('Index', i, 'MISS')
    
                                            

print(decode20msgs(m2c, c2m))



#------------------------------------------------------------------------
# Ejemplo 3 
#------------------------------------------------------------------------
R = [('a','0'), ('b','01'), ('c','011'), ('d','0111'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

''' 
6. Codificar y decodificar los mensajes  'ae' y 'be'. 
Comprobar si los mensajes decodificados coinciden con los originales.
'''

AE_cod = Encode('ae', m2c)
AE_dec = Decode(AE_cod, c2m)

print(AE_dec, AE_cod, 'Is decoding correct?', 'ae' == AE_dec)


BE_cod = Encode('be', m2c)
BE_dec = Decode(BE_cod, c2m)

print(BE_dec, BE_cod, 'Is decoding correct?', 'be' == BE_dec)





  




