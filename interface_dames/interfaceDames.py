#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
from dames.partie import Partie

class InterfaceDamier(tk.Frame):
    """
    Classe permettant l'affichage d'un damier. À modifier!
    @author: Bryan Oakley, Camille Besse, Jean-Francis Roy
    """

    def __init__(self, parent, taille_case, partie):
        
        """taille_case est la taille d'un côté d'une case en pixels."""
        # Definition du damier : # de cases
        self.n_lignes = 8
        self.n_colonnes = 8

        # Definition du damier : taille des cases (en pixels)
        self.taille_case = taille_case

        # Definition du damier : couleur de cases
        self.couleur1 = "white"
        self.couleur2 = "gray"

        self.partie = partie
        
        self.source_selectionnee = []

        # Calcul de la taille du dessin
        canvas_width = self.n_colonnes * self.taille_case
        canvas_height = self.n_lignes * self.taille_case

        # Initialisation de la fenêtre parent contenant le canvas
        tk.Frame.__init__(self, parent)

        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background=None, name = "damier")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(sticky = tk.W)
        self.grid(rowspan = 2, sticky=tk.N + tk.S + tk.E + tk.W)
        
        self.menu = tk.Menu(parent)
        
        self.menu.add_command(label = "Nouvelle partie", command = self.nouvelle_partie)
        self.menu.add_command(label = "Charger partie")
        self.menu.add_command(label = "Sauvegarder partie")
        self.menu.add_command(label = "Charger partie avec déplacements")
        self.menu.add_command(label = "Sauvegarder partie avec déplacements")
        self.menu.add_command(label = "Quitter", command = parent.quit)
        
        parent.config(menu = self.menu)
        
        self.informations = tk.LabelFrame(parent, text = "Informations", padx = 15)
        self.informations.grid(column = 1, row = 0, sticky = tk.W + tk.N)
        
        self.ltour = tk.Label(self.informations, text = "Tour du joueur " + self.partie.couleur_joueur_courant)
        self.ltour.grid()
        self.ldoit_prendre = tk.Label(self.informations, text = "Aucune prise obligatoire.")
        self.ldoit_prendre.grid()
        self.lpiece_forcee = tk.Label(self.informations, text = "Aucune pièce forcée.")
        self.lpiece_forcee.grid()
        
        self.deplacements = tk.LabelFrame(parent, text = "Déplacements")
        self.deplacements.grid(column = 1, row = 1, sticky = tk.W + tk.N)
        
        tk.Text(self.deplacements, width = 20, height = 24).grid(column = 3, row = 1)
        
        self.lerreur = tk.Label(parent, text = "", foreground = "red")
        self.lerreur.grid(column = 0, row = 2, sticky = tk.W)
        
        parent.bind("<Button-1>", self.deplacement)

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)

        self.initialise_jeu()

    
    def nouvelle_partie(self):
        
        self.partie.nouvelle_partie()
        self.ltour = "Tour du joueur " + self.partie.couleur_joueur_courant
        self.verifier_deplacement_force()
        self.lpiece_forcee = "Aucune pièce forcée."
        self.lerreur = ""
        self.canvas.delete("piece")
        self.initialise_jeu()
        
    
    def verifier_deplacement_force(self):
        
        if (self.partie.joueur_courant_peut_prendre_piece_adverse()):
            self.ldoit_prendre["text"] = "Vous devez prendre"
        else:
            self.ldoit_prendre["text"] = "Aucune prise obligatoire"
    
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
        
    def deplacement(self, event):

        if (event.widget.winfo_name() == self.canvas.winfo_name()):
            position = ((event.y // self.taille_case), (event.x // self.taille_case))
        
            if (self.source_selectionnee == []):
                try:
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
                    if (self.source_selectionnee[0] == position):
                        self.canvas.create_rectangle(self.source_selectionnee[1][0], self.source_selectionnee[1][1], self.source_selectionnee[2][0], self.source_selectionnee[2][1], outline="black", fill=self.couleur2, tags="case")
                        self.canvas.tag_raise("piece")
                        self.canvas.tag_lower("case")
                        self.source_selectionnee = []

                    else:
                        self.partie.valider_position_cible(self.source_selectionnee[0], position)
                        self.lerreur["text"] = ""
                        x1, y1 = (event.x // self.taille_case) * self.taille_case, (event.y // self.taille_case) * self.taille_case
                        x2, y2 = (event.x // self.taille_case) * self.taille_case + self.taille_case, (event.y // self.taille_case) * self.taille_case + self.taille_case
                        self.partie.damier.deplacer(self.source_selectionnee[0], position)
                        self.placer_piece(position, self.partie.damier.cases[position].nom)
                        self.canvas.create_rectangle(self.source_selectionnee[1][0], self.source_selectionnee[1][1], self.source_selectionnee[2][0], self.source_selectionnee[2][1], outline="black", fill=self.couleur2, tags="case")
                        self.source_selectionnee = []
                        self.partie.passer_au_joueur_suivant()
                        self.ltour["text"] = "Tour du joueur " + self.partie.couleur_joueur_courant
                        self.initialise_jeu()

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

    def initialise_jeu(self):
            
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

