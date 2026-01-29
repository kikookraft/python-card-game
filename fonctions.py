# le fichier qui contient toutes les fonctions
import random 

def carte_to_chaine(d):
	m=""
	if str(d['valeur'])!="10":
		m+=" "
	m+=str(d['valeur'])
	if d['couleur']=='P':
		m+=chr(9824)
	elif d['couleur']=='C':
		m+=chr(9825)
	elif d['couleur']=='K':
		m+=chr(9826)
	elif d['couleur']=='T':
		m+=chr(9827)
	return m

def afficher_reussite(l):
	for i in l:
		print(carte_to_chaine(i),end="")
		if i!=(len(l)-1):
			print(" ",end="")
	print("\n")

def init_pioche_fichier(n):
	l2=[]
	with open(n, "r") as a:
		c=a.read()
		l=c.split()
	for i in l:
		j=i.split("-")
		if j[0] in ["2","3","4","5","6","7","8","9","10"]:
			j[0]=int(j[0])
		l2+=[{"valeur":j[0],"couleur":j[1]}]
	return l2

def ecrire_fichier_reussite(nom_fich,pioche):
	with open(nom_fich, "w") as fi:
		for i in pioche:
			fi.write(str(i["valeur"])+"-"+i["couleur"]+" ")

def init_pioche_alea(nb_cartes=32):
	va=[7,8,9,10,"R","D","V","A",2,3,4,5,6]
	co=["P","C","K","T"]
	c=[]
	for i in range(int(8+((nb_cartes-32)/4))):
		for j in range(4):
			c+=[{"valeur":va[i],"couleur":co[j]}]
	random.shuffle(c)
	return c

def alliance(card1, card2):
	return (card1["valeur"] == card2["valeur"] or card1["couleur"] == card2["couleur"])

def saut_si_possible(liste_tas, num_tas):
	if num_tas < len(liste_tas)-1 and num_tas > 0: #exclure les extrémités
		if liste_tas[num_tas-1]['valeur'] == liste_tas[num_tas+1]['valeur'] or \
			liste_tas[num_tas-1]['couleur'] == liste_tas[num_tas+1]['couleur']: #verifier la mm valeur/couleur
			liste_tas.pop(num_tas-1)
			return True
	return False

def une_etape_reussite(liste_tas, pioche, affiche=False):
	card = pioche.pop(0) # changer la carte de liste
	liste_tas.append(card)
	if affiche: afficher_reussite(liste_tas)
	if saut_si_possible(liste_tas, len(liste_tas)-2): # faire le saut
		if affiche: afficher_reussite(liste_tas)
	end = False
	while not end:
		i=0
		while i<len(liste_tas):
			if saut_si_possible(liste_tas,i): 
				if affiche: afficher_reussite(liste_tas)
				break
			if i>=len(liste_tas)-1: end = True
			i+=1

def pioche(liste_tas, pioche): #faire une simple pioche
	card = pioche.pop(0) # changer la carte de liste
	liste_tas.append(card)
	 
def reussite_mode_auto(pioche,affiche=False):
	pio=[]
	pio+=pioche
	if affiche==True:
		afficher_reussite(pioche) #on utilise afficher_reussite pour afficher la pioche 
	r=[]
	fin=False
	while fin!=True:
		une_etape_reussite(r,pio,affiche)
		if len(pio)==0:
			fin=True
	return r

def reussite_mode_manuel(pioche,nb_tas_max=2):
	pio=[]
	pio+=pioche
	r=[]
	fin=False
	print("poiche :",len(pio))
	while fin!=True:
		if len(pio)!=0:
			re=input("pioche(p) ou saut(s) : ")
		else:
			re=input("saut(s) ou stop : ")
		if re=="stop" or re=="Stop" or re=="STOP":
			fin=True
		elif re=="p" or re=="P":
			if len(pio)!=0:
				cart=pio.pop(0)
				r+=[cart]
			afficher_reussite(r)
			print("poiche :",len(pio))
		elif re=="s" or re=="S":
			afficher_reussite(r)
			print(" ",end="")
			for i in range(len(r)):
				if i<9:
					print(i,end="   ")
				else:
					print(i,end="  ")
			print()
			re=input("quelle saut ? : ")
			if re=="stop" or re=="Stop" or re=="STOP":
				fin=True
			elif saut_si_possible(r,int(re)):
				afficher_reussite(r)
				print("poiche :",len(pio))
			else:
				print("saut non possible !")
		else:
			print("mauvait choix !")
	if len(pioche)!=0:
		for i in pio:
			cart=pio.pop(0)
			r+=[cart]
			afficher_reussite(r)
			print("poiche :",len(pio))
	if len(r)<=nb_tas_max:
		print("GAGNER !!!")
	else:
		print("Perdu :(")
	return r

def lance_reussite(mode,nb_cartes=32,affiche=False,nb_tas_max=2):
	p=init_pioche_alea(nb_cartes)
	if mode=="manuel":
		reussite_mode_manuel(p,nb_tas_max)
	elif mode=="auto":
		reussite_mode_auto(p,affiche)

if __name__ == "__main__":
	print("Ce n'est pas ce fichier python qui doit être lancé!")
