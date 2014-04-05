#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
from tkinter import filedialog
from dames.partie import Partie

class InterfaceDamier(tk.Frame):
    """
    Classe permettant l'affichage d'un damier. À modifier!
    @author: Bryan Oakley, Camille Besse, Jean-Francis Roy
    """

    def __init__(self, parent, taille_case, partie):

        self.parent = parent

        # Definition du damier : # de cases
        self.n_lignes = 8
        self.n_colonnes = 8

        # Definition du damier : taille des cases (en pixels)
        self.taille_case = taille_case

        # Definition du damier : couleur de cases
        self.couleur1 = "white"
        self.couleur2 = "gray"

        # Assignation de la partie courante
        self.partie = partie

        #Liste pour conserver la position source et ses coordonnées (x1, y1) et (x2, y2)
        self.source_selectionnee = []

        # Calcul de la taille du dessin
        canvas_width = self.n_colonnes * self.taille_case
        canvas_height = self.n_lignes * self.taille_case

        # Initialisation de la fenêtre parent contenant le canvas
        tk.Frame.__init__(self, self.parent)

        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background=None, name = "damier")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(sticky = tk.W)
        self.grid(rowspan = 2, sticky=tk.N + tk.S + tk.E + tk.W)

        # Création du menu, de ses composantes et ajout à la fenêtre
        self.menu = tk.Menu(parent)

        self.menu.add_command(label = "Nouvelle partie", command = self.nouvelle_partie)
        self.menu.add_command(label = "Charger partie", command = self.charger_partie)
        self.menu.add_command(label = "Sauvegarder partie", command = self.sauvegarder_partie)
        self.menu.add_command(label = "Charger partie avec déplacements")
        self.menu.add_command(label = "Sauvegarder partie avec déplacements")
        self.menu.add_command(label = "Quitter", command = parent.quit)

        parent.config(menu = self.menu)

        # Création du LabelFrame et des Label pour contenir les informations sur la partie courante
        self.informations = tk.LabelFrame(parent, text = "Informations", padx = 15)
        self.informations.grid(column = 1, row = 0, sticky = tk.W + tk.N)

        self.ltour = tk.Label(self.informations, text = "Tour du joueur " + self.partie.couleur_joueur_courant)
        self.ltour.grid()
        self.ldoit_prendre = tk.Label(self.informations, text = "Aucune prise obligatoire.")
        self.ldoit_prendre.grid()
        self.lpiece_forcee = tk.Label(self.informations, text = "Aucune pièce forcée.", width = 30)
        self.lpiece_forcee.grid()

        # Création du LabelFrame et du Text pour afficher l'historique des déplacements
        self.deplacements = tk.LabelFrame(parent, text = "Déplacements")
        self.deplacements.grid(column = 1, row = 1, sticky = tk.W + tk.N)

        self.historique = tk.Text(self.deplacements, width = 25, height = 24)
        self.historique.grid(column = 3, row = 1)

        #Création du Label pour afficher les erreurs
        self.lerreur = tk.Label(parent, text = "", foreground = "red")
        self.lerreur.grid(column = 0, row = 2, sticky = tk.W)

        #Gestion des clics
        self.parent.bind("<Button-1>", self.deplacement)

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)

        # Affiche les pièces sur le damier
        self.actualiser_jeu()

    def nouvelle_partie(self):
        """
        Remet tous les paramètres par défaut puis réaffiche le jeu.
        """

        self.partie.nouvelle_partie()
        self.ltour["text"] = "Tour du joueur " + self.partie.couleur_joueur_courant
        self.verifier_deplacement_force()
        self.lpiece_forcee["text"] = "Aucune pièce forcée."
        self.lerreur["text"] = ""
        self.historique.delete(1.0, tk.END)
        self.parent.bind("<Button-1>", self.deplacement)
        self.actualiser_jeu()

    def charger_partie(self):
        """
        Charge la partie choisie par l'utilisateur.
        """
        try:
            nom_fichier = filedialog.askopenfilename(title = "Partie à charger")
            self.partie.charger(nom_fichier)
            self.actualiser_jeu()
            self.verifier_deplacement_force()
            self.ltour["text"] = "Tour du joueur " + self.partie.couleur_joueur_courant

            liste_position = self.partie.damier.lister_deplacements_possibles_a_partir_de_position(self.partie.position_source_forcee,
                                                                                                   self.partie.doit_prendre)
            if (liste_position == []):
                self.lpiece_forcee["text"] = "Aucune pièce forcée."
            elif len(liste_position) == 1:
                str_temp = "Position cible forcée : " + str(liste_position[0])
            else:
                str_temp = "Positions cibles forcées : "
                for e in liste_position:
                    str_temp += str(e) + " "

            self.lpiece_forcee["text"] = str_temp

        except Exception:
            pass

    def sauvegarder_partie(self):
        """
        Sauvegarde la partie.
        """
        try:
            nom_fichier = filedialog.asksaveasfilename(title = "Sauvegarder la partie")
            self.partie.sauvegarder(nom_fichier)

        except Exception:
            pass

    def verifier_deplacement_force(self):
        """
        Vérifie si le joueur courant doit prendre une pièce et met à jour le Label
        self.ldoit_prendre en conséquence.
        """

        if (self.partie.joueur_courant_peut_prendre_piece_adverse()):
            self.ldoit_prendre["text"] = "Vous devez prendre"
            self.partie.doit_prendre = True
        else:
            self.ldoit_prendre["text"] = "Aucune prise obligatoire"
            self.partie.doit_prendre = False

    def ajouter_piece(self, position, nom_piece):
        """
        Ajoute une pièce sur le damier.
        """

        # On "dessine" la pièce
        ligne, colonne = position
        self.canvas.create_text(ligne, colonne, text=self.partie.damier.cases[position], tags=(nom_piece, "piece"))

        # On place la pièce dans le canvas (appel de placer_piece)
        self.placer_piece((ligne, colonne), nom_piece)

    def placer_piece(self, position, nom_piece):
        """
        Place une pièce à la position donnée (ligne, colonne).
        """

        ligne, colonne = position

        # Placer les pieces au centre des cases.
        x = (colonne * self.taille_case) + int(self.taille_case / 2)
        y = (ligne * self.taille_case) + int(self.taille_case / 2)

        # On change la taille de la police d'écriture selon la taille actuelle des cases.
        tempfont = ('Helvetica', self.taille_case//2)
        self.canvas.itemconfigure(nom_piece, font=tempfont)

        self.canvas.coords(nom_piece, x, y)

    def add_historique(self, source, dest):
        """
        Ajoute les informations de déplacements dans le Text self.historique
        """

        move = self.partie.couleur_joueur_courant+(": {}->{} \n".format(source, dest))
        self.historique.insert("end", move)

    def deplacement(self, event):

        # Vérifie que que l'événement à eu lieu sur le damier.
        if (event.widget.winfo_name() == self.canvas.winfo_name()):
            position = ((event.y // self.taille_case), (event.x // self.taille_case))

            # Vérifie s'il s'agit d'un clic pour la source
            if (self.source_selectionnee == []):
                try:
                    #Valide la source, puis met la pièce sélectionnée en bleu.
                    self.partie.valider_position_source(position)
                    self.lerreur["text"] = ""
                    self.source_selectionnee.append(position)
                    x1, y1 = (event.x // self.taille_case) * self.taille_case, (event.y // self.taille_case) * self.taille_case
                    x2, y2 = (event.x // self.taille_case) * self.taille_case + self.taille_case, (event.y // self.taille_case) * self.taille_case + self.taille_case
                    self.source_selectionnee.append((x1, y1))
                    self.source_selectionnee.append((x2, y2))
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="blue", tags="case")
                    self.canvas.tag_raise("piece")
                    self.canvas.tag_lower("case")

                except Exception as e:
                    self.lerreur["text"] = e
            else:
                try:
                    # Si la position source et la position cible sont les mêmes, remet la case en gris
                    if (self.source_selectionnee[0] == position):
                        self.canvas.create_rectangle(self.source_selectionnee[1][0], self.source_selectionnee[1][1],
                                                     self.source_selectionnee[2][0], self.source_selectionnee[2][1],
                                                     outline="black", fill=self.couleur2, tags="case")
                        self.canvas.tag_raise("piece")
                        self.canvas.tag_lower("case")
                        self.source_selectionnee = []

                    else:
                        # Valide la position cible, puis effectue le déplacement
                        self.partie.valider_position_cible(self.source_selectionnee[0], position)
                        self.lerreur["text"] = ""
                        test_prise = self.partie.damier.deplacer(self.source_selectionnee[0], position)
                        self.placer_piece(position, self.partie.damier.cases[position].nom)
                        self.canvas.create_rectangle(self.source_selectionnee[1][0], self.source_selectionnee[1][1],
                                                     self.source_selectionnee[2][0], self.source_selectionnee[2][1],
                                                     outline="black", fill=self.couleur2, tags="case")

                        # Ajoute le déplacement à l'historique
                        self.add_historique(self.source_selectionnee[0], position)

                        #Vérifie si le joueur peut faire une deuxième prise.
                        if (not test_prise):
                            # Met à jour les paramêtres une fois le coup joué
                            self.partie.position_source_forcee = None
                            self.partie.passer_au_joueur_suivant()
                            self.ltour["text"] = "Tour du joueur " + self.partie.couleur_joueur_courant

                        elif (self.partie.damier.position_peut_prendre_une_piece_adverse(position)):
                            # Force la position source, puis affiche la position cible forcée dans lpiece_forcee.
                            self.partie.position_source_forcee = position
                            liste_position = self.partie.damier.lister_deplacements_possibles_a_partir_de_position(position, self.partie.doit_prendre)

                            if len(liste_position) == 1:
                                str_temp = "Position cible forcée : " + str(liste_position[0])
                            else:
                                str_temp = "Positions cibles forcées : "
                                for e in liste_position:
                                    str_temp += str(e) + " "

                            self.lpiece_forcee["text"] = str_temp

                        else:
                            # Vérifie si la partie est terminée. Si ce n'est pas le cas, met à jour les paramètres
                            # et passe au joueur suivant
                            self.partie.position_source_forcee = None
                            joueur_actuel = self.partie.couleur_joueur_courant
                            self.partie.passer_au_joueur_suivant()
                            if (self.partie.damier.lister_deplacements_possibles_de_couleur(self.partie.couleur_joueur_courant)):
                                self.ltour["text"] = "Tour du joueur " + self.partie.couleur_joueur_courant
                                self.lpiece_forcee["text"] = "Aucune pièce forcée."
                            else:
                                self.lerreur["text"] = "Félicitations, joueur " + joueur_actuel + ", vous avez gagné!"
                                self.parent.unbind("<Button-1>")

                        self.source_selectionnee = []
                        self.actualiser_jeu()

                except Exception as e:
                    self.lerreur["text"] = e

        self.verifier_deplacement_force()

    def actualiser(self, event):
        """
        Redessine le damier lorsque la fenetre est redimensionnée.
        """

        # Calcul de la nouvelle taille du damier
        x_size = int((event.width - 1) / self.n_colonnes)
        y_size = int((event.height - 1) / self.n_lignes)
        self.taille_case = min(x_size, y_size)

        # On efface les cases
        self.canvas.delete("case")

        # On les redessine
        color = self.couleur2
        for row in range(self.n_lignes):
            #Alternance des couleurs
            if color == self.couleur2:
                color = self.couleur1
            else:
                color = self.couleur2

            for col in range(self.n_colonnes):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="case")

                #Alternance des couleurs
                if color == self.couleur2:
                    color = self.couleur1
                else:
                    color = self.couleur2

        # On redessine les pieces
        for position in self.partie.damier.cases.keys():
            self.placer_piece(position, self.partie.damier.cases[position].nom)

        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")

    def actualiser_jeu(self):
        """
        Met à jour la position des pièces sur le damier.
        """

        self.canvas.delete("piece")
        
        for cle in self.partie.damier.cases.keys():
            self.ajouter_piece(cle, self.partie.damier.cases[cle].nom)

class JeuDeDames:
    def __init__(self):
        # On a besoin d'une fenêtre.
        self.fenetre = tk.Tk()

        # On a besoin d'une partie.
        self.partie = Partie()

        # On a besoin d'un damier, qu'on placera dans notre fenêtre...
        self.interface_damier = InterfaceDamier(self.fenetre, 64, self.partie)
        self.interface_damier.grid()

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments du plateau.
        self.interface_damier.grid_columnconfigure(0, weight=1)
        self.interface_damier.grid_rowconfigure(0, weight=1)

        # Boucle principale.
        self.fenetre.mainloop()