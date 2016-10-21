from random import randint
import itertools

class Dog:
	kind = 'canine'
	def __init__(self, name):
		self.name = name
		self.tricks = []
	def anadirTrick(self, trick):
		self.tricks.append(trick)


d = Dog('Rub')
e = Dog('Boy')
e.anadirTrick('correr en circulo')
d.anadirTrick('perseguirse cola')
d.anadirTrick('correr')
#print d.name
#print d.tricks[1]

	#Debugger para fast-non-dominated sort
	#for elem in poblacion:
	#	print elem.solution
	#	print "Sp"
	#	for sol in range(len(elem.setSolDominadas)):
	#		print elem.setSolDominadas[sol].solution
		#print "numSolDom", 
	#	print elem.numSolDominantes
	#	print "rank", 
	#	print elem.rank
	#	print "NEXT!"

#for x in range(1,11):
#	print repr(x).rjust(2), repr(x*x).rjust(3),
#	print repr(x*x*x).rjust(4)


def generarSolucionRandomNEW(sol):
	nFac = 10
	vectLocalidades = []
	vectObjetos = []
	for x in range(nFac):
		vectObjetos.append(x)
		vectLocalidades.append(x)
	while len(vectObjetos) > 0:
		obj = random.choice(vectObjetos)
		loc = random.choice(vectLocalidades)
		print vectObjetos,
		print vectLocalidades 
		print obj, loc
		sol.insert(obj, loc)
		vectObjetos.pop(vectObjetos.index(obj)), vectLocalidades.pop(vectLocalidades.index(loc))
		print sol




		
numFac = 10
P = []
#generarSolucionRandomNEW(P)
lista = [2,3,5,6,4,9,8,7,1,0]
lista2 = [2,3,5,6,4,9,8,7,1,0]
lista3 = [2,3,5,6,4,9,8,7,1,0]
P.append(lista)
P.append(lista2)
P.append(lista3)

listaCirc = itertools.cycle(lista)
a = randint(0, numFac-1)
b = randint(0,numFac-2)
c = a+b
#print a, b, c
#print lista
for x in range(a,c):
	x = x%numFac
	k = lista[x]
#	print "soy el x: ", x
#	print "soy k: ", k
	#print "soy posicion real: ",k
	#print listaCirc.next()
lista = [2,3,5,6,4,9,8,7,1,0]
print "Prueba!"
for x in range(len(lista)-1, -1, -1):
	print "soy el x:", 
	print x
	for y in range(1,x+1):
		print "y yo el y: ",
		print y





def onePointCrossover():
	numFac = 10
	lista1 = [9,5,2,4,8,7,0,1,3,6]
	lista2 = [0,2,6,7,4,5,3,1,8,9]
	child, posRestringidas, posLibres, objPendiente  = [], [], [], []
	rangoA,rangoB = randint(0, numFac-1), randint(2, numFac-2)
	rangoC = rangoA+rangoB
	print lista1
	print lista2
	print "rA: ", rangoA,
	print "rB: ", rangoB,
	print "rC: ", rangoC
	for x in range(rangoA,rangoC):
		indice = x%numFac
		elemento = lista1[indice]
		child.insert(indice, elemento)
		posRestringidas.append(indice)
	#print child
	#print posRestringidas
	for x in range(len(lista1)):
		if x not in posRestringidas:
			posLibres.append(x)
	#print "pos libres: ", posLibres
	for x in range(numFac):
		elem = lista2[x]
		if elem in child:
			continue
		else:
			objPendiente.insert(x, elem)
	cont = 0
	for x in posLibres:
		child.insert(x,objPendiente[cont])
		cont +=1
	print "child: ", 
	print child
	return child


#onePointCrossover()	




	#	if( rangoA <= x <= rangoC):
	#		child.insert(x, sol.solution[x])
	#		posRestringidas.append(x)
	#	else:
	#		posLibres.append(x)
	#print "pos restringidas: ", posRestringidas
	#print "pos libres: ", posLibres
	#for x in range(numFac):
	#	elemento = other.solution[x]
	#	if (elemento in child):
	#		continue
	#	else:
	#		objPendiente.insert(x,elemento)
	#cont = 0
	#for x in posLibres:
	#	child.insert(x, objPendiente[cont])
	#	cont += 1
		
	#print "Child: ",
	#print child
	#return child

