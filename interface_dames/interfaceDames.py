#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
from dames.partie import Partie

class InterfaceDamier(tk.Frame):
    """
    Classe permettant l'affichage d'un damier. À modifier!
    @author: Bryan Oakley, Camille Besse, Jean-Francis Roy
    """

    def __init__(self, parent, taille_case):
        """taille_case est la taille d'un côté d'une case en pixels."""
        # Definition du damier : # de cases
        self.n_lignes = 8
        self.n_colonnes = 8

        # Definition du damier : taille des cases (en pixels)
        self.taille_case = taille_case

        # Definition du damier : couleur de cases
        self.couleur1 = "white"
        self.couleur2 = "gray"

        # Pièces sur le damier
        self.pieces = {}

        # Calcul de la taille du dessin
        canvas_width = self.n_colonnes * self.taille_case
        canvas_height = self.n_lignes * self.taille_case

        # Initialisation de la fenêtre parent contenant le canvas
        tk.Frame.__init__(self, parent)

        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background="white")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)
        self.grid(padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W)

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)


    def ajouter_piece(self, position, nom_piece):
        """
        Ajoute une pièce sur le damier.
        """

        # Caractères unicode des pièces
        caracteres_unicode_pieces = {"PB": "\u26C0",
                                    "DB": "\u26C1",
                                    "PN": "\u26C2",
                                    "DN": "\u26C3"}

        tempfont = ('Helvetica', self.taille_case//2)
        piece_unicode = caracteres_unicode_pieces[nom_piece[0:2]]

        # On "dessine" la pièce
        ligne, colonne = position
        self.canvas.create_text(ligne, colonne, text=piece_unicode, tags=(nom_piece, "piece"), font=tempfont)

        # On ajoute la piece dans le dictionnaire
        self.pieces[(ligne, colonne)] = nom_piece

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
        for position, nom in self.pieces.items():
            self.placer_piece(position, nom)

        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")


def initialise_jeu(plateau):
        plateau.ajouter_piece((7, 0), "PB1")
        plateau.ajouter_piece((7, 2), "PB2")
        plateau.ajouter_piece((7, 4), "PB3")
        plateau.ajouter_piece((7, 6), "PB4")
        plateau.ajouter_piece((6, 1), "PB5")
        plateau.ajouter_piece((6, 3), "PB6")
        plateau.ajouter_piece((6, 5), "PB7")
        plateau.ajouter_piece((6, 7), "PB8")
        plateau.ajouter_piece((5, 0), "PB9")
        plateau.ajouter_piece((5, 2), "PB10")
        plateau.ajouter_piece((5, 4), "PB11")
        plateau.ajouter_piece((5, 6), "PB12")
        plateau.ajouter_piece((2, 1), "PN1")
        plateau.ajouter_piece((2, 3), "PN2")
        plateau.ajouter_piece((2, 5), "PN3")
        plateau.ajouter_piece((2, 7), "PN4")
        plateau.ajouter_piece((1, 0), "PN5")
        plateau.ajouter_piece((1, 2), "PN6")
        plateau.ajouter_piece((1, 4), "PN7")
        plateau.ajouter_piece((1, 6), "PN8")
        plateau.ajouter_piece((0, 1), "PN9")
        plateau.ajouter_piece((0, 3), "PN10")
        plateau.ajouter_piece((0, 5), "PN11")
        plateau.ajouter_piece((0, 7), "PN12")



# Ajouts pour le TP4, idée de base...

class JeuDeDames:
    def __init__(self):
        # On a besoin d'une fenêtre.
        self.fenetre = tk.Tk()

        # On a besoin d'une partie.
        self.partie = Partie()

        # On a besoin d'un damier, qu'on placera dans notre fenêtre...
        self.interface_damier = InterfaceDamier(self.fenetre, 64)
        self.interface_damier.grid()

        # Par contre on aura probablement à modifier la classe InterfaceDamier pour
        # y inclure notre partie! À vous de jouer!


        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments du plateau.
        self.interface_damier.grid_columnconfigure(0, weight=1)
        self.interface_damier.grid_rowconfigure(0, weight=1)


        # Boucle principale.
        self.fenetre.mainloop()

