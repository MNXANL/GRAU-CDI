# -*- coding: utf-8 -*-

import itertools    # cartesian product

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
        uneq = missing / am1
        return 1/uneq
                
    else: return 0

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes
'''

def Code(L, q=2):
    L = sorted(L)
    prev = 0
    idx = 0
    code = []
    for i in L:
        if i != prev:
            idx = 0
            LST = list( itertools.product(range(q), repeat=i) )
            for c in code:
                prefixing = True
                while prefixing:
                    aux = ''.join(str(sl)   for sl in LST[idx])
                    if aux.startswith(c): 
                        idx += 1
                    else: prefixing = False

        code.append(''.join(str(sl) for sl in LST[idx]))
        idx += 1
        prev = i
    return code

'''


Ejemplo

[1, 2, 2, 2, 3, 3, 5, 5, 5, 7, 8, 9, 9, 10]  
codigo final: ['0', '10', '11', '12', '200', '201', '20200', '20201', '20202', '2021000', '20210010', '202100110', '202100111', '2021001120']
'''

L = [1, 3, 5, 5, 10, 3, 5, 7, 8, 9, 9, 2, 2, 2]
print(sorted(L), ' codigo final:', Code(L, 3))
print(kraft1(L))
#print(kraft2(L))
#print(kraft3(L, max(L)+1, 2))



L = [2,3,3,4,5,6,6,6,6,7,7,8,8,8,8,9,9]
print(sorted(L), ' codigo final:', Code(L, 2))
print(kraft1(L))
print(kraft2(L))
print(kraft3(L, 2))

L = [2,3,3,4,4,5,6,6,6,7,8]
print('\n\n\n codigo final:', Code(L, 2))
print(kraft1(L, 2))
print(kraft2(L, 2))
print(kraft3(L, 2))


a= ['00', '010', '011', '100', '101', '1100', '1101', '1110', '1111'] #L = [2, 3, 3, 3, 3, 4, 4, 4, 4]
b= ['00', '01', '100', '101', '110', '111', '1111'] # NO
c= ['0', '10', '110', '111'] #L = [1, 2, 3, 3]
d= ['00', '010', '011', '100', '101', '1100', '1101', '1110', '1111', '11111'] # NO


L = [2,2,2, 3,3, 4,4,4, 5,5,5, 6,6,6,6, 7, 8, 9,9]
#print('\n\n\n codigo final:', Code(L, 2))



def prefijo(lst):
    out = []
    sum = 0
    for i in lst:
        sum += 2**(-i)
    if sum>1: return out
    else:
        for j in range(0, 2**i):
            isPrefix = False
            aux = bin(j)[2:].zfill(i)
            for binw in out:
                prefix = (aux.startswith(binw) or binw.startswith(aux))
                if isPrefix: break
            if not isPrefix:
                out.append(aux)
                break
        return out

if not prefijo(L): 
    print('\n\n\nNO CODE EXISTS')
else: 
    print('\n\n\nYES THERE IS A CODE!')