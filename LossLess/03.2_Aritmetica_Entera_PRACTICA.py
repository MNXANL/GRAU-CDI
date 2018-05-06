# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random


#%%


"""
Dadas las frecuencias f(1),...,f(n), f(i) entero
hallar las frecuencias acumuladas:

F(0) = 0
F(i) = sum(f(k), k = 1..i)
T = F(n)  ->  Suma total de frecuencias

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal que R>4T
"""

def cdf(f):
    CumCount = []
    for i in range(0, len(f)):
        CumCount.append( sum(f[0:i]) )
    return CumCount

## aux begin
def MaxRange(f):
    SIZE = len(f)-1
    T = freq = sum( f[0:SIZE] )
    T4 = T<<2
    k = math.ceil( math.log(T4, 2) )
    R = (1 << k) -1 
    return R 



def LowAndUpperBounds(mensaje, alfabeto, frecuencias):
    cum = cdf(frecuencias)
    R = MaxRange(frecuencias)
    print(R)
    
    Range = 0
    SIZE = len(mensaje)
    i = 1 ; 
    # m -> low | M -> upper
    m = 0 ; M = 0
    
    #                            Underflow    and    Overflow check
    while i < len(mensaje) and Range < SIZE and Range*cum[SIZE] < 2**SIZE:
        Range = abs(M-m)
        M = m + math.floor(Range*cum[ i ] / SIZE) - 1
        m = m + math.floor(Range*cum[i-1] / SIZE)

        print(m, ' -- ', M)
        i += 1
    return m, M

## aux end


"""
Dado un mensaje y su alfabeto con sus frecuencias dar el código 
que representa el mensaje utilizando precisión infinita (reescalado)
"""
def IntegerArithmeticCode(mensaje, alfabeto, frecuencias):
    cum = cdf(frecuencias)
    
    Range = 0
    SIZE = len(mensaje)
    i = 1 ; 
    # m -> low | M -> upper
    m = 0 ; M = 0
    
    #                            Underflow    and    Overflow check
    while i < len(mensaje) :#and Range < SIZE and Range*cum[SIZE] < 2**SIZE:
        Range = abs(M-m)
        M = m + math.floor(Range*cum[ i ] / SIZE) - 1
        m = m + math.floor(Range*cum[i-1] / SIZE)

        print(m, ' -- ', M)
        i += 1
    return m, M
    

"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""
def dec2bin(x, nb=100):
    val = ''
    mid = 0.5
    while (x > 0 and len(val) < nb):
        if (x < mid): val += '0'
        else:
            val += '1'
            x = x - mid
        mid /= 2
    return val



def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias):

    return 'ccda'
    


             
            
#%%
      
mensaje='ccda'
alfabeto=['a','b','c','d','e','f']
frecuencias=[50,20,15,10,5,30]

codigo = IntegerArithmeticCode(mensaje, alfabeto, frecuencias)
print( codigo )

res = IntegerArithmeticDecode(codigo, 4, alfabeto, frecuencias)
print( res )
 
'''
Generar 10 mensajes aleatorios M de longitud n arbitraria 
con las frecuencias esperadas 50, 20, 15, 10 y 5 para los caracteres
'a', 'b', 'c', 'd', 'e' y codificarlo.
'''

alfabeto=['a','b','c','d','e','f']
frecuencias=[50,20,15,10,5,30]
indice=dict([(alfabeto[i],i+1) for i in range(len(alfabeto))])

# Dada una lista de frecuencias n, hallar su entropía.
# De la practica 0.13
def H2(n):
    SUM_VALS = sum(n)
    Probs = map((lambda x: x/SUM_VALS), n)
    bits = 0.0
    for Pi in Probs:
        if Pi != 0:
            bits += (-1 * Pi * math.log(Pi, 2))
    return bits
#####################

print( cdf(frecuencias) )
entropia=H2(frecuencias)
#print('Entropia: ',entropia)



U=''
for i in range(len(alfabeto)):
    U=U+alfabeto[i]*frecuencias[i]
#print(U)
def rd_choice(X,k = 1):
    Y = []
    for _ in range(k):
        Y +=[random.choice(X)]
    return Y

# TAMANYO MUUUUUUUUUUUUUUUUUUUY GRANDE DEL MENSAJE
l_max=100               # 10000
numero_de_pruebas=10    # 100
errores=0


for _ in range(numero_de_pruebas):
    n=random.randint(10,l_max)
    L = rd_choice(U, n)
    mensaje = ''
    for x in L:
        mensaje += x

#    print('---------- ')
#    informacion=sum(math.log(frecuencias[indice[mensaje[i]]-1],2) for i in range(len(mensaje)))-math.log(sum(frecuencias,2))    
#    print('mensaje e información: ',mensaje, informacion)    
    C = IntegerArithmeticCode(mensaje,alfabeto,frecuencias)
#    print(C, len(C))
    mr=IntegerArithmeticDecode(C,len(mensaje),alfabeto,frecuencias)    
    if (mensaje!=mr):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('m =',mensaje)
        print('mr=',mr)
        errores+=1

print("ERRORES: ",errores)





#%%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''


def EncodeArithmetic(mensaje_a_codificar):
    alfabeto = []
    frecuencias = []

    # Creando alfabeto y frecuencias, ambas sin escalado!
    chars = len(mensaje_a_codificar)
    for m in mensaje_a_codificar:
        if alfabeto.count(m) > 0:
            idx = alfabeto.index(m)
            frecuencias[idx] += 1
        elif alfabeto.count(m) == 0:
            alfabeto.append(m) ; alfabeto.sort()
            idx = alfabeto.index(m)
            frecuencias.insert(idx, 1)

    print(alfabeto, frecuencias)
    mensaje_codificado = IntegerArithmeticCode(mensaje_a_codificar, alfabeto, frecuencias)
    return mensaje_codificado, alfabeto, frecuencias
    

print( EncodeArithmetic('ayyyyyyyyyyylllmmmmmmmaoooo') )

def DecodeArithmetic(mensaje_codificado, tamanyo_mensaje, alfabeto, frecuencias):
    mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, tamanyo_mensaje, alfabeto, frecuencias)
    return mensaje_decodificado
        


#%%

'''
'' '
Ejemplo
'' '
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje)
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
        mensaje_codificado
        
        

'''