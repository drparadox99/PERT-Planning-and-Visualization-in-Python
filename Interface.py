import pygame
from math import pi
import random

class Interface_Graphique:
    def __init__(self,titre,LARGEUR_ECRAN,LONGEUR_ECRAN):

        # Initialisation du module
        pygame.init()
        pygame.display.set_caption(titre)

        # Defintion des coouleurs dans un format RBG
        self.couleurs = {"NOIR":(  0,   0,   0),"BLANC":(255, 255, 255),"BLEU": (  0,   0, 255),"VERT": (  0, 255,   0),"ROUGE": (255,   0,   0), "MAUVE_CLAIR":(255,204,229) }

        # Definition des dimensions de l'écran
        #dimensions = [1300, 300]
        self.dimensions = [LARGEUR_ECRAN, LONGEUR_ECRAN]
        self.ecran = pygame.display.set_mode(self.dimensions)

        #paramétrages relatives à l'affichage
        self.affichage = True
        self.clock = pygame.time.Clock()
        self.fontRenderer = pygame.font.Font('assets/fonts/font3.ttf', 15)
        self.fonts = [self.fontRenderer.render("22",True,(0,0,0)),self.fontRenderer.render("22",True,(0,0,0)),self.fontRenderer.render("22",True,(0,0,0))]

    def retourneFont(self,text):
        return self.fontRenderer.render(text,True,(0,0,0))


    def gererEvenements(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                self.affichage = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pygame.quit()

    #Trace le graphique (les étapes, les tâches et les poids)
    def dessiner(self,pert):
        lstPoids = []
        #tracage de la première étape
        ALLEtapes = pert.recupererEtapes()
        #doit forcement être la première étape créee
        premiereEtape = ALLEtapes.pop(0)
        doublon = False
        premiereEtape.circle = circle = pygame.draw.circle(self.ecran, self.couleurs['MAUVE_CLAIR'],[premiereEtape.coordonnees["x"], premiereEtape.coordonnees["y"]],premiereEtape.coordonnees["rayon"])
        pygame.draw.line(self.ecran, self.couleurs['BLANC'], [circle.midleft[0], circle.midleft[1]],[circle.midright[0], circle.midright[1]])
        pygame.draw.line(self.ecran, self.couleurs['BLANC'], [circle.center[0], circle.center[1]],[circle.bottomleft[0] + (circle.width / 2), circle.center[1] + (circle.height / 2)])
        self.ecran.blit(self.retourneFont(str(premiereEtape.nombre)),(circle.center[0] - 10, circle.center[1] - 20))
        if pert.affichage_partielle['dates']:
            if pert.affichage_partielle['dates_plut_tot']:
                self.ecran.blit(self.retourneFont(str(premiereEtape.etapes["plus_tot"]) ), (circle.center[0] - 22, circle.center[1] + 3))
            if pert.affichage_partielle['dates_plus_tard']:
                self.ecran.blit(self.retourneFont(str(premiereEtape.etapes["plus_tard"]) ), (circle.center[0] + 3, circle.center[1] + 3))

        #affichage du reste du diagramme de PERT
        for etape in ALLEtapes:
            #objet = pert.associassionObjets[t]
            etape.circle = circle = pygame.draw.circle(self.ecran, self.couleurs['MAUVE_CLAIR'],[etape.coordonnees["x"], etape.coordonnees["y"]],etape.coordonnees["rayon"])

            pygame.draw.line(self.ecran, self.couleurs['BLANC'], [circle.midleft[0], circle.midleft[1]],[circle.midright[0], circle.midright[1]])
            pygame.draw.line(self.ecran, self.couleurs['BLANC'], [circle.center[0], circle.center[1]],[circle.bottomleft[0] + (circle.width / 2), circle.center[1] + (circle.height / 2)])
            self.ecran.blit(self.retourneFont(str(etape.nombre) ),(circle.center[0] - 10, circle.center[1] - 20))
            if pert.affichage_partielle['dates']:
                if pert.affichage_partielle['dates_plut_tot']:
                    self.ecran.blit(self.retourneFont(str(etape.etapes["plus_tot"])), (circle.center[0] - 22, circle.center[1] + 3))
                if pert.affichage_partielle['dates_plus_tard']:
                    self.ecran.blit(self.retourneFont(str(etape.etapes["plus_tard"])), (circle.center[0] + 3, circle.center[1] + 3))

        ALLEtapes.insert(0,premiereEtape)
        for etape in ALLEtapes:
            circle_1 = etape.circle
            for tache in etape.lstTachesSortantes:
                circle_2 = tache.dates_fin.circle
                if etape.etapes["plus_tot"] - etape.etapes["plus_tard"] == 0 and tache.dates_fin.etapes["plus_tot"] - tache.dates_fin.etapes["plus_tard"] == 0 and pert.affichage_partielle['dates_plut_tot'] and pert.affichage_partielle['dates_plus_tard'] and pert.calcul_chemin_critique :
                    line = pygame.draw.line(self.ecran, etape.couleur_tache_sortante["ROUGE"], [circle_1.midright[0],circle_1.midright[1]], [circle_2.midleft[0], circle_2.midleft[1]],4)
                else:
                    line = pygame.draw.line(self.ecran, etape.couleur_tache_sortante["VERT"], [circle_1.midright[0],circle_1.midright[1]], [circle_2.midleft[0], circle_2.midleft[1]],4)
                if line in lstPoids:
                    doublon = True

                lstPoids.append(line)
                if doublon:
                    self.ecran.blit(self.retourneFont( tache.nom + " ( " + str(tache.duree_tache) + " ) " ), (line.center[0] - 10, line.center[1] - 40))
                    doublon = False
                else:
                    self.ecran.blit(self.retourneFont( tache.nom + " ( " + str(tache.duree_tache) + " ) " ), (line.center[0] - 10, line.center[1] - 20))

    #Positionnement des étapes et des tâches de façon aléatoire à chaque exécution
    def creerEtapes(self,pert,lstEtapes):
            etape_debut_actuelle = ""
            etape_fin_actuelle = ""
            espacement_y = 80
            placement_x = 200
            y_c = 120

            for indice_niveau, niveau in enumerate(pert.tabNiveaux):
                if indice_niveau == 0:
                    tache = pert.associassionObjets[niveau[0]]
                    tache.dates_debut.coordonnees["x"],tache.dates_debut.coordonnees["y"],tache.dates_debut.coordonnees["rayon"] = 30, 300,30
                    #x,y,rayon = etape_debut_actuelle.coordonnees["x"],etape_debut_actuelle.coordonnees["y"],etape_debut_actuelle.coordonnees["rayon"]
                    #self.dessiner(tache)

                for t in niveau:
                    tache = pert.associassionObjets[t]
                    tache.dates_fin.coordonnees["x"],tache.dates_fin.coordonnees["y"],tache.dates_fin.coordonnees["rayon"] =  tache.dates_debut.coordonnees["x"]  + placement_x, y_c ,tache.dates_debut.coordonnees["rayon"]
                    espacement_y += random.randint(100,   150)
                    y_c = espacement_y
                #time.sleep(5)
                espacement_y = random.randint(100, 150)
                y_c = 120

    #Positionnement des étapes et tâches de façon fixe
    def creerEtapesFixes(self,pert,lstEtapes):
            etape_debut_actuelle = ""
            etape_fin_actuelle = ""
            placement_x = 230
            placement_y = int((self.dimensions[1] / 2))
            espacement_y = 100
            espacement_y_niveau_zero = 60
            ss = 0
            v = 10
            for indice_niveau, niveau in enumerate(pert.tabNiveaux):
                if indice_niveau == 0:
                    tache = pert.associassionObjets[niveau[0]]
                    tache.dates_debut.coordonnees["x"],tache.dates_debut.coordonnees["y"],tache.dates_debut.coordonnees["rayon"] = 30,placement_y,tache.dates_debut.coordonnees["rayon"]
                for t in niveau:
                    if indice_niveau == 0:
                        y = espacement_y_niveau_zero + ss + v
                        ss = y
                        v += 90
                        #espacement_y_niveau_zero += espacement_y_niveau_zero * 2
                    else :
                        y = placement_y
                    tache = pert.associassionObjets[t]
                    tache.dates_fin.coordonnees["x"],tache.dates_fin.coordonnees["y"],tache.dates_fin.coordonnees["rayon"] =  tache.dates_debut.coordonnees["x"]  + placement_x, y ,tache.dates_debut.coordonnees["rayon"]
                    placement_y += espacement_y
                placement_y = int((self.dimensions[1] / 2)) - 90


    #Prépare et affiche le diagramme de PERT
    def afficherPert(self,Interface_Graphique,pert,lstEtapes):

        #Interface_Graphique.creerEtapes(pert,lstEtapes)
        Interface_Graphique.creerEtapesFixes(pert,lstEtapes)
        while Interface_Graphique.affichage:

            # nettoie l'écran et change la couleur du fond
            Interface_Graphique.ecran.fill(Interface_Graphique.couleurs['BLANC'])

            #Créations du diagramme PERT
            Interface_Graphique.dessiner(pert)

            # Gestion des événements
            Interface_Graphique.gererEvenements()
            Interface_Graphique.clock.tick(20)

            #Mise à jour de l'écran
            pygame.display.flip()

        # Quitter le program
        pygame.quit()
