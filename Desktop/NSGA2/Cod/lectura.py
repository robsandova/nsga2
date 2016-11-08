def lecturaDistribucion():
	archivo = raw_input("Ingrese nombre archivo")
	f = open(archivo, 'r')
	#print f.readline()
	i = 0
	arreglo = []
	tamano = f.readline()
	arreglo.append(tamano)
	print "El tamano es: ", tamano
	for line in f:
		for s in line.split(' '):
			if s == "":
				pass
			elif s == "\n":
				pass
			else:
				num = s
				arreglo.append(num)

	print len(arreglo)
	return arreglo

