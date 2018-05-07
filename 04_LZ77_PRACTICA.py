# -*- coding: utf-8 -*-


"""
Dado un mensaje, el tamaño de la ventana de trabajo W, y el tamaño
del buffer de búsqueda S dar la codificación del mensaje usando el
algoritmo LZ77


mensaje='cabracadabrarrarr'
[Offset, longitud, char]
 <--     
LZ77Code(mensaje,12,18)=[
  [0, 0, 'c'], [0, 0, 'a'], 
  [0, 0, 'b'], [0, 0, 'r'], 
  [3, 1, 'c'], [2, 1, 'd'], 
  [7, 4, 'r'], [3, 4, 'EOF']
]
  
"""

def searchSlices(SIZED, SearchBuffer, Slice):
    SIZE = SIZED+1
    StartRange = len(SearchBuffer)-SIZE
    ITERATIONS = 0

    for i in range(StartRange, -1, -1):
        Next = SearchBuffer[i : i+SIZE ]
        #print("'"+Next+"'", '==', "'"+Slice+"'")
        if (Next == Slice):
            return (True, ITERATIONS)
        ITERATIONS += 1
    return (False, 0)


def LZ77Code(mensaj, S=12, W=18):
    mensaje = mensaj + '@'
    code = list()
    O = 0; L = 0; i = 0;

    LookAhead = W
    while (i < len(mensaje)):
        Min = max(i-S, 0)

        SearchBuf = mensaje[ Min : i  ]
        LookAhead = mensaje[i : W] 
        L = 0
        Slice = mensaje[i]
        Value, O2 = searchSlices(L, SearchBuf, Slice)
        while (Value and i < len(mensaje)-1):
            O = O2
            i+=1
            Slice += mensaje[i]
            L = L+1
            Value, O2 = searchSlices(L, SearchBuf, Slice)


        #if len(code)>0: print(i, Slice, code[-1])
        if Slice[-1] != '@': 
            C = Slice[-1]
            newitem = [O+L, L, C]
            code.append(newitem)
            O = 0 ; L = 0

        # Ultimo char -> no hace nada
        elif len(Slice)==1:
            newitem = [0, 0, 'EOF' ]
            code.append(newitem)

        else: 
            L = code[len(code)-1][1]
            if (L == 0): #maybe deadcode
                newitem = [O+1, 1, 'EOF' ]
                code.append(newitem)

            else: #Falla
                Value, O = searchSlices(len(Slice)-2, SearchBuf, Slice[:-1])
                #print('\n\nbeep /', SearchBuf, len(Slice)-1, Value, O, L, "'"+Slice[:-1]+"'")
                #O = code[len(code)-1][0]
                newitem = [O+2, L+1, 'EOF' ]

                code.append(newitem)
                #code[-1] = newitem


        i+=1

    return code


"""
Dado un mensaje codificado con el algoritmo LZ77 hallar el mensaje 
correspondiente 

code=[[0, 0, 'p'], [0, 0, 'a'], [0, 0, 't'], [2, 1, 'd'], 
      [0, 0, 'e'], [0, 0, 'c'], [4, 1, 'b'], [0, 0, 'r'], [3, 1, 'EOF']]

code=[
        1   [0, 0, 'p'], 
        2   [0, 0, 'a'], 
        3   [0, 0, 't'], 
        4   [2, 1, 'd'], 
        5   [0, 0, 'e'], 
        6   [0, 0, 'c'], 
        7   [4, 1, 'b'], 
        8   [0, 0, 'r'], 
        9   [3, 1, 'EOF']
]

LZ77Decode(mensaje)='patadecabra'
"""   


def getDepthString(INI, SIZE, mensaje):
    END = INI+SIZE
    buf = ''
    if (len(mensaje) <= END):
        for i in range(0, END-len(mensaje)):
            buf += mensaje[-1]
    return mensaje[INI:END]+buf


def LZ77Decode(codigo):
    mensaje = ''
    idx = 1
    for code in codigo:
        OFFSET= code[0]
        SIZE  = code[1]
        CHAR  = code[2]
        if (OFFSET==0 and CHAR != 'EOF'):
                mensaje += CHAR
        else:
            INI = len(mensaje) - OFFSET
            aux = getDepthString(INI, SIZE, mensaje)
            mensaje += aux
            if (CHAR != 'EOF'):
                mensaje += CHAR
        #print('>>>>', mensaje)
        ++idx

    return mensaje




print( 'cabracadabrarrarr' )
print( LZ77Decode(LZ77Code('cabracadabrarrarr', 12, 18)) )
print( LZ77Code('cabracadabrarrarr', 12, 18) )
print( '-------------------------' )
code = [
  [0, 0, 'c'], [0, 0, 'a'], 
  [0, 0, 'b'], [0, 0, 'r'], 
  [3, 1, 'c'], [2, 1, 'd'], 
  [7, 4, 'r'], [3, 4, 'EOF']
]
print( code )
      

"""
Jugar con los valores de S y W (bits_o y bits_l)
para ver sus efectos (tiempo, tamaño...)


"""

mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos. La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos. La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos. La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'
#mensaje='topkek pk'
bits_o=12
bits_l=4
S=2**bits_o
W=2**bits_o+2**bits_l

import time
start_time = time.clock()
mensaje_codificado=LZ77Code(mensaje,S,W)
print (time.clock() - start_time, "seconds code")
start_time = time.clock()
mensaje_recuperado=LZ77Decode(mensaje_codificado)
print(mensaje_codificado, '\n-----------')
print(mensaje, '==', mensaje_recuperado)
print (time.clock() - start_time, "seconds decode")
ratio_compresion=8*len(mensaje)/((bits_o+bits_l+8)*len(mensaje_codificado))
print('Longitud de mensaje codificado:', len(mensaje_codificado))
print('Ratio de compresión:', ratio_compresion)




coderino = [
    [0, 0, 'p'],
    [0, 0, 'a'],
    [0, 0, 't'],
    [2, 3, 'p'],
    [4, 5, 'EOF']
]
print( LZ77Decode(coderino) )
