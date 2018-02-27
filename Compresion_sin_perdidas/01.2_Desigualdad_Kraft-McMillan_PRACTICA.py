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
        sum += pow(q, -l)
    return sum

def kraft1(L, q=2):
    return kraftSum(L, q) <= 1


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
        alpha = kraftSum(L, q) # info que s'esta fent servir
        K = 0
        
        am1 = 1-alpha # -alpha + one -> Info que encara queda per ocupar
        missing = pow(q, -Ln)
        uneq = missing // am1

        return uneq
                
    else: return 0

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''
def Code(L, q=2):
    ListCode = [str(x) for x in range(q)]
    for l in L:
        # what should I do?
        
    return 0

'''
Ejemplo
'''

L = [1, 3, 5, 5, 10, 3, 5, 7, 8, 9, 9, 2, 2, 2]
print(sorted(L), ' codigo final:', Code(L, 3))
print(kraft1(L))
print(kraft2(L))
print(kraft3(L, max(L)+1, 2))
