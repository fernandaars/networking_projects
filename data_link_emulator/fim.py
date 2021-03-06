import sys

def encode16(Array_bytes):
	base16 = ""
	for binary in Array_bytes:
		hexa = hex(int(binary, 2))
		temp = hexa.lstrip('0x')
		if len(temp) < 2:
			zero = "0"
			temp = zero + temp
		base16 = base16 + temp
	return base16

def preEncode(lista):
	size = len(lista)
	Array_bytes = []
	for i in range(0,size):
		num = bin(lista[i])
		num = num.replace("0b", "")
		Array_bytes.append(num)

	return Array_bytes

def decode16(string):
	size = len(string)
	lista = []
	i = 0
	while i < size:
		s = string[i:i+2]
		i = i + 2
		lista.append(int(s, 16))
		
	return lista

def checksum(frame):
	size = len(frame)
	x = 0
	soma = 0
	
	while size > 1:
		b1 = frame[x]
		b2 = frame[x+1]
		soma = soma + (b1 << 8) + b2
		size = size - 2
		x = x + 2

	if size > 0:
		soma = soma + frame[x]

	while (soma >> 16):
		soma = (soma & 0xffff) + (soma >> 16)

	soma = 0xffff - soma
	b1 = soma >> 8
	b2 = soma & 0xff

	return b1, b2

def convertInt(lista):
	size = len(lista)
	#print("Lista:  ", lista)
	#print("tamanho: ", size)
	inteiros = []
	bits = []
	for x in range(0,size):
		num = int(lista[x], 2)
		inteiros.append(num)
		#num = int(lista[x], 10)
		#bits.append(num)
	#print("inteiros: ", inteiros)

	return inteiros #, bits

def byteStuffing(lista):
	size = len(lista)
	i = 0
	while i < size:
		if lista[i] == 27 or lista[i] == 205:
			lista.insert(i, 27)
			i = i + 2
			size = size + 1
		else:
			i = i + 1
	return lista

def Undo_byteStuffing(lista):	
	size = len(lista)
	i = 0
	while i < size:
		if lista[i] == 27:
			lista.pop(i)
			size = size - 1
		i = i + 1
	return lista

def saidaDado(lista):
	size = len(lista)
	dado = lista[5:size-1]

	size = len(dado)
	frase = ""
	for i in range(0,size):
		frase = frase + chr(dado[i])

	return frase

def framing(lista, ID, FLAG, checksum1, checksum2):
	lista.append(205)
	lista.insert(0, checksum2)
	lista.insert(0, checksum1)
	lista.insert(0, FLAG)
	lista.insert(0, ID)
	lista.insert(0,204)
	return lista

def setChecksum(lista, byte1, byte2):
	lista[3]=byte1
	lista[4]=byte2
	return lista

def setID():
	return 1

def setFlag():
	return 7


input_file = str(sys.argv[1])
output_file = str(sys.argv[2])

f_input = open(input_file, 'r')
f_output = open(output_file, 'w')

#le 256 bytes por vez
a = f_input.read(256)
while len(a) > 0:
	#Formatação da Entrada
	a_msg = bytes(str(a), "ascii")
	str_bin = ' '.join(format(x, 'b') for x in bytearray(a_msg))
	Array_bytes = str_bin.split()
	inteiros = convertInt(Array_bytes)

	ID = 1
	FLAG = 255
	byte1 = 0
	byte2 = 0

	# Antes da Transmissão
	inteiros = byteStuffing(inteiros)
	frame = framing(inteiros, ID, FLAG, byte1, byte2)
	byte1, byte2 = checksum(inteiros)
	frame = setChecksum(frame, byte1, byte2)
	Array_bytes = preEncode(inteiros)
	frame = encode16(Array_bytes)
	
	#depois de Receber o Quadro
	inteiros = decode16(frame)
	# se byte1 e byte2 são iguais a 0 então quadro foi recebido corretamente
	byte1, byte2 = checksum(inteiros)
	if byte1==0 and byte2==0:
		inteiros = Undo_byteStuffing(inteiros)

		#escreve saida
		f_output.write(saidaDado(inteiros))

	else:
		#deu ruim retransmita
		print(":(")

	#le mais 256 bytes
	a = f_input.read(256)
	

f_input.close
f_output.close


