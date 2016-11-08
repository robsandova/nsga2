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
del P[:]

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
for x in range(1,3):
	print x


#DEBUGGER MAIN.PY
#	220
#	P = []
#	matrixFronteras = []
#	funciones.crearPoblacion(P,5, numFac)
#	print "Soluciones P"
#	for elem in P:
#		print elem.solution
#		elem.costoAsignacion()
#
#	nsga2 = NSGA2(2,0.1,1.0)
#	matrixFrontera = nsga2.fastNonDominatedSort(P, matrixFronteras)
#	nsga2.sortRanking(P)
##	Q = nsga2.make_new_pob(P)
#	print "soluciones Q"
#	
#	for elemn in Q:
#		print elemn.solution
#		elemn.costoAsignacion()
#	nsga2.fastNonDominatedSort(Q, matrixFrontera)
#	nsga2.sortRanking(P)
#	nsga2.sortRanking(Q)
##	for elem in matrixFrontera:
#		nsga2.crowdingDistanceAssignment(elem)
#	print "prueba fpr real"
#	for elem in Q:
#		print elem.solution,
#		print elem.rank,
##		print elem.crowdedDistance
#
#	end = time.time()