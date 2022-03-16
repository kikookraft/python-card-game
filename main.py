# fichier principal
import pygame
import fonctions as f
import affichage as ui


game = ui.game()

def main_loop():
    game.__init__()
    game.refresh()
    game.menu()

    #pour le bouton de test
    x=75
    y=40
    x_status = 0
    y_status = 0
    txt = "Bouton de la mort"
    ##

    nb = 0
    while game.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #bouton 'X' de la fenetre
                game.is_running = False
            if event.type == pygame.KEYDOWN: #appui de touche
                if event.key == pygame.K_t: #touche espace
                    if game.test:
                        print("Désactivation du mode test")
                        game.test = False
                        # suprimmer le texte et rectangle 
                        game.rect.pop("test")
                        game.texts.pop("test")
                        game.cards.clear()
                        game.cards_id.clear()
                    else:
                        print("Activation du mode test")
                        game.test = True
                        game.generate_cards()
                        game.load_img(52, game.cards_id)
                if event.key == pygame.K_ESCAPE: #touche echap
                    print("quitter")
                    pygame.quit()
                    quit()
                if event.key == pygame.K_KP_PLUS and game.card_size < 1:
                    game.card_size+=0.1
                    game.cards.clear()
                    game.load_img(52, game.cards_id)
                if event.key == pygame.K_KP_MINUS and game.card_size > 0.3:
                    game.card_size-=0.1
                    game.cards.clear()
                    game.load_img(52, game.cards_id)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    game.click = True
        
        if game.click: #effectuer une action quand un click est fait
            if game.clicked_rect == "test" and game.test:
                game.rect_color = (90,90,90)
                nb+=1
                game.text((500,960), "Le bouton à été cliqué {} fois!".format(nb), 'info', size=42)
                game.click = False
            elif game.clicked_rect == "quit":
                pygame.quit()
                quit()
            elif game.clicked_rect == "opt":
                game.text((500,950), "Fonctionalitée pas encore implémentée!", "info")
                game.click = False
            elif game.clicked_rect == "play":
                game.text((500,50), "Lancement du jeux...", "loading")
                game.click = False
            game.clicked_rect= None
        
        ########################### code pour bouger le texte
        if game.test:
            if x+75<game.w and x_status==0:
                x+=3
            elif x+75 > game.w and x_status==0:
                x_status = 1
                txt="Bonsoir"
            elif x>75 and x_status==1:
                x-=3
            elif x<=75 and x_status==1:
                x_status=0
                txt="Bouton de la mort"

            if y+40<game.h and y_status==0:
                y+=2
            elif y+40 >= game.h and y_status==0:
                y_status = 1
                txt="Bouton"
            elif y>40 and y_status==1:
                y-=2
            elif y<=40 and y_status==1:
                y_status=0
                txt="DVD"

            game.btn_x = x
            game.btn_y = y
            game.btn_text = txt
        ###########################
        #if game.show_menu: game.menu()
        game.refresh()

if __name__ == "__main__":
    main_loop()