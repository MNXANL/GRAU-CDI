# -*- coding: utf-8 -*-
"""
"""
import operator


#%%----------------------------------------------------

'''
Dada una distribucion de probabilidad, hallar un código de Huffman asociado
'''

'''
    p -> Árbol de Huffman p     [ [ [0.05, 0.05], 0.1 ], 0.8]
    probs -> probs acumuladas del árbol anterior. 
             Tiene el mismo length que p a cada paso. Ejemplo:
    Paso0: [0.05, 0.05,   0.1,   0.8]
    Paso1: [    0.1,      0.1,   0.8]
    Paso2: [         0.2,        0.8]
'''
def makeHuffmanTree(tree, probs):
    while len(tree) > 2:
        Size = len(tree)
        maximo = 1.0    # numero maximo arbitrario
        pos = 0         # pos del numero maximo
        for i in range(Size-1):
            tmp = probs[i] + probs[i+1]
            if (tmp < maximo):
                pos = i
                maximo = tmp
        # Meter los dos minimos en un subárbol
        
        list_of_pos =  [ tree[pos], tree[pos+1] ] 
        tree[pos] = list_of_pos
        tree.pop(pos+1)
        
        # Recalcular los árboles de probabilidad
        probs[pos] += probs[pos+1]
        probs.pop(pos+1)
    return tree

'''
Formato código Huffman:
    [(codigo_i, ddp_i), ...]
   [('1', 0.80), ('01', 0.1), ('000', 0.05), ('0001', 0.05)]
'''

import collections

def flatten(iterable):
    iterator = iter(iterable)
    array, stack = collections.deque(), collections.deque()
    while True:
        try:
            value = next(iterator)
        except StopIteration:
            if not stack: return list(array)
            iterator = stack.pop()
        else:
            if not isinstance(value, str) and isinstance(value, list):
                stack.append(iterator)
                iterator = iter(value)
            else:
                array.append(value)

             
def recursiveHuffman(curCode, tree):
    code0 = curCode + '0'
    code1 = curCode + '1'
    if type(tree[0]) == float:  # Caso base -> hemos llegado a una ddp
        lst1 = (code0, tree[0])
    elif type(tree[0]) == list:   # Caso recurrente
        lst1 = recursiveHuffman(code0, tree[0])
        
    if type(tree[1]) == float:  # Caso base -> hemos llegado a una ddp
        lst2 = (code1, tree[1])
    elif type(tree[1]) == list:   # Caso recurrente
        lst2 = recursiveHuffman(code1, tree[1])
        
    return [lst1, lst2]


def Huffman(p):
    tree = sorted(p)
    pProb = list(tree)
    makeHuffmanTree(tree, pProb) #[ [ [0.05, 0.05], 0.1 ], 0.8]
    codigo = recursiveHuffman('', tree) 
    return flatten(codigo)


#%%----------------------------------------------------

'''
Dada la ddp p=[0.80, 0.1, 0.05, 0.05], hallar un código de Huffman asociado,
la entropía de p y la longitud media de código de Huffman hallado.
'''

   
'''
Entropía, de la practica anterior
'''
import math
def Entropy_sub1(p):
    bits = 0.0
    for Pi in p:
        if Pi != 0:
            bits += (-1 * Pi * math.log(Pi, 2))
    return bits

def Entropy(n):
    SUM_VALS = sum(n)
    Probs = map((lambda x: x/SUM_VALS), n)
    return Entropy_sub1(Probs)


p = [0.80, 0.1, 0.05, 0.05]
print(Huffman(p) , Entropy(p), '\n')





#%%----------------------------------------------------

'''
Dada la ddp p=[1/n,..../1/n] con n=2**8, hallar un código de Huffman asociado,
la entropía de p y la longitud media de código de Huffman hallado.
'''

n = 2**8
p256 = [1/n for _ in range(n)]
print(Huffman(p256) , Entropy(p256), '\n')






#%%----------------------------------------------------

'''
Dado un mensaje hallar la tabla de frecuencia de los caracteres que lo componen
'''

# Dict en el que al insertar carácteres devuelve números
class MsgDict(dict):
    def __missing__(self, key):
        return 0.0

def tablaFrecuencias(mensaje):
    freqs = MsgDict()
    size = len(mensaje)
    for m in mensaje:
        if freqs[m]:
            freqs[m] += (1/size)
        else:
            freqs[m] = (1/size)
   
    # Keys sorted as [(key1, val1), (key2, val2), ...]
    freq_sort = sorted(freqs.items(), key = operator.itemgetter(1))
    return freq_sort

'''
Definir una función que codifique un mensaje utilizando un código de Huffman 
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''
#%%----------------------------------------------------

def CreateDict(ListHuff, tf):
    m2c = dict()
    for i in range(len(ListHuff)):
        m2c[tf[i][0]] = ListHuff[i][0]
    return m2c

def CreateDictInv(ListHuff, tf):
    m2c = dict()
    for i in range(len(ListHuff)):
        m2c[ListHuff[i][0]] = tf[i][0]
    return m2c

def EncodeMsg(string, c2m):
    code = str()
    for s in string:
        code += c2m[s]
    return code        

def EncodeHuffman(mensaje_a_codificar):
    tf = tablaFrecuencias(mensaje_a_codificar)
    
    ddp = [ x[1] for x in tf]
    ListHuff = Huffman(ddp)
    print('\n\ntf', tf)
    print('\n\nhf', ListHuff)
    
    c2m = CreateDict(ListHuff, tf)
    m2c = CreateDictInv(ListHuff, tf)
    mensaje_codificado = EncodeMsg(mensaje_a_codificar, c2m)
    return mensaje_codificado, m2c
    


    
def DecodeHuffman(mensaje_codificado, m2c):
    mensaje_decodificado = ''
    aux = ''    #substrings 
    start = 0
    end = 0
    for m in mensaje_codificado:
        aux += m

        if aux in m2c:
            mensaje_decodificado += m2c[aux]
            aux = ''

    return mensaje_decodificado
        
#%%----------------------------------------------------

'''
Ejemplo
'''
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
mensaje_codificado, m2c = EncodeHuffman(mensaje)


mensaje_recuperado = DecodeHuffman(mensaje_codificado, m2c)
print(mensaje_recuperado)


ratio_compresion = 8*len(mensaje)/len(mensaje_codificado)
print('RATIO DE COMPRESIÓN (ASCII) =', ratio_compresion)

ratio_compresion2 = 32*len(mensaje)/len(mensaje_codificado)
print('RATIO DE COMPRESIÓN (UTF-8) =', ratio_compresion2)

'''
Si tenemos en cuenta la memoria necesaria para almacenar el diccionario, 
¿cuál es la ratio de compresión?
    
   * La ratio será de [1.8798257168912758] si se codifica en ASCII
   * La ratio será de [7.519302867565103] si se codifica en UTF-8 
    
    (que es el caso de este ejercicio!)

    ACLARACIÓN: La primera línea de este programa es [ coding: utf-8 ]
    Asumo que el ratio de compresión original es el de un código en ASCII,
    ya que se codifica usando 8 bits, pero el texto del mensaje no se puede
    codificar en ASCII ya que lleva accentos! Por lo tanto esa representación
    no es precisa, y requerirá 32 bits para representarlo en UTF-8.

    (De todas formas, seguramente existen otras codificaciones más precisas 
    que puedan representar este mismo mensaje usando menos bits)

'''

