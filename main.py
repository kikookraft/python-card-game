# fichier principal
import fonctions as f

def main_loop():
    game.__init__()
    game.menu()
    player = ui.Player()
    game.refresh(player)

    click_time = 5

    while game.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #bouton 'X' de la fenetre
                game.is_running = False
            if event.type == pygame.KEYDOWN: #detecter les appui de touche
                if event.key == pygame.K_ESCAPE: #touche echap
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    game.click = True
        
        if game.click: #effectuer une action quand un click est fait
            if game.clicked_rect == "quit":
                pygame.quit()
                quit()
            # elif game.clicked_rect == "opt":
            #     game.text((game.w/2,950), "Fonctionalitée pas encore implémentée!", "info", time_duration=180)
            #     game.click = False
            elif game.clicked_rect == "play":
                game.text((game.w/2,50), "Choisissez le nombre de cartes", "choice")
                game.delete_menu()
                game.choose_nbCards=True
                game.card_choice_menu()
                game.click = False

            elif game.clicked_rect == "exit":
                game.win = False
                game.rect.clear()
                game.texts.clear()
                player.cards.clear()
                player.pioche.clear()
                game.text((game.w/2,50), "Choisissez le nombre de cartes", "choice")
                game.choose_nbCards=True
                game.card_choice_menu()
                game.click = False
        
            if game.choose_nbCards:  #pour l'écran de choix des cartes
                if game.clicked_rect == "52":
                    player.nbCard=52
                    game.clicked_rect = None
                    game.delete_choice_card()
                    player.init_pioche()
                    game.choose_nbCards = False
                elif game.clicked_rect == "32":
                    player.nbCard=32
                    game.clicked_rect = None
                    game.delete_choice_card()
                    player.init_pioche()
                    game.choose_nbCards = False
            game.clicked_rect= None

            if game.click:
                click_time-=1
                if click_time==0:
                    game.click = False
                    click_time=10
            elif not game.click and click_time!= 5:
                click_time=5
            # game.click=False

                
        #if game.show_menu: game.menu()
        game.refresh(player)

if __name__ == "__main__":
    print("\nBienvenue sur la resussite des alliance!\n\nQue souhaitez-vous faire?")
    print("  1 >> Jouer dans le terminal\n  2 >> Jouer avec une interface graphique\n  3 >> Ouvrir l'outils de statistiques")
    choice = input("Votre choix (1 ou 2 ou 3): ")

    if choice=="1":
        af = False
        print("\n\nChoisissez le mode je jeux:\n  1 >> Mode manuel\n  2 >> Mode auto")
        mod="0"
        while mod not in "12":
            mod = input("Mode: ")
        if mod=="1": mod="manuel"
        elif mod=="2":
            mod="auto"
            if input("Voulez-vous afficher les details?\nAfficher (oui/non): ").lower() == "oui":
                af = True
        print("\nChoisissez le nombres de cartes (32 ou 52)")
        nbcarte = 0
        while nbcarte!=32 and nbcarte!=52:
            nbcarte = int(input("Nombre: "))
        print("\n\n")
        f.lance_reussite(mod, nbcarte, af)

    elif choice=="2":
        import pygame
        import affichage as ui
        game = ui.game()
        main_loop()

    elif choice=="3":
        print("\n\n")
        import Statistique

    else:
        print("Choix incorect!")
    exit()