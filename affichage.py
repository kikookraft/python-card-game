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
        self.window_surface = pygame.display.set_mode(self.screen_size)
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

    def beizer(self, x): #utile pour faire de petites animation de position/couleurs
        return x**2*(3-2*x)

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
        G.test_affichage(x,y, txt)

        G.refresh()