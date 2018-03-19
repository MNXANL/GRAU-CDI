

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


def cdf(p):
    f = []
    for i in range(0, len(p)):
        f.append( sum(p[0:i]) )
    f.append(1)
    return f
    
def Arithmetic(mensaje, alfabeto, probabilidades):
    f = cdf(probabilidades)
    fx = [0.0] * len(f)
    diff = 1
    aux1 = 0
    aux2 = 0
    for msg in mensaje:
        for i in range(0, len(f)):
            fx[i] = aux1 + (f[i]*diff)
        idx = alfabeto.index(msg)
        diff = fx[idx] - fx[idx+1]
        aux1 = fx[idx]
        aux2 = fx[idx+1]
    m = aux1
    M = aux2
    return m, M


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


print(EncodeArithmetic2('ccda',['a','b','c','d'],[0.4,0.3,0.2,0.1]))