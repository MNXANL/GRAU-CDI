# -*- coding: utf-8 -*-


"""
Dado un mensaje dar su codificación usando el
algoritmo LZ78


mensaje='wabba wabba wabba wabba woo woo woo'
LZ78Code(mensaje)=
[[0, 'w'], [0, 'a'], [0, 'b'], [3, 'a'], 
[0, ' '], [1, 'a'], [3, 'b'], [2, ' '], 
[6, 'b'], [4, ' '], [9, 'b'], [8, 'w'], 
[0, 'o'], [13, ' '], [1, 'o'], [14, 'w'], 
[13, 'o'], [0, 'EOF']]
"""


def find(codigo, letras):
    i=0
    idx=0
    for c in codigo:
        aux = ''
        if c[0]==0: aux = c[1]
        else:
            c_1 = codigo[ c[0]-1 ]
            idx = c[0]
            auxRev = c_1[1]

            while(c_1[0] > 0):
                c_1 = codigo[ c_1[0]-1 ]
                auxRev += c_1[1]

            aux += auxRev[::-1] + c[1]
        if (aux == letras):  return (True, i+1)
        i = i+1
    return (False, idx)



def LZ78Code(mensaje):
    code = list()
    i = 0
    SIZE = len(mensaje)
    while i < SIZE:
        idx = 0
        m = mensaje[i]

        (found, idx) = find(code, m)
        while found and i<SIZE-1:
            i += 1
            m += mensaje[i]
            (found, idx2) = find(code, m)
            if found: 
                idx = idx2


        if  len(m) == 1 :#and i < SIZE-1:  
            code += [[ 0, m ]]
        elif len(m) > 1 :#and i < SIZE-1:  
            code += [[ idx, m[-1] ]]
        #elif len(m) > 1 and i == SIZE-1:  
        #    code += [[ idx, 'EOF' ]]
        #else:  
        #    code += [[ 0, 'EOF' ]]

        i += 1
    code += [[ 0, 'EOF' ]]
    return code
    


"""
Dado un mensaje codificado con el algoritmo LZ78 hallar el mensaje 
correspondiente 

code=[[0, 'm'], [0, 'i'], [0, 's'], [3, 'i'], [3, 's'], 
      [2, 'p'], [0, 'p'], [2, ' '], [1, 'i'], [5, 'i'], 
      [10, 'p'], [7, 'i'], [0, ' '], [0, 'r'], [2, 'v'], 
      [0, 'e'], [14, 'EOF']]

LZ78Decode(mensaje)='mississippi mississippi river'
"""    


def getDepthMessage(codigo, idx):
    c2 = codigo[idx-1]

    aux = c2[1]
    idx2 = c2[0]-1
    c2 = codigo[idx2]

    while(idx2 >= 0):
        aux += c2[1]
        idx2 = c2[0]-1
        c2 = codigo[idx2]

    salida = aux[::-1]
    return salida


def LZ78Decode(codigo):
    res = ''
    i = 0;
    for c in codigo:
        idx = c[0]
        if c[1] != 'EOF':
            if idx == 0:  
                res += c[1]
            else:
                res += getDepthMessage(codigo, idx)
                res += c[1]
        else:
            idx2 = idx-1
            if idx2>0: res += codigo[idx-1][1]
    return res




mensaje='wabba wabba wabba wabba woo woo woo' 
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

mensaje='mississipi mississipi' 
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'

import time
bits_indice=12
start_time = time.clock()
mensaje_codificado=LZ78Code(mensaje)
print (time.clock() - start_time, "seconds CODE")
start_time = time.clock()
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print (time.clock() - start_time, "seconds DECODE")
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print(len(mensaje_codificado),ratio_compresion)
if (mensaje!=mensaje_recuperado):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(len(mensaje),len(mensaje_recuperado))
    print(mensaje[-5:],mensaje_recuperado[-5:])


''' '''