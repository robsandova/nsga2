import funciones
import random
import numpy as np
import matplotlib.pyplot as plt

class Solucion:

	def __init__(self, numFacilities):
		self.numFacilities = numFacilities
		#self.numObjetivos = 2
		self.costoFlujo = []
		for _ in range(1,3):
			self.costoFlujo.append(None) 
		self.solution = []
		self.rank = 10000
		self.numSolDominantes = 0
		self.setSolDominadas = []
		self.crowdedDistance = 0.0
		self.tabuList = []

	def costoAsignacion(self):
		self.costoFlujo[0] = 0.0
		self.costoFlujo[1]= 0.0
		for i in range(self.numFacilities):
			for j in range(self.numFacilities):
				self.costoFlujo[0] = self.costoFlujo[0] + funciones.matrixFlujoUno[i*(self.numFacilities)+j]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[j]]
				self.costoFlujo[1] = self.costoFlujo[1] + funciones.matrixFlujoDos[i*(self.numFacilities)+j]*funciones.matrixDistancia[self.solution[i]*(self.numFacilities)+self.solution[j]]
		#print "Costo F1: ", self.costoFlujo[0]
		#print "Costo F2: ", self.costoFlujo[1]


class NSGA2:

	def __init__(self, numObjectives, mutationRate, crossoverRate):
		self.numObjectives = numObjectives
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate

	def runAlgorithm(self, poblacion, tamPob, generaciones):
		for sol in poblacion:
			sol.costoAsignacion()
		lastIteration = generaciones-1	
		nextPobla = self.makeNewPob(poblacion)
		for sol in nextPobla:
			sol.costoAsignacion()
		nombreArchivo = "generaciones.csv"
		nArchivo = open(nombreArchivo, 'w' )	
		for i in range(1,generaciones+1):
			print "+++++++++++++++++++"
			print "Iteracion: ", i,
			print "de un total de ", generaciones
			print "+++++++++++++++++++"
			pobCombinada = []
			pobCombinada.extend(poblacion)
			pobCombinada.extend(nextPobla)

			fronteras = self.fastNonDominatedSort(pobCombinada)
			#print "la cantidad de fronteras es: ", len(fronteras)

			del poblacion[:]

			for frontera in fronteras:
				if len(frontera)==0:
					break
				frontera = self.crowdingDistanceAssignment(frontera)
				for elem in frontera:
					poblacion.append(elem)

				if len(poblacion) >= tamPob:
					break
			self.sortCrowding(poblacion)
			if len(poblacion) > tamPob:
				del poblacion[tamPob:]
			
			nArchivo.write("Generacion: " + str(i) + "\n")
			for i in range(len(poblacion)):
				if i == len(poblacion)-1:
					nArchivo.write("" +str(poblacion[i].solution)+ ", " + str(poblacion[i].costoFlujo[0]) + ", " + str(poblacion[i].costoFlujo[1]) + ", " + str(poblacion[i].rank) + "\n")
				else:
					nArchivo.write(""+ str(poblacion[i].costoFlujo[0]) + ", " + str(poblacion[i].costoFlujo[1]) + ", " + str(poblacion[i].rank) + "\n")
				
	
			if i == generaciones:
				break
				#funciones.graficarPob(poblacion)
			else:
				nextPobla = self.makeNewPob(poblacion)
				print "Comenzando Local Search. . ."
				solucionesconLS = tamPob/2
				for i in range(solucionesconLS):
					solucion = random.choice(nextPobla)
					solucion = localSearch(solucion)
		return poblacion
		 		


	def sortRanking(self, poblacion):
		for i in range(len(poblacion)-1, -1,-1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if sol1.rank > sol2. rank:
					poblacion[j-1] = sol2
					poblacion[j] = sol1
		return poblacion

	def sortCostoAssignacion(self, poblacion, objetivo):
		print "Iniciando sortCostoAsignacion. . ."
		for i in range(len(poblacion)-1,-1,-1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if objetivo ==0:
					if sol1.costoFlujo[0] > sol2.costoFlujo[0]:
						poblacion[j-1] = sol2
						poblacion[j] = sol1
				elif objetivo ==1:
					if sol1.costoFlujo[1] > sol2.costoFlujo[1]:
						poblacion[j-1] = sol2
						poblacion[j] = sol1
		return poblacion

	def sortCrowding(self, poblacion):
		print "Iniciando sortCrowding. . ."
		for i in range(len(poblacion)-1, -1, -1):
			for j in range(1,i+1):
				sol1 = poblacion[j-1]
				sol2 = poblacion[j]
				if (crowdedComparisonOperator(sol1, sol2) < 0):
					poblacion[j-1] = sol2
					poblacion[j] = sol1
		return poblacion

	def makeNewPob(self, poblacion):
		print "Creando una nueva poblacion. . ."
		new_pob = []
		while len(new_pob) != len(poblacion):
			child = Solucion(poblacion[0].numFacilities)
			solSeleccionadas = [None, None]
			while solSeleccionadas[0] == solSeleccionadas[1]:
				for i in range(2):
					sol1 = random.choice(poblacion)
					sol2 = random.choice(poblacion)
					while sol1 == sol2:
						sol2 = random.choice(poblacion)
					if crowdedComparisonOperator(sol1, sol2) > 0:
						solSeleccionadas[i] = sol1
					else:
						solSeleccionadas[i] = sol2
			if random.random() < self.crossoverRate:
				child = self.onePointCrossover(solSeleccionadas[0], solSeleccionadas[1])

				if random.random() < self.mutationRate:
					child = self.twOptSearch(child)

				child.costoAsignacion()

			new_pob.append(child)
		return new_pob				

	def fastNonDominatedSort(self, poblacion):
		print "Inicio FND-Sort"
		matrixFrontera = []
		fronteras = []
		for solP in poblacion:
			for solQ in poblacion:
				if solP == solQ:
					continue
				if funciones.dominance(solP,solQ):
					solP.setSolDominadas.append(solQ)
				elif funciones.dominance(solQ,solP):
					solP.numSolDominantes += 1
			if solP.numSolDominantes == 0:
				solP.rank = 1
				fronteras.append(solP)
		matrixFrontera.append(fronteras)		
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
				matrixFrontera.append(fronteras)
		return matrixFrontera

	def crowdingDistanceAssignment(self,frontera):
		print "Crowded Distance Assignment"
		largo = len(frontera)
		for sol in frontera:
			sol.crowdedDistance = 0.0
		for n_obj in range(0,self.numObjectives):
			frontera = self.sortCostoAssignacion(frontera, n_obj)
			if largo == 1:
				frontera[0].crowdedDistance = 0.0
			elif largo == 2:
				frontera[0].crowdedDistance = 2.0
				frontera[1].crowdedDistance = 2.0	
			else:
				frontera[0].crowdedDistance = float('Inf')
				frontera[largo-1].crowdedDistance = float('Inf')
				for i in range(1,largo-1):
					#pass
					#print frontera[i].crowdedDistance,
					#print frontera[i+1].costoFlujo[n_obj]
					frontera[i].crowdedDistance += (frontera[i+1].costoFlujo[n_obj] - frontera[i-1].costoFlujo[n_obj])/(frontera[largo-1].costoFlujo[n_obj] - frontera[0].costoFlujo[n_obj])
		return frontera
		

	def onePointCrossover(self,sol,other):
		#print "One Point Crossover beggining"
		numFac = sol.numFacilities
		child = Solucion(numFac)
		posRestringidas, posLibres, objPendiente  = [], [], []
		rangoA,rangoB = random.randint(0, numFac-1), random.randint(2, numFac-2)
		rangoC = rangoA+rangoB
		for x in range(rangoA,rangoC):
			indice = x%numFac
			elemento = sol.solution[indice]
			child.solution.insert(indice, elemento)
			posRestringidas.append(indice)
		for x in range(len(sol.solution)):
			if x not in posRestringidas:
				posLibres.append(x)
		for x in range(numFac):
			elem = other.solution[x]
			if elem in child.solution:
				continue
			else:
				objPendiente.insert(x, elem)
		cont = 0
		for x in posLibres:
			child.solution.insert(x,objPendiente[cont])
			cont +=1
		#print "child: ", 
		#print child
		#print "One Point Crossover Finished"
		return child


	def twOptSearch(self,sol):
		numFac = sol.numFacilities
		posicionUno = random.randint(0,numFac-1)
		posicionDos = random.randint(0,numFac-1)
		while posicionUno == posicionDos:
			posicionDos = random.randint(0,numFac-1)
		#print "posiciones: ", 
		#print posicionUno, 
		#print posicionDos
		elementoPosUno = sol.solution[posicionUno]
		elementoPosDos = sol.solution[posicionDos]
		a, b = sol.solution.index(elementoPosUno), sol.solution.index(elementoPosDos)
		sol.solution[b], sol.solution[a] = sol.solution[a], sol.solution[b]
		#print "Solucion con cambio: ", 
		#print sol.solution
		return sol

	def binaryTournament(poblacion):
		participantes = random.sample(poblacion, 2)
		best = None
		for solParticipante in participantes:
			if (best is None) or self.crowdedComparisonOperator(solParticipante, best) == 1:
				best = solParticipante
		return best


def localSearch(solucion):
	contadorVecinosDominantes = 0
	listaVecinosDominantes = []
	vecinos = generoVecinos(solucion, 50)
	for vecino in vecinos:
		if funciones.dominance(vecino, solucion):
			listaVecinosDominantes.append(vecino)
			contadorVecinosDominantes +=1
		else:
			continue
	if contadorVecinosDominantes == 1:
		mejorSolucion = listaVecinosDominantes[0]
	elif contadorVecinosDominantes == 0:
		mejorSolucion = solucion
	elif contadorVecinosDominantes > 1:
		mejorSolucion = random.choice(listaVecinosDominantes)
	return mejorSolucion


def generoVecinos(solucion, cantVecinos):
	vecindad = []
	for i in range(cantVecinos):
		vecino = funciones.generarVecino(solucion)
		vecino.costoAsignacion()
		vecindad.append(vecino)
	return vecindad	


def crowdedComparisonOperator(sol, otherSol):
	if (sol.rank < otherSol.rank) or \
		((sol.rank == otherSol.rank) and (sol.crowdedDistance > otherSol.crowdedDistance)):
		return 1
	else: 
		return -1








