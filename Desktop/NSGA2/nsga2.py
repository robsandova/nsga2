# -*- coding: utf-8 -*-
import math
import time, sys, random
from random import randint

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []


class Solucion:

	def __init__(self, numFacilities):
		self.numObjetos = numFac
		self.solution = []
		self.costoFlujo1 = 0.0
		self.costoFlujo2 = 0.0
		self.rank = 10000
		self.numSolDominantes = 0
		self.setSolDominadas = []
		self.crowdedDistance = 0.0

	def costoAsignacion(self):
		self.costoFlujo1 = 0.0
		self.costoFlujo2 = 0.0
		for i in range(numFac):
			for j in range(numFac):
				self.costoFlujo1 = self.costoFlujo1 + matrixFlujoUno[i*(numFac)+j]*matrixDistancia[self.solution[i]*(numFac)+self.solution[j]]
				self.costoFlujo2 = self.costoFlujo2 + matrixFlujoDos[i*(numFac)+j]*matrixDistancia[self.solution[i]*(numFac)+self.solution[j]]
		print "Costo F1: ", self.costoFlujo1
		print "Costo F2: ", self.costoFlujo2

#LECTURA DE INSTANCIAS DEL PROBLEMA
def lectura():
	#archivo = raw_input("Ingrese nombre archivo: ")
	f = open('10.dat', 'r')
	i = 0
	arreglo = []
	tamano = f.readline()
	arreglo.append(tamano)
	for line in f:
		for s in line.split(' '):
			if s == "":
				pass
			elif s == "\n":
				pass
			else:
				num = s
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
	sF1 = sol.costoFlujo1
	sF2 = sol.costoFlujo2
	oF1 = otherSol.costoFlujo1
	oF2 = otherSol.costoFlujo2
	a,b = sF1 < oF1, sF2 < oF2
	c,d = sF1 <= oF1, sF2 <= oF2
	if (c and d) and (a or b):
		#print True
		return True
	else:
		#print False
		return False

def strongDominance(sol, otherSol):
	sF1 = sol.costoFlujo1
	sF2 = sol.costoFlujo2
	oF1 = otherSol.costoFlujo1
	oF2 = otherSol.costoFlujo2
	a,b = sF1 < oF1, sF2 < oF2
	if(a and b):
		return True
	else:
		return False


def fastNonDominatedSort(poblacion):
	fronteras = []
	for p in poblacion:
		for q in poblacion:
			if p == q:
				continue
			if dominance(p,q):
				p.setSolDominadas.append(q)
			elif dominance(q,p):
				p.numSolDominantes += 1
		if p.numSolDominantes == 0:
			p.rank = 1
			fronteras.append(p)
	i = 1
	while len(fronteras) != 0:
		nextFront = []
		for solP in fronteras:
			for solQ in solP.setSolDominadas:
					solQ.numSolDominantes -= 1
					if solQ.numSolDominantes == 0:
						solQ.rank = i+1
						nextFront.append(solQ)
		i +=1
		fronteras = nextFront
	return poblacion		

def crowdingDistanceAssignment(P):
	print "Crowded Distance Assignment"



def onePointCrossover(sol,other):
	print "One Point Crossover beggining"
	child, posRestringidas, posLibres, objPendiente  = [], [], [], []
	rangoA,rangoB = randint(0, numFac-1), randint(2, numFac-2)
	rangoC = rangoA+rangoB
	#print "rA: ", rangoA,
	#print "rB: ", rangoB,
	#print "rC: ", rangoC
	for x in range(rangoA,rangoC):
		indice = x%numFac
		elemento = sol.solution[indice]
		child.insert(indice, elemento)
		posRestringidas.append(indice)
	for x in range(len(sol.solution)):
		if x not in posRestringidas:
			posLibres.append(x)
	#print "pos libres: ", posLibres
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
	print "child: ", 
	print child
	print "One Point Crossover Finished"
	return child

#YO DEL FUTURO:
# ACABO DE TERMINAR EL CROSSOVER CON CICLO CIRCULAR, ME COSTO PERO SALIO AHORAM E DUELE LA CALETA LA CABEZA, MAÑANA SEGUIRÉ
#AHROA QUEDA REALIZAR EL ND-SORTING PARA LAS POBLACIOJNES GENERADA... VAMSO A TERMIANR ESTE ALGORITMO DE MIERDA LUEGO!!!

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
	crearPoblacion(P, 5)
	for elem in P:
		print elem.solution
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
	for elem in P:
		#for other in P:
		#	dominance(elem, other)
		print elem.rank
		pass
		#elem.dominancia(P[cont], P[cont+1])
		#print elem.solution
		#elem.costoAsignacion()
		#twOptSearch(elem)
	end = time.time()
	print "t = ", end-start

if __name__ == '__main__':
	main()

