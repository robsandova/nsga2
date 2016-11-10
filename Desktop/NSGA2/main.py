import funciones
from nsga2func import Solucion
from nsga2func import NSGA2
import math
import time, sys, random
from random import randint
import numpy as np
import matplotlib.pyplot as plt

global matrixDistancia, matrixFlujoUno, matrixFlujoDos
global numFac
matrixDistancia = []
matrixFlujoUno = []
matrixFlujoDos = []


def main():
	
	numFac = funciones.distribuirMatrices(funciones.lectura())
	start = time.time()
	nsga2 = NSGA2(2, 0.3, 1.0)
	P = []
	funciones.crearPoblacion(P,25, numFac)
	front = nsga2.fastNonDominatedSort(P)
	#for fron in front:
	#	nsga2.crowdingDistanceAssignment(fron)

	#nsga2.sortCrowding(P)

	pob = nsga2.runAlgorithm(P,25,25)
	end = time.time()
	print "T =", end-start
	funciones.graficarPob(pob)
	


if __name__ == '__main__':
	main()

