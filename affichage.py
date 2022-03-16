##python 3.8.5, pygame 2.1.2 (SDL 2.0.18)

import pygame #2.1.2

class game():
    """Classe principale du jeu
    """
    def __init__(self):
        #variable générales
        self.screen_size=(1000,1000)
        self.w = self.screen_size[0]
        self.h = self.screen_size[1]
        self.bg_color='#141414'
        self.general_font = "res/font/UbuntuMono-Bold.ttf"
        self.is_running = True

        #variable de pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("res/bensound-dreams.mp3")
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
        pygame.key.set_repeat(600, 75)
        pygame.display.set_caption('jsp quoi mettre en titre')
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
        self.clicked_rect = {'id':None, 'data':None}
        self.rect_color = (90,90,90)
        self.test = False

        # variables des cartes
        self.cards = {}
        self.cards_id = []
        self.card_size = 0.5
        
        # pour le bouton qui se balade en mode test
        self.btn_x = 0
        self.btn_y = 0
        self.btn_text = "None"

        #variables menu
        self.show_menu = True


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
            self.cards[id] = {'file':file,'object':resized_img, 'pos':(0,0), 'size':1}
    
    def show_img_test(self):
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
        self.show_img_test()
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
            self.cursor_pos =  pygame.mouse.get_pos()
            pos_x = self.cursor_pos[0]
            pos_y = self.cursor_pos[1]
            if pos_x>self.rect[rect]['pos'][0]-self.rect[rect]['size'][0]/2 and pos_x<self.rect[rect]['pos'][0]+self.rect[rect]['size'][1] and \
                pos_y>self.rect[rect]['pos'][1]-self.rect[rect]['size'][1]/2 and pos_y<self.rect[rect]['pos'][1]+self.rect[rect]['size'][1]/2: #changer la couleur du bouton quand la souris passe desssus
                self.rect[rect]['color'] = (150,150,150)
                if self.click:
                    self.clicked_rect=rect
            else: #réinitialiser la couleur du rectangle
                self.rect[rect]['color'] = (90,90,90)
        for txt in self.texts: #afficher les textes
            self.window_surface.blit(self.texts[txt][0], self.texts[txt][1])
        if self.test: self.test_affichage(self.btn_x, self.btn_y,self.btn_text)
        pygame.display.update()
        pygame.display.flip()

    def test_affichage(self, x, y, text="Bouton"): #afficher le texte et le rectangle
        self.draw_rect("test", (x,y), (150, 80), self.rect_color)
        self.text((x,y), text, "test")

    def menu(self):
        pos = (self.w/2, self.h/8*3)
        self.draw_rect("play", pos, (150, 50), self.rect_color)
        self.text(pos, "JOUER", "play")
        pos = (self.w/2, self.h/2)
        self.draw_rect("opt", pos, (150, 50), self.rect_color)
        self.text(pos, "OPTIONS", "opt")
        pos = (self.w/2, self.h/8*5)
        self.draw_rect("quit", pos, (150, 50), self.rect_color)
        self.text(pos, "QUITTER", "quit")

class CARD:
    def __init__(self) -> None:
        self.color = None
        self.value = None
        self.posX = 0
        self.posY = 0
        self.size = 0
        self.hiden = False
        self.pioche = True
        self.img = 0

    # def generate_cards(self, nb_cards=52):
    #     # code repris en partie de res/imgs/rename.py
    #     suites = [ (0,'T'), (14, 'K'), (28, 'C'), (42, 'P') ]
    #     for start, suite in suites:
    #         for i in range(1,14):
    #             targ = str(i)
    #             if i == 1:
    #                 targ = 'A'
    #             elif i == 11:
    #                 targ = 'V'
    #             elif i == 12:
    #                 targ = 'D'
    #             elif i == 13:
    #                 targ = 'R'
    #             self.cards_id.append({'valeur':targ,'couleur':suite})
    #     # for i,c in [(56, 'J-N'), (57, 'J-R'), (58, 'dos')]:
    #     #     self.cards_id.append({'valeur':c,'couleur':None})
    
    def load_img(self, card):
        # exemple de la liste
        #card_list = [{"valeur":"7", "couleur":"P"}, {"valeur":"10", "couleur":"K"}, {"valeur":"D", "couleur":"K"}]
        self.color = card['couleur']
        self.value = card['valeur']
        self.file = "res/imgs/carte-{}-{}.gif".format(card['valeur'],card['couleur'])
        self.img = pygame.image.load(self.file).convert()

    
    def blit(self, surface):
        id = '{} {}'.format(self.value,self.color)
        resized_img = pygame.transform.smoothscale(self.img, (self.img.get_width()*self.size, self.img.get_height()*self.size))
        self.cards_id = {'file':self.file,'object':resized_img, 'pos':(self.posX,self.posY)}
        