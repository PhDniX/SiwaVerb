# -*- coding: utf-8 -*-
# 1 = ḷ, ! = Ḷ
# 2 = ẓ, @ = Ẓ
# 3 = ɛ, # = Ɛ
# 4 = ṭ, $ = Ṭ
# 5 = ṣ, % = Ṣ
# 6 = ḍ, ^ = Ḍ
# 7 = ḥ, & = Ḥ
# 8 = ḅ, * = Ḅ
# 9 = ɣ
# 0 = č, ) = Č

V = [u'a',u'i',u'u']
C = [u'q',u'w',u'r',u't',u'y',u's',u'd',u'f',u'g',u'h',u'j',u'k',u'l',u'z',u'x',u'š',u'b',u'n',u'm',u'0',u'5',u'6',u'2',u'1',u'-',u'8',u'7',u'9',u'4',u'3']
K = [u'Q',u'W',u'R',u'T',u'Y',u'S',u'D',u'F',u'G',u'H',u'J',u'K',u'L',u'Z',u'X',u'Š',u'B',u'N',u'M',u')',u'%',u'^',u'@',u'!',u'_',u'*',u'&',u'(',u'$',u'#']

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
	BhD = [u'fl', u'rf']
	if x in BhD:
		return True
	else:
		return False
		
def IsOnom(x):
	Onom = [u'0r04']
	if x in Onom:
		return True
	else:
		return False

def IsValidOnset(x):
	if x[0] in V:
		return False
	if x[0] in K:
		return False
	if x[0] == u'e':
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
	if x[len(x)-1] == u'-':
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
	if x[0] == u's' or x[0] == u'0':
		return x
	else:
		return u't' + x

def InfixA(x): #Places a long vowel (in this case a, but melodies mutate it) before the last stem consonant.
	if x[len(x)-1] in C:
		return x[:len(x)-1] + u'a' + x[len(x)-1:]
	else:
		return x

#Apply vowel melodies
def MelodyA(x):
	for vowel in V:
		x = x.replace(vowel, u'a')
	return x

def MelodyI(x):
	for vowel in V:
		x = x.replace(vowel, u'i')
	return x

def MelodyU(x):
	for vowel in V:
		x = x.replace(vowel, u'u')
	return x

#Add final vowels
def AddU(x):
	return x + u'u'

def AddA(x):
	return x + u'a'

def AddAI(x): #Adds the variable vowel A/I to the stem, the PNG suffixes functions replace it with either a or i.
	return x + u'A'

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
				y.insert(len(y)-count-1, u'e')
				count += 1
			else:
				count += 1
		if y[len(y)-count-1] in C:
			if y[len(y)-count-2] in C or y[len(y)-count-2] in K: 
				if y[len(y)-count] == u'e' or y[len(y)-count] in V:
					count += 1
					if y[len(y)-count-3] == u'e' or y[len(y)-count-3] in V:
						count += 1
				else:
					y.insert(len(y)-count-1, u'e')
					count += 1
			else:
				count += 1
		else:
			count += 1
	if y[0] == u'y' and y[1] in C:
		y[0] = u'i'
	y.pop()
	return  ''.join(y)

#PNG-Marking
def Conj1s(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'i'
	return x + u'9'

def Conj2s(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'i'
	return x + u'4'

def Conj3sm(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'a'
	return u'y' + x

def Conj3sf(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'a'
	return u't' + x

def Conj1p(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'a'
	return u'n' + x

def Conj2p(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'a'
	return x + u'm'

def Conj3p(x):
	if x[len(x)-1] == u'A':
		x = x[:len(x)-1] + u'a'
	return u'y' + x + u'n'

#Complete conjugation (excluding imperatives, and without the IRR ga- prefix).
def Conj(x):
	print u'1S   |' + InsertShwa(Conj1s(x)) + u'   | ' + InsertShwa(Conj1s(Pf(x))) + u'  | ' + InsertShwa(Conj1s(Impf(x)))
	print u'2S   |' + InsertShwa(Conj2s(x)) + u'   | ' + InsertShwa(Conj2s(Pf(x))) + u'  | ' + InsertShwa(Conj2s(Impf(x)))
	print u'3S:M |' + InsertShwa(Conj3sm(x)) + u'   | ' + InsertShwa(Conj3sm(Pf(x))) + u'  | ' + InsertShwa(Conj3sm(Impf(x)))
	print u'3S:F |' + InsertShwa(Conj3sf(x)) + u'   | ' + InsertShwa(Conj3sf(Pf(x))) + u'  | ' + InsertShwa(Conj3sf(Impf(x)))
	print u'1P   |' + InsertShwa(Conj1p(x)) + u'   | ' + InsertShwa(Conj1p(Pf(x))) + u'  | ' + InsertShwa(Conj1p(Impf(x)))
	print u'2P   |' + InsertShwa(Conj2p(x)) + u'   | ' + InsertShwa(Conj2p(Pf(x))) + u'  | ' + InsertShwa(Conj2p(Impf(x)))
	print u'3P   |' + InsertShwa(Conj3p(x)) + u' | ' + InsertShwa(Conj3p(Pf(x))) + u' | ' + InsertShwa(Conj3p(Impf(x)))
	print u'-----------------------------------'

#Testcases
'''print Conj('fl')
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
print Conj('kMl')'''
print Conj(u'krš') 