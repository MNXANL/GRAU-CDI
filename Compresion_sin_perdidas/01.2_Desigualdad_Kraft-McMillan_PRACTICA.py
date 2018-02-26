# -*- coding: utf-8 -*-
"""

"""

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.

'''

def kraftSum(L, q):
    sum = 0
    for l in L:
        sum += 1/(q ** l)
    return sum

def kraft1(L, q=2):
    sum = kraftSum(L, q)
    return sum <= 1


'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.

'''

def kraft2(L, q=2):
    return kraft3(L, max(L), q)


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def kraft3(L, Ln, q=2):
    if kraft1(L, q):
        alpha = kraftSum(L, q)
        K = 0
        i = 0
        while K+alpha <= 1 and i < len(L):
            if len(L[i]) == len(Ln):
                K += (1/L[i])
                i += 1
        return K
                
    else: return 0

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''
def Code(L, q=2):
    return 0

'''
Ejemplo
'''

L = [1, 3, 5, 5, 10, 3, 5, 7, 8, 9, 9, 2, 2, 2]
print(sorted(L), ' codigo final:', Code(L, 3))
print(kraft1(L))
print(kraft2(L))
print(kraft3(L, max(L)+1, 2))
