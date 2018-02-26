# -*- coding: utf-8 -*-
"""

"""

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.

'''

def kraft1(L, q=2):
    sum = 0
    for li in L:
        sum += q ** li
    return sum <= 1


'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.

'''

def kraft2(L, q=2):


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def kraft3(L, Ln, q=2):


'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''
def Code(L,q=2):


'''
Ejemplo
'''

L=[1, 3, 5, 5, 10, 3, 5, 7, 8, 9, 9, 2, 2, 2]
print(sorted(L), ' codigo final:', Code(L, 3))
print(kraft1(L))
