# le fichier qui contient toutes les fonctions
import random 

def test():
    print("C'est ok !")

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
		print(carte_to_chaine(i))
		if i!=(len(l)-1):
			print(" ")
	print("\n\n")

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
    return card1["valeur"] == card2["valeur"]

def saut_si_possible(liste_tas, num_tas):
    if num_tas < len(liste_tas)-1 and num_tas > 0: #exclure les extrémités
        if liste_tas[num_tas-1]['valeur'] == liste_tas[num_tas+1]['valeur'] or \
            liste_tas[num_tas-1]['couleur'] == liste_tas[num_tas+1]['couleur']: #verifier la mm valeur/couleur
            return True
    return False

def une_etape_reussite(liste_tas, pioche, affiche=False):
    card = pioche.pop()
    liste_tas.append(card)
    if saut_si_possible(liste_tas, len(liste_tas)-2):
        pass



if __name__ == "__main__":
    print("Ce n'est pas ce fichier python qui doit être lancé!")
