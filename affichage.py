##python 3.8.5, pygame 2.1.2 (SDL 2.0.18)

# --- BUGS ---
# R.A.S
# -- TACHES --
# > Fonction pour importer les cartes (depuis res/imgs/XX.gif )
# > Fonction pour afficher carte (stockés dans un dic) 
# > Structurer le menu
# > Transformer le programme en classe pour être appelé par main.py
# 
# > Dormir 
#

import pygame #2.1.2
import random

class game():
    """Classe principale du jeu
    """
    def __init__(self):
        self.screen_size=(1000,1000)
        self.w = self.screen_size[0]
        self.h = self.screen_size[1]
        self.bg_color='#141414'
        self.general_font = "res/font/UbuntuMono-Bold.ttf"
        self.is_running = True
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("res/bensound-dreams.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        pygame.key.set_repeat(600, 75)
        pygame.display.set_caption('jsp quoi mettre en titre')
        self.background = pygame.Surface(self.screen_size)
        self.clock = pygame.time.Clock()
        self.background.fill(pygame.Color(self.bg_color))
        self.window_surface = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.font = pygame.font.SysFont(self.general_font, 24)
        game.clock = pygame.time.Clock()
        self.texts = {}
        self.rect = {}
        self.tick = 0
        self.FPS = 60
        self.cursor_pos = None
        self.click = False
        self.clicked_rect = {'id':None, 'data':None}
        self.rect_color = (90,90,90)

        # variables des cartes
        self.cards = {}
        self.cards_id = []
        self.card_size = 0.5
        
        # pour le bouton qui se balade
        self.btn_x = 0
        self.btn_y = 0
        self.btn_text = "None"


    def beizer(self, x): #utile pour faire de petites animation de position/couleurs
        return x**2*(3-2*x)
    
    def generate_cards(self, nb_cards=52):
        # code repris en partie de res/imgs/rename.py
        suites = [ (0,'T'), (14, 'K'), (28, 'C'), (42, 'P') ]
        for start, suite in suites:
            for i in range(1,14):
                targ = str(i)
                if i == 1:
                    targ = 'A'
                elif i == 11:
                    targ = 'V'
                elif i == 12:
                    targ = 'D'
                elif i == 13:
                    targ = 'R'
                self.cards_id.append({'valeur':targ,'couleur':suite})
        # for i,c in [(56, 'J-N'), (57, 'J-R'), (58, 'dos')]:
        #     self.cards_id.append({'valeur':c,'couleur':None})
    
    def load_img(self, nb_cartes=52, card_list=[]):
        # exemple de la liste
        #card_list = [{"valeur":"7", "couleur":"P"}, {"valeur":"10", "couleur":"K"}, {"valeur":"D", "couleur":"K"}]
        for card in card_list:
            file = "res/imgs/carte-{}-{}.gif".format(card['valeur'],card['couleur'])
            id = '{} {}'.format(card['valeur'],card['couleur'])
            img = pygame.image.load(file).convert()
            resized_img = pygame.transform.smoothscale(img, (img.get_width()*self.card_size, img.get_height()*self.card_size))
            self.cards[id] = {'file':file,'object':resized_img}
    
    def show_img(self):
        x=10
        y=10
        for card in self.cards:
            self.window_surface.blit(self.cards[card]['object'], (x,y))
            x+= self.cards[card]['object'].get_width() + 10
            if x+self.cards[card]['object'].get_width() + 10 > self.w: # si les images dépassent de l'écran
                x=10
                y+= self.cards[card]['object'].get_height() +10
    
    def text(self, pos, text, id, color=(255,255,255), size=24, centered=True):
        """Génère les textes et les ajoutes dans la liste d'objets a rendre
        Args:
            pos (tuple): Position en `x` et `y` 
            text (str): Texte a afficher
            id (str|int): l'id sous lequel le texte sera enregistré
            color (tuple, optional): Couleur au format RGB.\n Par defaut: (255,255,255) (blanc).
            size (int, optional): Taille du texte. DPar defaut: 24.
            centered (bool, optional): Pour centrer (ou décentrer) le texte. Par defaut: True.
        Returns:
            int: id de l'objet créé
        """
        ft = pygame.font.SysFont(self.general_font, size)
        tx = ft.render(text, True, color)
        txt_size = ft.size(text)
        if centered:
            self.texts[str(id)]=(tx, (pos[0]-(txt_size[0]/2), pos[1]-(txt_size[1]/2)), txt_size)
        else:
            self.texts[str(id)]=(tx, (pos[0], pos[1]))
        return str(id)
        
    def draw_rect(self, id, pos, size, color=(50,50,50), keep_ratio = False):
        """Dessiner la grille
        Args:
            id (str|int): id de la surface
            pos (tuple->float): position en x et y
            size (tuple->int): Taille
            color (tuple, optional): couleur RGB. Defaults to (50,50,50).
            keep_ratio (bool, optional): Garder le format carré avec le redimensionnement. Defaults to False.
        Returns:
            int: id de l(objet créé)
        """
        self.rect[str(id)] = {'pos':pos, 'size':size, 'color':color, 'ratio':keep_ratio, 'id':id}
        return str(id)

    def refresh(self): #fonction qui met a jour les position des objets contenus dans 'rect' et 'texts'
        self.window_surface.blit(self.background, (0, 0))
        self.tick += 1
        self.clock.tick(self.FPS)
        self.show_img()
        for rect in self.rect: #afficher chaque surface
            if self.rect[rect]['ratio']: #si l'objet contient ratio a True on affiche un carré
                x= self.rect[rect]['pos'][0] - self.rect[rect]['size'][1]/2 ## centrer en x
                y= self.rect[rect]['pos'][1] - self.rect[rect]['size'][1]/2 ## centrer en y
                box = pygame.Rect(x, y, self.rect[rect]['size'][1], self.rect[rect]['size'][1])
            else:
                x= self.rect[rect]['pos'][0] - self.rect[rect]['size'][0]/2 ## centrer en x
                y= self.rect[rect]['pos'][1] - self.rect[rect]['size'][1]/2 ## centrer en y
                box = pygame.Rect(x, y, self.rect[rect]['size'][0], self.rect[rect]['size'][1])
            color = self.rect[rect]['color']
            pygame.draw.rect(self.window_surface, color, box)
            #detecter click de souris
            self.cursor_pos =  pygame.mouse.get_pos()
            pos_x = self.cursor_pos[0]
            pos_y = self.cursor_pos[1]
            if pos_x>self.rect[rect]['pos'][0]-self.rect[rect]['size'][0]/2 and pos_x<self.rect[rect]['pos'][0]+self.rect[rect]['size'][1] and \
                pos_y>self.rect[rect]['pos'][1]-self.rect[rect]['size'][1]/2 and pos_y<self.rect[rect]['pos'][1]+self.rect[rect]['size'][1]/2: #changer la couleur du bouton quand la souris passe desssus
                self.rect_color = (150,150,150)
                if self.click:
                    self.clicked_rect=rect
            else: #réinitialiser la couleur du rectangle
                self.rect_color=(90,90,90)
        for txt in self.texts: #afficher les textes
            self.window_surface.blit(self.texts[txt][0], self.texts[txt][1])
        self.test_affichage(self.btn_x, self.btn_y,self.btn_text)
        pygame.display.flip()

    def test_affichage(self, x, y, text="Bouton"): #afficher le texte et le rectangle
        self.draw_rect("test", (x,y), (150, 80), self.rect_color)
        self.text((x,y), text, "azertyui")
        

if __name__ == "__main__":
    G = game()
    G.refresh()

    x=75
    y=40
    x_status = 0
    y_status = 0
    txt = "Bouton de la mort"
    nb = 0
    G.generate_cards()
    G.load_img(52, G.cards_id)

    while G.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #bouton 'X' de la fenetre
                G.is_running = False
            if event.type == pygame.KEYDOWN: #appui de touche
                if event.key == pygame.K_SPACE: #touche espace
                    print("pas encore implémenté")
                if event.key == pygame.K_ESCAPE: #touche echap
                    pygame.quit()
                    quit()
                if event.key == pygame.K_KP_PLUS and G.card_size < 1:
                    G.card_size+=0.1
                    G.cards.clear()
                    G.load_img(52, G.cards_id)
                if event.key == pygame.K_KP_MINUS and G.card_size > 0.3:
                    G.card_size-=0.1
                    G.cards.clear()
                    G.load_img(52, G.cards_id)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    G.click = True
        
        if G.click: #effectuer une action quand un click est fait
            if G.clicked_rect == "test":
                G.rect_color = (90,90,90)
                nb+=1
                G.text((500,960), "Le bouton à été cliqué {} fois!".format(nb), 'info', size=42)
                G.click = False
        
        ########################### code pour bouger le texte
        if x+75<G.w and x_status==0:
            x+=3
        elif x+75 > G.w and x_status==0:
            x_status = 1
            txt="Bonsoir"
        elif x>75 and x_status==1:
            x-=3
        elif x<=75 and x_status==1:
            x_status=0
            txt="Bouton de la mort"

        if y+40<G.h and y_status==0:
            y+=2
        elif y+40 >= G.h and y_status==0:
            y_status = 1
            txt="Bouton"
        elif y>40 and y_status==1:
            y-=2
        elif y<=40 and y_status==1:
            y_status=0
            txt="DVD"
        ###########################
        G.btn_x = x
        G.btn_y = y
        G.btn_text = txt

        G.refresh()