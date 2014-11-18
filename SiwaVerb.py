# -*- coding: utf-8 -*-
# 1 = ḷ, ! = Ḷ
# 2 = ẓ, @ = Ẓ
# 3 = ɛ, # = Ɛ
# 4 = ṭ, $ = Ṭ
# 5 = ṣ, % = Ṣ
# 6 = ḍ
# 7 = ḥ, & = Ḥ
# 8 = ḅ, * = Ḅ
# 9 = ɣ
# 0 = č, ) = Č

V = ['a','i','u']
C = ['q','w','r','t','y','s','d','f','g','h','j','k','l','z','x','c','b','n','m','0','5','6','2','1','-','8','7','9','4','3']
K = ['Q','W','R','T','Y','S','D','F','G','H','J','K','L','Z','X','C','B','N','M',')','%','$','@','!','_','*','&','Q','$','#']

def CountWeight(x):
	weight = 0
	if IsFinalGeminate(x) == True:
		weight += 1
	#if IsFinalLong(x) == True:
	#	weight += 1
	for phoneme in x:
		if phoneme in V:
			weight += 2
		if phoneme in K:
			weight += 3
		if phoneme in C:
			weight += 1
		else:
			weight += 0
	return weight

def IsBhD(x):
	BhD = ['fl', 'rf']
	if x in BhD:
		return True
	else:
		return False
		
def IsOnom(x):
	Onom = ['0r04']
	if x in Onom:
		return True
	else:
		return False

def IsValidOnset(x):
	if x[0] in V:
		return False
	if x[0] in K:
		return False
	if x[0] == 'e':
		return False
	else:
		return True

def IsFinalGeminate(x):
	if x[len(x)-1] in K:
		return True
	else:
		return False

def IsFinalLong(x):
	if x[len(x)-2] in V:
		return True
	else:
		return False

def IsFinalM(x):
	if x[len(x)-1] == '-':
		return True
	else:
		return False

#These functions apply morphological processes

def Geminate(x): #Main Gemination Function
	idx = 0
	for cons in C:
		if x == cons:
			return K[idx]
		else:
			idx +=1

def GeminateC1(x): #Geminates the first consonant of a stem
	if x[0] in C:
		return Geminate(x[0]) + x[1:]
	else:
		return x

def GeminateC2(x): #Geminates the second consonant of a stem
	return x[:1] + Geminate(x[1]) + x[2:]

def PrefixT(x): #Prefixes t- before a stem
	if x[0] == 's' or x[0] == '0':
		return x
	else:
		return 't' + x

def InfixA(x): #Places a long vowel (in this case a, but melodies mutate it) before the last stem consonant.
	if x[len(x)-1] in C:
		return x[:len(x)-1] + 'a' + x[len(x)-1:]
	else:
		return x

#Apply vowel melodies
def MelodyA(x):
	for vowel in V:
		x = x.replace(vowel, 'a')
	return x

def MelodyI(x):
	for vowel in V:
		x = x.replace(vowel, 'i')
	return x

def MelodyU(x):
	for vowel in V:
		x = x.replace(vowel, 'u')
	return x

#Add final vowels
def AddU(x):
	return x + 'u'

def AddA(x):
	return x + 'a'

def AddAI(x): #Adds the variable vowel A/I to the stem, the PNG suffixes functions replace it with either a or i.
	return x + 'A'

#Stem formation
def Pf(stem):
	if CountWeight(stem) <= 2:
		return AddAI(stem)
	if CountWeight(stem) >= 5:
		return GeminateC1(stem)
	else:
		return stem

def Impf(stem):
	output = stem
	if IsBhD(stem):
		output = InfixA(GeminateC1(output))
	if IsValidOnset(output) == False:
		output = MelodyA(PrefixT(output))
		return output
	if CountWeight(output) <= 3:
		output = GeminateC2(output)
		return output
	if IsFinalLong(stem) == True:
		output = PrefixT(AddA(output))
	if IsFinalGeminate(stem) == True:
		output = AddU(output)
		return output
	else:
		output = InfixA(output)
		if IsOnom(stem):
			output = MelodyI(output)
		if IsFinalM(stem):
			output = MelodyU(output)
		else:
			output = MelodyA(output)
	return output

#Shwa Insertion

def InsertShwa(x):
	count = 1
	y = list(x)
	y.append('~')
	while (count <= len(y)):
		if y[len(y)-count-1] in K:
			if y[len(y)-count-2] in C or y[len(y)-count-2] in K: 
				y.insert(len(y)-count-1, 'e')
				count += 1
			else:
				count += 1
		if y[len(y)-count-1] in C:
			if y[len(y)-count-2] in C or y[len(y)-count-2] in K: 
				if y[len(y)-count] == 'e' or y[len(y)-count] in V:
					count += 1
					if y[len(y)-count-3] == 'e' or y[len(y)-count-3] in V:
						count += 1
				else:
					y.insert(len(y)-count-1, 'e')
					count += 1
			else:
				count += 1
		else:
			count += 1
	if y[0] == 'y' and y[1] in C:
		y[0] = 'i'
	y.pop()
	return  ''.join(y)

#PNG-Marking
def Conj1s(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'i'
	return x + '9'

def Conj2s(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'i'
	return x + '4'

def Conj3sm(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'a'
	return 'y' + x

def Conj3sf(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'a'
	return 't' + x

def Conj1p(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'a'
	return 'n' + x

def Conj2p(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'a'
	return x + 'm'

def Conj3p(x):
	if x[len(x)-1] == 'A':
		x = x[:len(x)-1] + 'a'
	return 'y' + x + 'n'

#Complete conjugation (excluding imperatives, and without the IRR ga- prefix).
def Conj(x):
	print '1S   |' + InsertShwa(Conj1s(x)) + '   | ' + InsertShwa(Conj1s(Pf(x))) + '  | ' + InsertShwa(Conj1s(Impf(x)))
	print '2S   |' + InsertShwa(Conj2s(x)) + '   | ' + InsertShwa(Conj2s(Pf(x))) + '  | ' + InsertShwa(Conj2s(Impf(x)))
	print '3S:M |' + InsertShwa(Conj3sm(x)) + '   | ' + InsertShwa(Conj3sm(Pf(x))) + '  | ' + InsertShwa(Conj3sm(Impf(x)))
	print '3S:F |' + InsertShwa(Conj3sf(x)) + '   | ' + InsertShwa(Conj3sf(Pf(x))) + '  | ' + InsertShwa(Conj3sf(Impf(x)))
	print '1P   |' + InsertShwa(Conj1p(x)) + '   | ' + InsertShwa(Conj1p(Pf(x))) + '  | ' + InsertShwa(Conj1p(Impf(x)))
	print '2P   |' + InsertShwa(Conj2p(x)) + '   | ' + InsertShwa(Conj2p(Pf(x))) + '  | ' + InsertShwa(Conj2p(Impf(x)))
	print '3P   |' + InsertShwa(Conj3p(x)) + ' | ' + InsertShwa(Conj3p(Pf(x))) + ' | ' + InsertShwa(Conj3p(Impf(x)))
	print '-----------------------------------'

#Testcases
print Conj('fl')
print Conj('Ks')
print Conj('sl')
print Conj('lmd')
print Conj('jL')
print Conj('ban')
print Conj('suq')
print Conj('0ur')
print Conj('ukr')
print Conj('bdu')
print Conj('siwl')
print Conj('sugz')
print Conj('qiqw')
print Conj('0r04')
print Conj('ndd-')
print Conj('en7rq')
print Conj('bdd')
print Conj('kMl') 