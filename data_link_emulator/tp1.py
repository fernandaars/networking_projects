import sys

#Para funcionar corretamente a função deve receber dado em bytes
def encode16(Array_bytes):
	base16 = ""
	for binary in Array_bytes:
		hexa = hex(int(binary, 2))
		temp = hexa.lstrip('0x')
		#print(temp)
		if len(temp) < 2:
			zero = "0"
			temp = zero + temp
			#print("Precisou completar: ",temp)
		base16 = base16 + temp
	return base16


def decode16(string):
	return bytes.fromhex(string).decode('ascii')

def insert_DLE(string, index):
    return string[:index] + '1b' + string[index:]

def findDLE(dado):
	start = 0
	ind = 0
	while ind!=-1:
		if start < len(dado):
			ind = dado.find("1b", start)
			print(ind)
			if ind != -1:
				dado = insert_DLE(dado, ind)
				print(dado)
				start = ind + 4
		else:
			ind = -1
	return dado

def findEOF(dado):
	start = 0
	ind = 0
	while ind!=-1:
		if start < len(dado):
			ind = dado.find("cd", start)
			print(ind)
			if ind != -1:
				dado = insert_DLE(dado, ind)
				print(dado)
				start = ind + 4
		else:
			ind = -1
	return dado

def framing(ID, flags, checksum, dados):
	frame = "cc"
	frame = frame + ID + flags + checksum + dados + "dc"
	return frame

#Teste de encode16 e decode16
for msg in sys.stdin:
	a_msg = bytes(msg, "ascii")
	str_bin = ' '.join(format(x, 'b') for x in bytearray(a_msg))
	Array_bytes = str_bin.split()

	string = encode16(Array_bytes)
	print("Em base16: ", string)
	print("Em ascii: ", decode16(string))

#byte stuffing e framing
dado = "dccd001bb1"
dado1 = findDLE(dado)
dado2 = findEOF(dado1)
print(dado2)

ID = "00"
flags = "7f"
checksum = "ae2d"
print(framing(ID, flags, checksum, dado2))




