# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:52:37 2018

# 1 - liste tout les fichiers d'un dossier
# 2 - récupère le numéros de la semaine de création du fichier
# 3 - Cherche si un dossier pour la semaine existe déjà (formatage des nom pour logmatic), si le dossier existe pas il le créer
# 4 - Une fois tout les fichiers dans des dossiers, compress le tout.

@author: jlaqueyr
"""

# --------------import des modules -------------------------------------------#
import glob
import datetime
import os
import shutil

from pathlib import Path
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import W, S, E, N
from tkinter import filedialog
from tkinter import Frame
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Radiobutton
from tkinter import messagebox

#import send2trash as go

#-------------------- Fonctions --------------------------------------------#


class TriLogGUI:

    def __init__(self, master):
        # Variables
        self.DossierLog = None
        self.ChaineNomDossier = ""
        self.AnnéeDossier = ""
        self.ChaineGlob = "*.txt"

        # Config de la police
        MF_WIDTH = 400
        MF_HEIGHT = 150
        Police = "Arial Bold"
        TaillePolice = 15

        # Création fenêtre principale
        self.master = master
        master.title("Archivage Dossier")

        # Paramètres de la fenêtre principale
        MainFrame = Frame(self.master, width=MF_WIDTH, height=MF_HEIGHT)
        MainFrame.columnconfigure(100, weight=1)
        MainFrame.rowconfigure(100, weight=1)
        MainFrame.pack(pady=100, padx=100)

        # Création des variables tkinter pour le gui
        SepVar0 = StringVar(master)
        SepVar1 = StringVar(master)
        ZipVar3 = IntVar(master)
        DelVar4 = IntVar(master)

        # Dictionnaire avec les options des menu déroulants
        ListSepVar0 = {'Semaine', 'Année'}
        ListSepVar1 = {'Semaine', 'Année'}

        # valeur par défaut des widgets
        SepVar0.set('Année')
        SepVar1.set('Semaine')
        ZipVar3.set(2)
        DelVar4.set(2)

        # Création des widgets
        self.Ett1 = Label(
            MainFrame,
            text="1 - Sélectionner le dossier contenant les fichiers à trier :",
            font=(Police, TaillePolice)
        )

        self.Boutton_Dossier = Button(
            MainFrame,
            text="Sélectionner dossier",
            command=self.SelectDossierLog
        )

        self.Boutton_Dossier.config(width=26)

        self.Ett2 = Label(
            MainFrame,
            text="2 - Choisir le format du titre des dossiers : ",
            font=(Police, TaillePolice)
        )

        self.Separateur0 = OptionMenu(MainFrame, SepVar0, *ListSepVar0)
        self.Separateur0.config(width=20)
        self.Separateur1 = OptionMenu(MainFrame, SepVar1, *ListSepVar1)
        self.Separateur1.config(width=20)

        self.Ett3 = Label(
            MainFrame,
            text="3 - Effacer dossier après zip : ",
            font=(Police, TaillePolice)
        )

        self.RadioOuiDel = Radiobutton(
            MainFrame,
            text="Oui",
            variable=DelVar4,
            value=1
        )
        self.RadioNonDel = Radiobutton(
            MainFrame,
            text="Non",
            variable=DelVar4,
            value=2
        )

        self.Ett4 = Label(
            MainFrame,
            text="4 - Zipper les dossiers : ",
            font=(Police, TaillePolice)
        )

        self.RadioOui = Radiobutton(
            MainFrame,
            text="Oui",
            variable=ZipVar3,
            value=1
        )
        self.RadioNon = Radiobutton(
            MainFrame,
            text="Non",
            variable=ZipVar3,
            value=2
        )

        self.Ett5 = Label(
            MainFrame,
            text="5 - Lancer le tri des fichiers",
            font=(Police, TaillePolice)
        )

        self.Lancer_Tri = Button(
            MainFrame,
            text="Go !",
            command=lambda: self.TriFichier(self.DossierLog,
                                            SepVar0.get(),
                                            SepVar1.get(),
                                            ZipVar3.get(),
                                            DelVar4.get())
        )

        # positionnement des widgets
        MainFrame.grid()
        self.Ett1.grid(row=0, column=0, sticky=W)
        self.Boutton_Dossier.grid(row=0, column=1, sticky=W)
        self.Ett2.grid(row=2, column=0, sticky=W)

        self.Separateur0.grid(row=2, column=1, sticky=W)
        self.Separateur1.grid(row=2, column=2, sticky=W)

        self.Ett3.grid(row=3, column=0, sticky=W)
        self.RadioOuiDel.grid(row=3, column=1, sticky=W)
        self.RadioNonDel.grid(row=3, column=2, sticky=W)

        self.Ett4.grid(row=4, column=0, sticky=W)
        self.RadioOui.grid(row=4, column=1, sticky=W)
        self.RadioNon.grid(row=4, column=2, sticky=W)

        self.Ett5.grid(row=5, column=0, sticky=W)

        self.Lancer_Tri.grid(row=5, column=1, sticky=N+W+S+E)

    def SelectDossierLog(self):
        self.DossierLog = filedialog.askdirectory()
        print("dossier de log : {}".format(Path(self.DossierLog)))

    def ExtractDate(self, Chemin):
        EpochDatefichier = os.path.getmtime(Chemin)
        Datefichier = datetime.datetime.fromtimestamp(
            EpochDatefichier).strftime('%d-%m-%Y %H:%M:%S')
        return Datefichier

    def ExtractSemaine(self, Date):
        d = datetime.datetime.strptime(Date, '%d-%m-%Y %H:%M:%S').date()
        NumSemaine = d.isocalendar()[1]
        NumSemaine = str(NumSemaine).zfill(2)
        return NumSemaine

    def ConvertSeparateur(self, Separateur):
        if Separateur == "Semaine":
            ChaineDossier = "W{0}"
        elif Separateur == "Année":
            ChaineDossier = "Y{1}"

        return ChaineDossier

    def ZipDossier(self, DossierSource, ListeDossier):
        for DossierAZipper in ListeDossier:
            NomDossier = os.path.basename(os.path.normpath(DossierAZipper))
            try:
                os.chdir(DossierSource)
                shutil.make_archive(
                    NomDossier,           # Non de l'archive zippé
                    'zip',                # Extension de l'archive
                    root_dir=NomDossier,  # Emplacement du dossier à zipper
                    base_dir=None)        # Nom du dossier racine dans l'archive
            except shutil.Error as err:
                print(err.args[0])

##    def EffaceDossier(self, Dossier):
##        try:
##            go.send2trash(Dossier)
##            Ret = 0
##        except:
##            Ret = 1
##            return Ret

    def MsgFini(self):
        messagebox.showinfo("Tri Fini", "le tri des fichiers est fini")

    def TriFichier(self, DossierLog, Sep0, Sep1, ZipVar, DelVar):

        Part1Nom = self.ConvertSeparateur(Sep0)
        Part2Nom = self.ConvertSeparateur(Sep1)

        ChaineNomDossier = "/" + Part1Nom + Part2Nom + "/"

        print("Chaine du nom de dossier : {}".format(ChaineNomDossier))

        New = DossierLog.replace("/", "\\")
        ListeDeFichier = glob.glob(os.path.join(New, '*.txt'))
        ListeDossierACreer = []

        for Fichier in ListeDeFichier:
            AncienDossier = os.path.dirname(Fichier)
            print("Ancien Dosssier = {}".format(AncienDossier))

            DateFichier = self.ExtractDate(Fichier)
            SemaineFichier = self.ExtractSemaine(DateFichier)

            #actualise la liste des dossiers disponible pour déplacer les fichiers
            AnneeFichier =  DateFichier.split("-")[2][0:4]
            
            NomNouveauxDossier = DossierLog+ChaineNomDossier.format(
                SemaineFichier, AnneeFichier)
            print("Nvx : {}".format(NomNouveauxDossier))
            
            if len(ListeDossier) == 0:
                if os.path.isdir(NomNouveauxDossier):
                    pass
                else:
                    os.mkdir(NomNouveauxDossier)
                    ListeDossierACreer.append(NomNouveauxDossier)

            else:
                
                if os.path.isdir(NomNouveauxDossier):
                    try:
                        shutil.move(Fichier, os.path.join(NomNouveauxDossier, os.path.basename(Fichier)))
                    except shutil.Error as err:
                        print(err.args[0])
                else:
                    print("Création nouveaux Dossier = {}".format(NomNouveauxDossier))
                    os.mkdir(NomNouveauxDossier)
                    ListeDossierACreer.append(NomNouveauxDossier)
                    shutil.move(Fichier, os.path.join(NomNouveauxDossier, os.path.basename(Fichier)))

        if ZipVar == 1:
            self.ZipDossier(DossierLog, ListeDossierACreer)

        if DelVar == 1:
            try:
                ListeDossierEffacer = [x[0] for x in os.walk(DossierLog)][1:]
                ListeDossierEffacer = [z.replace("/", "\\") for z in ListeDossierEffacer]

                for Dossier in ListeDossierEffacer:
                    print("Chemin du dossier à Effacer : {0}".format(Dossier))
                    Retour = self.EffaceDossier(Dossier)
            except:
                print("erreur efffacement fichier", end='\n')
                print("Retour de la fonction {0}".format(Retour))
            finally:
                pass
            self.MsgFini()


def main():
    root = Tk()
    my_gui = TriLogGUI(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
