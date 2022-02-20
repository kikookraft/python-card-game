# le fichier qui contient toutes les fonctions

def test():
    print("C'est ok !")


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
        



if __name__ == "__main__":
    print("Ce n'est pas ce fichier python qui doit être lancé!")