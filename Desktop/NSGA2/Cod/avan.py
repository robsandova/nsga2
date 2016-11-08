#COSTO ASIGNACION IMPLEMENTADO COMO MÉTODO DE LA CLASE 2/10

def costoAsignacion(solucion):
	costoFlujo1 = 0
	costoFlujo2 = 0
	filas = len(solucion)
	print filas
	for i in range(filas):
		for j in range(filas):
				costoFlujo1 = costoFlujo1 + matrixFlujoUno[i*(filas)+j]*matrixDistancia[solucion[i]*(filas)+solucion[j]]
				costoFlujo2 = costoFlujo2 + matrixFlujoDos[i*(filas)+j]*matrixDistancia[solucion[i]*(filas)+solucion[j]]
	print "Costo F1: ", costoFlujo1
	print "Costo F2: ", costoFlujo2
	