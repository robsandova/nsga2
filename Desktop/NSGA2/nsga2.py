# -*- coding: utf-8 -*-
import math
import time, sys, random
from random import randint

global matrixDistancia, matrixFlujoUno, matrixFlujoDos, matrixFronteras
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []
matrixFronteras = []


class Solucion:

	def __init__(self, numFacilities):
		self.numObjetos = numFac
		#self.numObjetivos = 2
		self.costoFlujo = []
		for _ in range(1,3):
			self.costoFlujo.append(None) 
		self.solution = []
		self.rank = 10000
		self.numSolDominantes = 0
		self.setSolDominadas = []
		self.crowdedDistance = 0.0

	def costoAsignacion(self):
		self.costoFlujo[0] = 0.0
		self.costoFlujo[1]= 0.0
		for i in range(numFac):
			for j in range(numFac):
				self.costoFlujo[0] = self.costoFlujo[0] + matrixFlujoUno[i*(numFac)+j]*matrixDistancia[self.solution[i]*(numFac)+self.solution[j]]
				self.costoFlujo[1] = self.costoFlujo[1] + matrixFlujoDos[i*(numFac)+j]*matrixDistancia[self.solution[i]*(numFac)+self.solution[j]]
		print "Costo F1: ", self.costoFlujo[0]
		print "Costo F2: ", self.costoFlujo[1]

#LECTURA DE INSTANCIAS DEL PROBLEMA
def lectura():
	#archivo = raw_input("Ingrese nombre archivo: ")
	instancias = open('10.dat', 'r')
	arreglo = []
	tamano = instancias.readline()
	arreglo.append(tamano)
	for line in instancias:
		for caract in line.split(' '):
			if caract == "":
				pass
			elif caract == "\n":
				pass
			else:
				num = caract
				arreglo.append(int(num))
	return arreglo

#DISTRIBUCION EN MATRICES DE FLUJO Y DISTANCIA	
def distribuirMatrices(arreglo):
	global numFac
	numFac = int(arreglo[0])
	largoArray = len(arreglo)
	distribucion = numFac*numFac
	rangoMatrizD = distribucion
	rangoMatrizFU = distribucion*2
	rangoMatrizFD = distribucion*3
	for i in range(1,largoArray):
		if (0 < i and i <= rangoMatrizD):
			matrixDistancia.append(arreglo[i])
		elif (rangoMatrizD < i and i <= rangoMatrizFU):
			matrixFlujoUno.append(arreglo[i])
		elif (rangoMatrizFU < i and i <= rangoMatrizFD):
			matrixFlujoDos.append(arreglo[i])
		else:
			pass
	
def imprimeMatriz(arreglo):
	largo = len(arreglo)
	ancho = int(math.sqrt(largo))
	for i in range(ancho):
		for j in range(ancho):
			print arreglo[i*ancho+j],
			print " ",
		print "\n"

		
def generarSolucionRandom(sol):
	nFac = sol.numObjetos
	vectorObjetos = []
	vectorLocalidades = []
	for x in range(numFac):
		vectorObjetos.append(x)
		vectorLocalidades.append(x)
	while len(vectorObjetos) > 0:
		obj = random.choice(vectorObjetos)
		loc = random.choice(vectorLocalidades)
		sol.solution.insert(obj, loc)
		vectorObjetos.pop(vectorObjetos.index(obj)), vectorLocalidades.pop(vectorLocalidades.index(loc))
	return sol


def crearPoblacion(poblacion, tamPoblacion):
	for x in range(tamPoblacion):
		if(x==0):
			solux = Solucion(numFac)
			generarSolucionRandom(solux)
			poblacion.append(solux)
		else:
			solux = Solucion(numFac)
			generarSolucionRandom(solux)
			while (solux in poblacion):
				generarSolucionRandom(solux)
			poblacion.append(solux)
	return poblacion

def dominance(sol, otherSol):
	sF1 = sol.costoFlujo[0]
	sF2 = sol.costoFlujo[1]
	oF1 = otherSol.costoFlujo[0]
	oF2 = otherSol.costoFlujo[1]
	a,b = sF1 < oF1, sF2 < oF2
	c,d = sF1 <= oF1, sF2 <= oF2
	if (c and d) and (a or b):
		#print True
		return True
	else:
		#print False
		return False

def strongDominance(sol, otherSol):
	sF1 = sol.costoFlujo[0]
	sF2 = sol.costoFlujo[1]
	oF1 = otherSol.costoFlujo[0]
	oF2 = otherSol.costoFlujo[1]
	a,b = sF1 < oF1, sF2 < oF2
	if(a and b):
		return True
	else:
		return False


def fastNonDominatedSort(poblacion):
	fronteras = []
	for solP in poblacion:
		for solQ in poblacion:
			if solP == solQ:
				continue
			if dominance(solP,solQ):
				solP.setSolDominadas.append(solQ)
			elif dominance(solQ,solP):
				solP.numSolDominantes += 1
		if solP.numSolDominantes == 0:
			solP.rank = 1
			fronteras.append(solP)
	matrixFronteras.append(fronteras)		
	cont_front = 1
	while len(fronteras) != 0:
		nextFront = []
		for solP in fronteras:
			for solQ in solP.setSolDominadas:
					solQ.numSolDominantes -= 1
					if solQ.numSolDominantes == 0:
						solQ.rank = cont_front+1
						nextFront.append(solQ)
		cont_front +=1
		fronteras = nextFront
		if(fronteras == []):
			continue
		else:
			matrixFronteras.append(fronteras)
	return poblacion		

def crowdingDistanceAssignment(frontera):
	print "Crowded Distance Assignment"
	largo = len(frontera)
	for sol in frontera:
		sol.crowdedDistance = 0.0
	for n_obj in range(0,2):
		frontera = sortCostoAssignacion(frontera, n_obj)
		frontera[0].crowdedDistance = float('Inf')
		frontera[largo-1].crowdedDistance = float('Inf')
		for i in range(1,largo-1):
			frontera[i].crowdedDistance += (frontera[i+1].costoFlujo[n_obj] - frontera[i-1].costoFlujo[n_obj])/(frontera[largo-1].costoFlujo[n_obj] - frontera[0].costoFlujo[n_obj])

def crowdedComparisonOperator(sol, otherSol):
	if(sol.rank < otherSol.rank):
		return true
	elif (sol.rank == otherSol.rank and sol.crowdedDistance > otherSol.crowdedDistance):
		return true
	else:
		return false
		

def sortRanking(poblacion):
	for i in range(len(poblacion)-1, -1,-1):
		for j in range(1,i+1):
			s1 = poblacion[j-1]
			s2 = poblacion[j]
			if s1.rank > s2. rank:
				poblacion[j-1] = s2
				poblacion[j] = s1
	return poblacion

def sortCostoAssignacion(poblacion, objetivo):
	for i in range(len(poblacion)-1,-1,-1):
		for j in range(1,i+1):
			s1 = poblacion[j-1]
			s2 = poblacion[j]
			if objetivo ==0:
				if s1.costoFlujo[0] > s2.costoFlujo[0]:
					poblacion[j-1] = s2
					poblacion[j] = s1
			elif objetivo ==1:
				if s1.costoFlujo[1] > s2.costoFlujo[1]:
					poblacion[j-1] = s2
					poblacion[j] = s1
	return poblacion

		

def onePointCrossover(sol,other):
	print "One Point Crossover beggining"
	child, posRestringidas, posLibres, objPendiente  = [], [], [], []
	rangoA,rangoB = randint(0, numFac-1), randint(2, numFac-2)
	rangoC = rangoA+rangoB
	for x in range(rangoA,rangoC):
		indice = x%numFac
		elemento = sol.solution[indice]
		child.insert(indice, elemento)
		posRestringidas.append(indice)
	for x in range(len(sol.solution)):
		if x not in posRestringidas:
			posLibres.append(x)
	for x in range(numFac):
		elem = other.solution[x]
		if elem in child:
			continue
		else:
			objPendiente.insert(x, elem)
	cont = 0
	for x in posLibres:
		child.insert(x,objPendiente[cont])
		cont +=1
	#print "child: ", 
	#print child
	print "One Point Crossover Finished"
	return child


def twOptSearch(sol):
	posicionUno = randint(0,numFac-1)
	posicionDos = randint(0,numFac-1)
	while posicionUno == posicionDos:
		posicionDos = randint(0,numFac-1)
	print "posiciones: ", 
	print posicionUno, 
	print posicionDos
	elementoPosUno = sol.solution[posicionUno]
	elementoPosDos = sol.solution[posicionDos]
	a, b = sol.solution.index(elementoPosUno), sol.solution.index(elementoPosDos)
	sol.solution[b], sol.solution[a] = sol.solution[a], sol.solution[b]
	print "Solucion con cambio: ", 
	print sol.solution

	
def main():
	distribuirMatrices(lectura())
	P = []
	start = time.time()
	crearPoblacion(P, 90)
	for elem in P:
		#print elem.solution
		elem.costoAsignacion()

		

	#cont = 0
	#print P[0].solution
	#print P[1].solution
	#P[0].costoAsignacion()
	#P[1].costoAsignacion()
	#dominance(P[0], P[1])
	#print "+++++"
	#dominance(P[1], P[0])
	#onePointCrossover(P[0],P[1])
	#onePcrossover(P[0],P[1])
	fastNonDominatedSort(P)
	sortRanking(P)
	#sortCostoAssignacion(P,1)
	for x in matrixFronteras:
		crowdingDistanceAssignment(x)
	for elem in P:
		#print elem.costoFlujo1,
		#print elem.costoFlujo2,
		print elem.solution,
		print elem.rank,
		print elem.crowdedDistance

		#for other in P:
		#	dominance(elem, other)
		#print elem.rank
		#pass
		#elem.dominancia(P[cont], P[cont+1])
		#print elem.solution
		#elem.costoAsignacion()
		#twOptSearch(elem)
	
	#Debugger de crowded distance
	#cont = 1
	

		

		
	end = time.time()
	#Debugger fronteras
	#cont = 1
	#for x in matrixFronteras:
	#	print "Frontera: ",
	#	print cont
	#	for y in x:
	#		print y.solution
	#	cont+=1	

	print "t = ", end-start

if __name__ == '__main__':
	main()

