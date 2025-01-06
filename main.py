import numpy as np
from fractions import Fraction # so that numbers are not displayed in decimal.
import sys
import copy
import numpy as np
import Interface
#Classe representant un diagarmme de PERT avec les éléments associés(tâche,étapes...)
class Pert:
    def __init__(self):
      #self.taches = list(map(chr, range(97, 123)))
      #Liste des taches(en String)
      self.taches = list(map(chr, range(97, 109)))
      #durée des tâches
      self.durees_taches = [4,8,1,1,6,3,5,3,1,2,2,5]
      #Liste des antécédents
      self.tabAnt = [["\\"],["\\"],["\\"],["c"],["a"] ,["a"],["b"],["e","f","g"],["d"],["i"],["h"],["j","k"]]
      #Une liste d'objets Taches
      self.lstTaches = []
      #la table de réduction
      self.tabReduction = self.tabAnt
      #la table des niveaux
      self.tabNiveaux = []
      self.genererTaches()
      self.associassionObjets = dict(zip(self.taches,self.lstTaches))
      #Objet permetttan de dessiner un diagramme de Pert
      self.graphe = Interface.Interface_Graphique("PERT Diagramme", 1280, 600)
      self.affichage_partielle = {"dates": True, "dates_plut_tot":True, "dates_plus_tard": True}
      #calcut et affiche le chemin critique
      self.calcul_chemin_critique = False

    #Crée d'une liste de tâches
    def genererTaches(self):
      for i in range(len(self.taches)):
        self.lstTaches.append(Tache(self.taches[i],self.durees_taches[i],self.tabAnt[i]) )

    #Retourne l'objet tâche associé à une lettre
    def getTache(self,lettre):
      for tache in self.lstTaches:
        if tache.nom == lettre:
          return tache

    #Réduit des tâches dans la liste lstTaches
    def reduire(self):
      trouve = False
      reduction = False
      indice_sup = -1
      for tache in self.lstTaches:
        for antecedent in tache.antecedents:   #chaque antécedent de la tache choisie
          if antecedent == "\\":      #si il n'a pas d'antécedent
            break
          else:
              #chaque liste d'antécedent de la table générale d'antécédent
            for lst in self.tabReduction:
              for i in lst:
                  if i == tache.nom:
                      trouve = True
                      if trouve:
                          trouve = False
                          indice = 0
                          for ant in lst:
                              if ant == antecedent:
                                  reduction = True
                                  indice_sup = indice
                              indice += 1
                              if  reduction:
                                  reduction = False
                                  del lst[indice_sup]

    #Crée des niveaux
    def creerNiveaux(self):
      #Nom des tâches
      lst1 = [x.nom for x in self.lstTaches]
      #Antécedents reduits des tâches
      lst2 = copy.deepcopy(self.tabReduction)
      fusion =  list(zip(lst1, lst2))
      tabNiveaux = []
      reduction_en_cours = ["\\"]
      reduction_a_ajouter = []
      moins_un = False
      nbr_moins_un = 0

      while len(reduction_en_cours) != 0:
        for f in fusion:  #la fusion entre taches et réduction
          for indexx,ant in enumerate(f[1]): #pour chaque reduction de chaque tâche
            if ant in reduction_en_cours:
              if len(f[1]) == 1:
                  reduction_a_ajouter.append(f)
              if len(f[1]) != 1:
                  nbr_moins_un = 0
                  for i in f[1]:
                      if i == -1:
                          nbr_moins_un += 1
                  if len(f[1]) - nbr_moins_un == 1:
                      moins_un  = True
                  else:
                      moins_un = False
                  if moins_un:
                      reduction_a_ajouter.append(f)
                      moins_un = False
                  else:
                    f[1][indexx] = -1

        #Suppression des reductions effectuées
        reduction_en_cours = []
        #Ajout de nouvelles reductions
        for i in reduction_a_ajouter:
          reduction_en_cours.append(i[0])
        #suppression des fusion dans la table fusion
        for i in reduction_a_ajouter:
          if not len(fusion):
              fusion.remove (i)
        #suppression des reductions ajoutées
        reduction_a_ajouter =[]
        #Mise à jour de la table niveaux
        if len(reduction_en_cours) != 0:
            tabNiveaux.append(reduction_en_cours)
      self.tabNiveaux = tabNiveaux
      #print(tabNiveaux)

    #calcule les successeurs de chaque tache
    def ajouterSuccesseurs(self):
        for tache in self.lstTaches:
            for t in self.lstTaches:
                if t != tache:
                    for ant in t.antecedents:
                        #if tache.nom == "i":
                        #    print("lolita")
                        if ant == tache.nom:
                            tache.successeurs.append(t)

    #calcule les dates relatives à chaque tâche
    def calculerDates(self):
        tabN  = copy.deepcopy(self.tabNiveaux)
        for niveau in tabN:
            for t in niveau:
                tache = self.associassionObjets[t]
                if tache.antecedents == ["\\"]:
                    tache.dates_debut.etapes["plus_tot"] = 0
                if  tache.dates_debut.etapes["plus_tot"]  + tache.duree_tache > tache.dates_fin.etapes["plus_tot"]:
                    tache.dates_fin.etapes["plus_tot"] = tache.dates_debut.etapes["plus_tot"]  + tache.duree_tache


        #Pour l'afficahge progressive
        #Etape.filterEtapes()
        #self.graphe.afficherPert(self.graphe, self, Etape.lstEtapes)

        tabN.reverse()
        for niveau in tabN:
            for t in niveau:
                tache = self.associassionObjets[t]
                if len(tache.successeurs) == 0:
                    #tache.dates_fin.etapes["plus_tot"] = tache.dates_debut.etapes["plus_tot"] + tache.duree_tache
                    tache.dates_fin.etapes["plus_tard"] = tache.dates_fin.etapes["plus_tot"]
                    tache.dates_debut.etapes["plus_tard"] = tache.dates_fin.etapes["plus_tard"] - tache.duree_tache
                if  tache.dates_fin.etapes["plus_tard"]  - tache.duree_tache < tache.dates_debut.etapes["plus_tard"]:
                        tache.dates_debut.etapes["plus_tard"] = tache.dates_fin.etapes["plus_tard"] - tache.duree_tache

    #crée des étapes
    def creerEtapes(self):
        etapes_deja_creees = dict()
        etape = Etape("plut_tot","plut_tard")
        for tache in self.lstTaches:
            if tache.antecedents == ["\\"]:
                tache.dates_debut = etape
                tache.dates_debut.lstTachesSortantes.append(tache)
        for tache in self.lstTaches:
            tache.dates_fin = Etape("plut_tot","plut_tard")
            tache.partagerEtape(etapes_deja_creees)

    #calcule les marges des tâches
    def calculerMarges(self):
        for tache in self.lstTaches:
            tache.marges["totale"] = tache.dates_fin.etapes['plus_tard'] -tache.dates_debut.etapes['plus_tot'] - tache.duree_tache
            tache.marges["libre"] = tache.dates_fin.etapes['plus_tot'] -tache.dates_debut.etapes['plus_tot'] - tache.duree_tache
            tache.marges["certaine"] = tache.dates_fin.etapes['plus_tot'] -tache.dates_debut.etapes['plus_tard'] - tache.duree_tache

    #Prépare le diagramme de Pert pour être affiché
    def preparerAffichage(self):
        tachesParNiveaux = copy.deepcopy(self.tabNiveaux)
        indice = 0
        for niveau in tachesParNiveaux:
            for t in niveau:
                niveau[indice] = self.associassionObjets[t]
                indice += 1
            indice = 0
        return tachesParNiveaux

    #retourne une liste des étapes
    def recupererEtapes(self):
        return copy.deepcopy(Etape.lstEtapes)
    def concatener(self,tab):
        str = ""
        for elt in tab:
            str += elt
        return str

    def AfficherTableau(self):
        entetes = ["Tache","Durée","Antériorité","Date au plus tôt","Date au plus tard","Marge totale","Marge libre","Marge Certaine"]
        for i in entetes:
            print(i, end='\t ')
        print()
        separateur = ', '
        for tache in self.lstTaches:
            print(tache.nom, end='\t ')
            print(tache.duree_tache, end='\t\t')

            #print(separateur.join(tache.antecedents),end='\t')
            print(self.concatener(tache.antecedents),end='\t \t')
            #[print (ant, end="\t") for ant in tache.antecedents]
            #print(tache.antecedents, end='\t \t \t ')
            print(tache.dates_debut.etapes["plus_tot"], end='\t \t \t')
            print(tache.dates_debut.etapes["plus_tard"],end='\t \t \t')
            print(tache.marges["totale"], end='\t \t')
            print(tache.marges["libre"], end='\t \t \t')
            print(tache.marges["certaine"])
        print()

    #calcul du chemin critique mais pas utilisée
    def determinerCheminsCritique(self):
        lst = Etape.lstEtapes
        for etape in lst:
            for succ in etape:
                pass


#Représent une tâche
class Tache:
  def __init__(self,nom,duree_tache,tache):
    self.nom = nom
    self.antecedents = tache
    self.successeurs = []
    self.duree_tache = duree_tache
    self.dates_debut = ""
    self.dates_fin = ""
    self.marges = {"totale": -1, "libre": - 1, "certaine" :-1 }

  #Associe une étape à des tâches associées
  def partagerEtape(self,etapes_deja_creees):
      for succ in self.successeurs:
          if not succ.nom in etapes_deja_creees:
            #self.dates_fin = Etape("plut_tot","plut_tard")
            succ.dates_debut = self.dates_fin
            etapes_deja_creees.update({succ.nom:succ.dates_debut })
            succ.dates_debut.lstTachesSortantes.append(succ)
          else:
              self.dates_fin = etapes_deja_creees[succ.nom]

#Représente une étape
class Etape:
    COMPTEUR = 1
    lstEtapes = []
    def __init__(self,date_1,date_2):
        self.nombre = Etape.COMPTEUR
        self.etapes = {"plus_tot":-1 ,"plus_tard":9999999999 }
        Etape.COMPTEUR += 1
        #valeur de flottement
        self.battement = -1
        Etape.lstEtapes.append(self)
        self.coordonnees = {"x":-1,"y":-1,"rayon":30}
        #liste de taches sortantes de chaque étape
        self.lstTachesSortantes = []
        self.circle = -1
        self.couleur_tache_sortante = {"VERT":(  100,   255,   70),"ROUGE": (255,   0,   0) }



    def calculerBattements(self):
        self.battement = self.etapes["plus_tard"] - self.etapes["plus_tot"]

    @classmethod
    def filterEtapes(cls):
        #Recherche des étapes non utilisées
        delEtapes = []
        for etape in Etape.lstEtapes:
            if etape.etapes["plus_tot"] == -1 and etape.etapes["plus_tard"] == 9999999999:
                delEtapes.append(etape)
        for i in delEtapes:
            Etape.lstEtapes.remove(i)
        nombre = 1
        #Suppression des etapes inutilisées et mises à jours du compteur
        for etape in Etape.lstEtapes:
            etape.nombre = nombre
            nombre += 1
        Etape.COMPTEUR = nombre
        #print("nbr etapes " + str(len(Etape.lstEtapes)))





pert = Pert()
#réduction des antériorités
pert.reduire()
#création des niveaux
pert.creerNiveaux()
#ajout des successeurs
pert.ajouterSuccesseurs()
#création et assoiciation des étapes
pert.creerEtapes()
#calcul des dates
pert.calculerDates()
#calcul des marges
pert.calculerMarges()
#Préparation pour affichage
Etape.filterEtapes()
pert.preparerAffichage()
#Affichage du tableau
pert.AfficherTableau()
#Affichage du digramme de PERT
pert.graphe.afficherPert(pert.graphe,pert,Etape.lstEtapes)









'''
for etape in Etape.lstEtapes:
    print(str(etape.nombre) + str(etape.etapes) + str(etape.battement))
for t in t.lstTaches:
    print( t.nom + " " + str(t.dates_debut.etapes)  + str(t.dates_fin.etapes) + str(t.marges)  )
'''
