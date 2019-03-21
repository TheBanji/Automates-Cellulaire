﻿# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image, ImageTk,ImageGrab
import tkinter.messagebox
import tkinter.filedialog
import AlgoCSV #ALGOCSV permet de générer un csv en fonction du nombre de cellules choisies par l'utilisateur
import varCommunes as VC #varCommunes contient une classe qui rassemble toutes les variables utiles aux différents fichiers
import algorithmeForet as algoForet #Fichier qui contient l'algorithme
import csv
import classDialectCsv

def Clic(event):
    X = event.x
    Y = event.y
    X = int(X/100)*100
    Y = int(Y/100)*100
    vg.augmentCellEnFeu(X, Y)
    vg.augmentCellToCheck(X,Y)

def enregistrer():
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    image = ImageGrab.grab((x + 2, y + 2, x + w - 2, y + h - 2))
    image.save("resulat_simulation.png")

def dix () :
    vg.setNbCell(10)

def cinquante () :
    vg.setNbCell(50)

def cent () :
    vg.setNbCell(100)


# Déroulement de l'algorithme :

def sim_auto():
    for i in range(vg.getCellUpdated(), len(vg.getCellToCheck())//2):
        tmpCellEnFeu, tmpListeForet = algoForet.propagationFeu(vg.getNbCellules(), vg.getCellToCheck(), vg.getListeForet(), vg.getCellUpdated()) #On test d'abord si le feu peut se propager
        vg.setNewListeForet(tmpListeForet)

        for j in range(len(tmpCellEnFeu)):
            vg.augmentCellEnFeu(tmpCellEnFeu[j], tmpCellEnFeu[j+1])

        vg.setCellUpdated(vg.getCellUpdated()+2)

    cellEnFeu = vg.getCellEnFeu()
    for i in range(0, CellEnFeu, 2):
        vg.augmentCellToCheck(cellEnFeu[i], cellEnFeu[i+1])

    if(len(vg.getCellEnFeu()) > 0):
        for i in range(0, len(vg.getCellEnFeu()), 2):
            Fenetre.update()
            pass             #On affiche les nouveaux arbres à brûler

    vg.emptyCellEnFeu()
    canvas.after(2000, sim_auto)

def pasapas():
    for i in range(vg.getCellUpdated(), len(vg.getCellToCheck())//2):
        tmpCellEnFeu, tmpListeForet = algoForet.propagationFeu(vg.getNbCellules(), vg.getCellToCheck(), vg.getListeForet(), vg.getCellUpdated()) #On test d'abord si le feu peut se propager
        vg.setNewListeForet(tmpListeForet)

        for j in range(len(tmpCellEnFeu)):
            vg.augmentCellEnFeu(tmpCellEnFeu[j], tmpCellEnFeu[j+1])

        vg.setCellUpdated(vg.getCellUpdated()+2)

    cellEnFeu = vg.getCellEnFeu()
    for i in range(0, CellEnFeu, 2):
        vg.augmentCellToCheck(cellEnFeu[i], cellEnFeu[i+1])

    if(len(vg.getCellEnFeu()) > 0):
        for i in range(0, len(vg.getCellEnFeu()), 2):
            Fenetre.update()
            pass             #On affiche les nouveaux arbres à brûler

    vg.emptyCellEnFeu()

# Fin des fonctions concernant l'algorithme


def drawGrid(event): #Fonction qui dessine une grille sur le Canvas pour tester la position des textures
    for i in range(0, 1000, 1000//vg.getNbCellules()):
        canvas.create_line(0, i, 1000, i)
        canvas.create_line(i, 0, i, 1000)


def createMap(event):
    AlgoCSV.createCsv(vg.getHauteur(), vg.getLargeur(), vg.getNbCellules())
    tailleImg = 80
    grass = ImageTk.PhotoImage(Image.open("textures/grass80x80.png"))
    cordY = 0
    with open("csv.csv", "r", newline='') as f:
        reader = csv.reader(f, classDialectCsv.Dialect())
        for row in reader:
            cordX = 0
            for i in row:
                int(i)
                if i == 0:
                    canvas.create_image(cordX, cordY, anchor=tkinter.NW, image=grass)
                elif i==10:
                    canvas.create_image(cordX, cordY, anchor=tkinter.NW, image=grass)
                cordX = cordX+tailleImg
            cordY = cordY+tailleImg
    canvas.mainloop()
	

vg = VC.varGlobales() #vg est une instance de varGlobales
vg.setLargeur(800)
vg.setHauteur(800)
vg.setNbCell(10)

Fenetre = Tk()
Fenetre.title("Image")
Fenetre.geometry('1000x1000')
canvas = Canvas(Fenetre, width = 800, height = 800, background='grey')
menubar = Menu(Fenetre)

menufichier = Menu(menubar, tearoff = 0)
dimensions = Menu(menubar, tearoff = 0)
menufichier.add_command(label = "Enregistrer l'image", command = enregistrer)
menufichier.add_command(label = "Quitter", command = Fenetre.destroy)
dimensions.add_command(label = "10x10", command = dix)
dimensions.add_command(label = "50x50", command = cinquante)
dimensions.add_command(label = "100x100", command = cent)
menubar.add_cascade(label = "Fichier", menu = menufichier)
menubar.add_cascade(label = "Dimensions", menu = dimensions)

auto = Button(Fenetre, text = "Simulation Automatique", bg = "green", command = sim_auto)
manuel = Button(Fenetre, text = "Simulation Pas à Pas", bg = "blue", command = pasapas)
auto.grid(row = 0, column = 0, sticky = "n")
manuel.grid(row = 1, column = 0, sticky = "n")

canvas.bind("<Button-1>", Clic)
#canvas.bind("<Button-3>", drawGrid)
canvas.bind("<Button-3>", createMap)
# Affichage du menu
Fenetre.config(menu = menubar)

# Utilisation d'un dictionnaire pour conserver une référence
canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)
gifdict = {}
Fenetre.mainloop()
