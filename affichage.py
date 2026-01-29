##python 3.8.5, pygame 2.1.2 (SDL 2.0.18)

from time import time
import pygame #2.1.2
import fonctions as f

class game():
    """Classe principale du jeu
    """
    def __init__(self):
        #variable générales
        self.screen_size=(1500,1000)
        self.w = self.screen_size[0]
        self.h = self.screen_size[1]
        self.bg_color='#141414'
        self.general_font = "res/font/UbuntuMono-Bold.ttf"
        self.is_running = True
        self.time_cheat= 0
        self.cheat = False

        #variable de pygame
        pygame.init()
        pygame.display.set_caption('La réussite des alliances')
        self.background = pygame.Surface(self.screen_size)
        self.clock = pygame.time.Clock()
        self.background.fill(pygame.Color(self.bg_color))
        self.window_surface = pygame.display.set_mode(self.screen_size)
        self.font = pygame.font.SysFont(self.general_font, 24)
        game.clock = pygame.time.Clock()

        #variable pour les textes et rectangles
        self.texts = {}
        self.rect = {}
        self.tick = 0
        self.FPS = 60
        self.cursor_pos = None
        self.click = False
        self.clicked_rect = ""
        self.rect_color = (90,90,90)
        self.test = False
        
        #variables menu
        self.show_menu = True
        self.choose_nbCards = False
        self.win = False

    def bezier(self, x): #utile pour faire de petites animation de position/couleurs
        """Prends en argument et retourne un nombre flottant
        (compris entre 0 et 1)
        """
        return x**2*(3-2*x)
    
    def text(self, pos, text, id, color=(255,255,255), size=24, centered=True, time_duration=-1):
        """Génère les textes et les ajoutes dans la liste d'objets a rendre
        Args:
            pos (tuple): Position en `x` et `y` 
            text (str): Texte a afficher
            id (str|int): l'id sous lequel le texte sera enregistré
            color (tuple, optional): Couleur au format RGB.\n Par defaut: (255,255,255) (blanc).
            size (int, optional): Taille du texte. DPar defaut: 24.
            centered (bool, optional): Pour centrer (ou décentrer) le texte. Par defaut: True.
            time_duration (int, optional) temps en frame durant laquelle le texte sera affiché (-1 pour infinis)
        Returns:
            int: id de l'objet créé
        """
        ft = pygame.font.SysFont(self.general_font, size)
        tx = ft.render(text, True, color)
        txt_size = ft.size(text)
        if centered and time_duration!=0:
            self.texts[str(id)]={'text':tx, 'pos':(pos[0]-(txt_size[0]/2), pos[1]-(txt_size[1]/2)), 'size':txt_size, 'time':time_duration}
        else:
            self.texts[str(id)]={'text':tx, 'pos':(pos[0], pos[1]),'size':txt_size, 'time':time_duration}
        return str(id)
        
    def draw_rect(self, id, pos, size, color=(90,90,90), keep_ratio = False):
        """Dessiner les differents boutons
        Args:
            id (str|int): id de la surface
            pos (tuple->float): position en x et y
            size (tuple->int): Taille
            color (tuple, optional): couleur RGB. Defaults to (50,50,50).
            keep_ratio (bool, optional): Garder le format carré avec le redimensionnement. Defaults to False.
        Returns:
            int: id de l(objet créé)
        """
        self.rect[str(id)] = {'pos':pos, 'size':size, 'color':color, 'ratio':keep_ratio, 'id':id, 'default_color':color}
        return str(id)


    def refresh(self, player): #fonction qui met a jour les position des objets contenus dans 'rect' et 'texts'
        """Permet de mettre a jour l'ecran et les objets"""
        self.window_surface.blit(self.background, (0, 0))
        self.tick += 1
        self.cursor_pos =  pygame.mouse.get_pos()
        pos_x = self.cursor_pos[0]
        pos_y = self.cursor_pos[1]
        for rect in self.rect: #afficher chaque surface
            if self.rect[rect]['ratio']: #si l'objet contient ratio a True on affiche un carré
                x= self.rect[rect]['pos'][0] - self.rect[rect]['size'][1]/2 ## centrer en x
                y= self.rect[rect]['pos'][1] - self.rect[rect]['size'][1]/2 ## centrer en y
                box = pygame.Rect(x, y, self.rect[rect]['size'][1], self.rect[rect]['size'][1])
            else:
                x= self.rect[rect]['pos'][0] - self.rect[rect]['size'][0]/2 ## centrer en x
                y= self.rect[rect]['pos'][1] - self.rect[rect]['size'][1]/2 ## centrer en y
                box = pygame.Rect(x, y, self.rect[rect]['size'][0], self.rect[rect]['size'][1])
            pygame.draw.rect(self.window_surface, self.rect[rect]['color'], box)

            #detecter click de souris
            if pos_x>self.rect[rect]['pos'][0]-self.rect[rect]['size'][0]/2 and pos_x<self.rect[rect]['pos'][0]+self.rect[rect]['size'][1] and \
                pos_y>self.rect[rect]['pos'][1]-self.rect[rect]['size'][1]/2 and pos_y<self.rect[rect]['pos'][1]+self.rect[rect]['size'][1]/2: #changer la couleur du bouton quand la souris passe desssus
                self.rect[rect]['color'] = (150,150,150)
                if self.click:
                    self.clicked_rect=str(rect)
            else: #réinitialiser la couleur du rectangle
                self.rect[rect]['color'] = self.rect[rect]['default_color']
        
        if player.cards != []:
            if len(player.cards)>2 or len(player.pioche)>0:
                self.show_card(player)
            elif not self.win:
                self.winning(player)
                self.win = True
                self.cheat = False
                self.time_cheat = 0
        if player.pioche != []: #affichage des cartes
            self.window_surface.blit(player.carte_dos, (15,15))
            if self.click and (pos_x>15 and pos_x<15+player.siz[0] and pos_y>15 and pos_y<15+player.siz[1]):
                self.click = False
                f.pioche(player.cards, player.pioche)

        for txt in list(self.texts): #afficher les textes
            self.window_surface.blit(self.texts[txt]['text'], self.texts[txt]['pos'])
            if self.texts[txt]['time'] == 0: self.texts.pop(txt) #si le texte est temporaire, verifier si le temps est écoulé
            else: self.texts[txt]['time']-=1
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.FPS) #limiter la fréquence d'affichage

    def show_card(self, player):
        """Affiche les cartes du joueur de manière dynamique"""
        nbCartes=len(player.cards)

        if self.click and self.clicked_rect=="cheat": #option triche qui permet de tester le menu de victoire
            self.click = False
            self.clicked_rect = None
            self.cheat=True
            player.tmp=nbCartes+len(player.pioche)-1
            if player.pioche !=[]:
                self.time_cheat=180
            else:
                self.time_cheat=0
        if self.cheat:
            self.time_cheat-=1
            if player.pioche !=[]:
                f.pioche(player.cards, player.pioche)
            if self.tick%5==0 and player.pioche==[] and self.time_cheat<=0:
                if player.tmp>=2:
                    i=player.tmp
                    player.tmp-=1
                    player.cards[i]['exit']=True
                    player.cards[i]['anim']=True
                    player.cards[i]['end_pos']=player.cards[i]['pos'][0],self.h+200
                    player.cards[i]['end_frame']=self.tick+60

        cardShift=12
        marge = 10
        line=0
        line2=0
        line3=0
        line4=0
        line5=0
        if nbCartes<=cardShift*2: #detecter si une 2eme ligne est necessaire
            line = 1
            line2=nbCartes-cardShift
        elif nbCartes>cardShift*2:
            line = 2
            line2=cardShift
            if nbCartes<=cardShift*3:
                line3=nbCartes-2*cardShift
            else:
                line=3
                line3=cardShift
                if nbCartes<=cardShift*4:
                    line4=nbCartes-3*cardShift
                else:
                    line=4
                    line4=cardShift
                    line5=nbCartes-4*cardShift
        anim_time = self.FPS #temps d'animation en frames (60=1sec a 60FPS)
        sX=player.cards[0]['surface'].get_width() # largeur de la carte
        sY=player.cards[0]['surface'].get_height() #hauteur de la carte

        if nbCartes<cardShift: #permet de bien gerer les position de debut des lignes
            pX=(self.w/2-(((nbCartes%cardShift)*sX+(nbCartes-1)*marge))/2) #position x de la 1ere carte de la ligne
        else:
            pX=(self.w/2-((cardShift*sX+(cardShift-1)*marge))/2)
            if line2<cardShift:
                pX2=(self.w/2-(((line2%cardShift-1)*sX+(nbCartes-1)*marge))/2) #position x de la 1ere carte de la 2eme ligne
            else:
                pX2=(self.w/2-((cardShift*sX+(cardShift-1)*marge))/2)
                if line3<cardShift:
                    pX3=(self.w/2-(((line3%cardShift-line-1)*sX+(nbCartes-1)*marge))/2)
                else:
                    pX3=(self.w/2-((cardShift*sX+(cardShift-1)*marge))/2)
                    if line4<cardShift:
                        pX4=(self.w/2-(((line4%cardShift-line-1)*sX+(nbCartes-1)*marge))/2)
                    else:
                        pX4=(self.w/2-((cardShift*sX+(cardShift-1)*marge))/2)
                        if line5<cardShift:
                            pX5=(self.w/2-(((line5%cardShift-line-1)*sX+(nbCartes-1)*marge))/2)
                        else:
                            pX5=(self.w/2-((cardShift*sX+(cardShift-1)*marge))/2)
        pY=self.h/2 - (sY/2)*line -sY/2
        increment_X=sX+marge
        increment_Y=sY+marge
        cardToPOP=None # variable qui sert a stocker la carte a enlever
        # afin de le faire hors de la boucle for
        restant=len(player.pioche)
        if restant>0:
            rest_color= ((1-restant/player.nbCard)*255, (restant/player.nbCard)*255,50)
            self.text((increment_X/2+marge, increment_Y+marge*2), "Restant: {}".format(restant), "nbpioche", rest_color, time_duration=120)

        for i in range(nbCartes): #pour cahque carte:
            cardposX=pX
            player.cards[i]['line'] = i//cardShift #assigner chaque carte a la bonne ligne
            # et a la bonne position
            if line==1 and i>=cardShift:
                player.cards[i]['line'] = 1
                cardposX=pX2
            elif line==2:
                if i>=cardShift and i<cardShift*2:
                    player.cards[i]['line'] = 1
                    cardposX=pX2
                elif i>=cardShift*2:
                    player.cards[i]['line'] = 2
                    cardposX=pX3
            elif line==3:
                if i>=cardShift*2 and i<cardShift*3:
                    player.cards[i]['line'] = 2
                    cardposX=pX3
                elif i>=cardShift*3:
                    player.cards[i]['line'] = 3
                    cardposX=pX4
            elif line==4:
                if i>=cardShift*3 and i<cardShift*4:
                    player.cards[i]['line'] = 3
                    cardposX=pX4
                elif i>=cardShift*4:
                    player.cards[i]['line'] = 4
                    cardposX=pX5

            theCard = player.cards[i]
            if theCard['pioched']: # si la carte est piochée, mettre a droite
                player.cards[i]['pioched']=False
                player.cards[i]['anim']=True #demarer animation
                player.cards[i]['end_frame']=self.tick+anim_time #définir a quel moment la carte arrete l'anim
                player.cards[i]['end_pos']=cardposX+(i%cardShift)*increment_X, pY+theCard['line']*increment_Y #position de fin de la carte
            if (theCard['pos'][0] != cardposX+(i%cardShift)*increment_X or theCard['pos'][1] != pY+theCard['line']*increment_Y) and theCard['end_frame']-self.tick<anim_time-self.FPS/2 and not theCard['exit']: #si la carte n'est pas a la bonne position: rebouger la carte
                player.cards[i]['anim']=True
                player.cards[i]['end_frame']=self.tick+anim_time
                player.cards[i]['end_pos']=cardposX+(i%cardShift)*increment_X, pY+theCard['line']*increment_Y
            if theCard['anim']:
                time_left= (theCard['end_frame']-self.tick)/anim_time #completion de l'animation (en flottant: 0.0=0% -> 1.0=100%)
                end_X= theCard['end_pos'][0]-(theCard['end_pos'][0]-theCard['pos'][0])*self.bezier(time_left) #formule pour l'animation de la carte
                end_Y= theCard['end_pos'][1]-(theCard['end_pos'][1]-theCard['pos'][1])*self.bezier(time_left) #permet de faire glisser du point A au point B de manière fluide
                player.cards[i]['pos'] = (end_X, end_Y)
                if player.cards[i]['pos']==player.cards[i]['end_pos']:
                    player.cards[i]['anim'] = False
                    if player.cards[i]['exit']:
                        cardToPOP=i

            if self.click:
                inside_x = self.cursor_pos[0]>theCard['pos'][0] and self.cursor_pos[0]<theCard['pos'][0]+sX
                inside_y = self.cursor_pos[1]>theCard['pos'][1] and self.cursor_pos[1]<theCard['pos'][1]+sY
                if inside_x and inside_y:
                    self.text((self.w/2, 30), "Carte selectionné: {}{}".format(theCard['valeur'],theCard['couleur']), "sel", time_duration=120)
                    self.click = False
                    if f.saut_si_possible(list(player.cards), i): #créer l'animation de sortie de la carte
                        player.cards[i]['exit']=True
                        player.cards[i]['anim']=True
                        player.cards[i]['end_pos']=theCard['end_pos'][0],self.h+2*sY
                        player.cards[i]['end_frame']=self.tick+anim_time
            self.window_surface.blit(theCard['surface'], theCard['pos'])
        if cardToPOP != None:
            player.cards.pop(cardToPOP)

    def winning(self, player):
        self.text((self.w/2,self.h/2), "TU AS GAGNÉ !", "win", (100,255,50), 75)

    def menu(self): #afficher le menu)
        self.text((self.w/2, 100), "La réussite des alliances", "title", size=75)
        pos = (self.w/2, self.h/8*3)
        self.draw_rect("play", pos, (150, 50), self.rect_color)
        self.text(pos, "JOUER", "play")
        pos = (self.w/2, self.h/8*5)
        self.draw_rect("quit", pos, (150, 50), self.rect_color)
        self.text(pos, "QUITTER", "quit")
    
    def delete_menu(self): #arreter d'afficher le menu
        self.texts.pop("title")
        self.rect.pop("play")
        self.texts.pop("play")
        self.rect.pop("quit")
        self.texts.pop("quit")

    def card_choice_menu(self): #afficher menu de choix du nombre de cartes
        pos = (self.w/2, self.h/16*7)
        self.draw_rect("52", pos, (150, 50), self.rect_color)
        self.text(pos, "52 CARTES", "52")
        pos = (self.w/2, self.h/16*9)
        self.draw_rect("32", pos, (150, 50), self.rect_color)
        self.text(pos, "32 CARTES", "32")

    def delete_choice_card(self): #suprimmer le menu de choix des cartes
        self.rect.pop("52")
        self.rect.pop("32")
        self.texts.pop("52")
        self.texts.pop("32")
        self.texts.pop("choice")
        #quand ce menu est suprimmé, afficher les bouton suplementaires
        self.draw_rect("cheat", (self.w-50, 25), (100,50), (20,20,20))
        self.text((self.w-50, 25), "TRICHE", "cheat", (20,20,20))
        self.draw_rect("exit", (self.w-85, self.h-35), (150,50))
        self.text((self.w-85,self.h-35), "RECOMMENCER", "exit")
        

class Player:
    def __init__(self):
        self.nbCard = 32
        self.cards = []
        self.pioche = []
        self.card_size = 0.5
        file = "res/imgs/carte-dos.gif"
        img = pygame.image.load(file).convert()
        self.siz = (img.get_width()*self.card_size, img.get_height()*self.card_size)
        self.carte_dos = pygame.transform.smoothscale(img, self.siz)
        self.tmp=0

    def init_pioche(self):
        self.pioche =  f.init_pioche_alea(self.nbCard)

        #ajouter les attribus d'affichage au dico
        for i in range(len(self.pioche)):
            self.pioche[i]['pos']=(15,15)
            self.pioche[i]['index']=0
            self.pioche[i]['size']= self.card_size
            self.pioche[i]['anim']=False
            self.pioche[i]['end_pos']=(0,0)
            self.pioche[i]['end_frame']=0
            self.pioche[i]['pioched']=True
            self.pioche[i]['line']=0
            self.pioche[i]['file'], self.pioche[i]['surface']=self.load_img(self.pioche[i])
            self.pioche[i]['exit']=False
        
    def load_img(self, card):
        # exemple de la liste
        #card_list = [{"valeur":"7", "couleur":"P"}, {"valeur":"10", "couleur":"K"}, {"valeur":"D", "couleur":"K"}]
        color = card['couleur']
        value = card['valeur']
        file = "res/imgs/carte-{}-{}.gif".format(value,color)
        img = pygame.image.load(file).convert()
        resized_img = pygame.transform.smoothscale(img, (img.get_width()*card['size'], img.get_height()*card['size']))
        return file, resized_img

    def update_size(self, card):
        idx = card["index"]
        self.pioche[idx]['file'], self.pioche[idx]['surface']=self.load_img(self.pioche[idx])

