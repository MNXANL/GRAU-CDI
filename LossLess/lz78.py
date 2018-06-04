# -*- coding: utf-8 -*-


"""
Dado un mensaje dar su codificación  usando el
algoritmo LZ78


mensaje='wabba wabba wabba wabba woo woo woo'
LZ78Code(mensaje)=[[0, 'w'], [0, 'a'], [0, 'b'], [3, 'a'], 
                   [0, ' '], [1, 'a'], [3, 'b'], [2, ' '], 
                   [6, 'b'], [4, ' '], [9, 'b'], [8, 'w'], 
                   [0, 'o'], [13, ' '], [1, 'o'], [14, 'w'], 
                   [13, 'o'], [0, 'EOF']]
  
"""

def getPos(men,dic):
	for entry in dic:
		if(men==entry[1]): return entry[0]
	return -1
	
def LZ78Code(mensaje):
	mensaje=mensaje
	dic=[]
	stepD=[1,mensaje[0]]
	dic.append(stepD)
	res=[]
	stepR =[0,mensaje[0]]
	res.append(stepR)
	i=1
	cont=2
	while i<len(mensaje):
		j=i;
		pos=0
		while(getPos(mensaje[i:j+1],dic)!=-1 and j<len(mensaje)):
			pos=getPos(mensaje[i:j+1],dic)
			j=j+1;
		stepD=[cont,mensaje[i:j+1]]
		dic.append(stepD)
		if(j<len(mensaje)):
			if(pos==0):stepR=[pos,mensaje[i]]
			else: stepR=[pos,mensaje[j]]
		else: stepR=[pos,'EOF']
		res.append(stepR)
		i=j+1
		cont=cont+1
	if res[-1][1]!='EOF': res.append([0,'EOF'])
	
	return res
"""
Dado un mensaje codificado con el algoritmo LZ78 hallar el mensaje 
correspondiente 

code=[[0, 'm'], [0, 'i'], [0, 's'], [3, 'i'], [3, 's'], 
      [2, 'p'], [0, 'p'], [2, ' '], [1, 'i'], [5, 'i'], 
      [10, 'p'], [7, 'i'], [0, ' '], [0, 'r'], [2, 'v'], 
      [0, 'e'], [14, 'EOF']]

LZ78Decode(mensaje)='mississippi mississippi river'
"""    
def LZ78Decode(codigo):
	dic=[]
	mensaje=''
	cont=1
	for c in codigo:
		if c[1]!='EOF':
			if c[0]==0: 
				mensaje=mensaje+c[1]
				dic.append([cont,c[1]])
				cont=cont+1
			else: 
				mensaje=mensaje+dic[c[0]-1][1]+c[1]
				dic.append([cont,dic[c[0]-1][1]+c[1]])
				cont=cont+1
		else:
			if c[0]>0:
				mensaje=mensaje+dic[c[0]-1][1]
	
	return mensaje
    

i=20#00000000
mensaje='a'
while(i>0):
	mensaje=mensaje+'a'
	i=i-1;

print(LZ78Code(mensaje))
print(LZ78Decode(LZ78Code(mensaje)))

mensaje = 'a' * 300
print(LZ78Code(mensaje))
print(LZ78Decode(LZ78Code(mensaje)))


    
mensaje = 'a' * 3054691
print('Have fun')
print(len(LZ78Code(mensaje)))
#print(LZ78Decode(LZ78Code(mensaje)))


    