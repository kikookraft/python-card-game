import fonctions as f

print("Bienvenue dans cette extension !\nLe but ici est de calculer la probabilité de gagner au jeu 'la réussite des alliances'")
fin=False
j=False
c="h"
print("Pour commencer voici toute les obtions :\nm : mode manuèle\na : mode automatique\ns : afficher vos statistiques\nf : mettre fin a se programme\nh : afficher les obtions possibles")
while not fin:
	c=input("Que voulez vous faire : ")
	if c not in "mash":
		fin=True
	elif c=="m":
		gagner=int(input("A combien de cartes restante a t'on gagner : "))
		if gagner<1:
			gagner=1
		p=f.init_pioche_alea()
		r=f.reussite_mode_manuel(p,gagner)
		with open("states.txt", "r") as fi:
			re=fi.readlines()
			re[0]=int(re[0][:-1])+1
			if len(r)<=gagner:
				re[1]=int(re[1])+1
		with open("states.txt", "w") as fi:
			x=str(re[0])+"\n"+str(re[1])
			fi.write(x)
	
	elif c=="a":
		n=int(input("Veuiller indiqué le nombre de simulations que vous souété calculer : "))
		if j==False and n>0:
			a=input("Voulez vous afficher les parties (cela peut vite envahir l'écrant) : ")
			if a=="Jamais" or a=="jamais" or a=="JAMAIS":
				j=True
			if a=="oui" or a=="Oui" or a=="OUI":
				a=True
			else:
				a=False
		gagner=int(input("A combien de cartes restante a t'on gagner : "))
		print("C'est partie !")
		ng=0
		for i in range(n):
			if not a:
				print("calcule en cours :",int(i/n*100)+1,"%")
			p=f.init_pioche_alea()
			r=f.reussite_mode_auto(p)
			if len(r)==gagner:
				ng+=1
			if a:
				f.afficher_reussite(r)
			elif i<n-1:
				print("\033[F",end="")
		print("nombre de victoires :",ng)
		if n>0:
			print("ceux qui fait",round(ng/n*100,2),"%")
	
	elif c=="s":
		with open("states.txt", "r") as fi:
			re=fi.readlines()
		print("nombre de partie faite :",re[0][:-1])
		print("nombre de victoire :",re[1])
		if re[0][:-1]!="0":
			print("pourcentage de victoire :",round(int(re[1])/int(re[0][:-1])*100,2),"%")
	
	elif c=="h":
		print("obtions :\nm : mode manuèle\na : mode automatique\ns : afficher vos statistiques\nf : mettre fin a se programme\nh : afficher les obtions possibles")
print("au revoir")
