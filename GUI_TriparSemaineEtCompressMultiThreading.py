# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:52:37 2018

# 1 - liste tout les fichiers d'un dossier
# 2 - récupère le numéros de la semaine de création du fichier
# 3 - Cherche si un dossier pour la semaine existe déjà (formatage des nom pour
 logmatic), si le dossier existe pas il le créer
# 4 - Une fois tout les fichiers dans des dossiers, compress le tout.

@author: jlaqueyr
"""

# --------------import des modules -------------------------------------------#
import glob
import datetime
import os
import shutil
from pathlib import Path
import concurrent.futures
import send2trash as go
from time import sleep
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


"""-------------------- Fonctions ------------------------------------------"""


class TriLogGUI (Frame):

    def __init__(self, master):
        # Variables
        self.DossierLog = ""
        self.ChaineNomDossier = ""
        self.AnnéeDossier = ""
        self.ChaineGlob = "*.txt"
        self.ListeDossierACreer = []
        self.NbrCore = os.cpu_count()
        print("init")
        # Config de la police
        MF_WIDTH = 400
        MF_HEIGHT = 150
        Police = "Arial Bold"
        TaillePolice = 15

        # Création fenêtre principale
        self.master = master
        master.title("Archivage Dossier")

        # Paramètres de la fenêtre principale
        print("Frame")
        MainFrame = Frame(self.master, width=MF_WIDTH, height=MF_HEIGHT)
        MainFrame.columnconfigure(100, weight=1)
        MainFrame.rowconfigure(100, weight=1)
        MainFrame.pack(pady=100, padx=100)

        # Création des variables tkinter pour le gui
        print("gui var")
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
            text="1 - Sélectionner le dossier contenantles fichiers à trier :",
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
            command=lambda: self.Sequenceur(self.DossierLog,
                                            self.ChaineGlob,
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
        print("Dans Zip Fonction")
        print(next(ListeDossier))
        for DossierAZipper in ListeDossier:
            NomDossier = os.path.basename(os.path.normpath(DossierAZipper))
            print(NomDossier)
            try:
                os.chdir(DossierSource)
                print("le dossier source est : {}".format(DossierSource))
                shutil.make_archive(
                    NomDossier,           # Non de l'archive zippé
                    'zip',                # Extension de l'archive
                    root_dir=NomDossier,  # Emplacement du dossier à zipper
                    base_dir=None)        # Nom du dossier racine dans l'archiv
            except shutil.Error as err:
                print(err.args[0])

    def EffaceDossier(self, Dossier):
        try:
            go.send2trash(Dossier)
            Ret = 0
        except OSError:
            Ret = 1
            return Ret

    def MsgFini(self):
        messagebox.showinfo("Tri Fini", "le tri des fichiers est fini")

    def NouveauxNomDossier(self, CheminFichier, ChaineNomDossier):
        DateFichier = self.ExtractDate(CheminFichier)
        SemaineFichier = self.ExtractSemaine(DateFichier)
        AnnéeDossier = datetime.datetime.today().year
        DossierLog = os.path.dirname(CheminFichier)

        NomNouveauxDossier = DossierLog+"/"+ChaineNomDossier.format(
            SemaineFichier,
            AnnéeDossier
        )
        return NomNouveauxDossier

    def TriFichier(self, CheminFichier):

        # Part1Chaine = self.ConvertSeparateur(self.SepVar0)
        # Part2Chaine = self.ConvertSeparateur(self.SepVar1)
        Part1Chaine = "W{0}"
        Part2Chaine = "Y{1}"
        ChaineNomDossier = "{}{}".format(Part1Chaine, Part2Chaine)
        NewPath = self.NouveauxNomDossier(CheminFichier, ChaineNomDossier)

        print("le nouveaux chemin pour le fichier est : {}".format(NewPath))

        ListeDossier = [x[0] for x in os.walk(os.path.dirname(CheminFichier))]

        if len(ListeDossier) == 0:
            if os.path.isdir(NewPath):
                pass
            else:
                # test si on peut créer un nouveaux dossier
                os.makedirs(NewPath, exist_ok=True)
        else:
            for DossierSemaine in ListeDossier:
                if os.path.isdir(NewPath):
                    try:
                        shutil.move(CheminFichier, NewPath)
                    except shutil.Error as err:
                        print(err.args[0])
                else:
                    try:
                        os.makedirs(NewPath, exist_ok=True)
                    except FileExistsError:
                        print("race condition")
                        sleep(2)
                        shutil.move(CheminFichier, NewPath)
                    try:
                        shutil.move(CheminFichier, NewPath)
                    except shutil.Error:
                        print("move")

    def Sequenceur(self, Dossier, Patern, ZipAction, DelAction):
        print("Zip = {} ; Del = {}".format(str(ZipAction), str(DelAction)))
        sleep(4)
        ListeDeFichier = glob.glob(Dossier+"/"+Patern)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.NbrCore) as executor1:
            for Fichier in zip(ListeDeFichier, executor1.map(
                self.TriFichier,
                ListeDeFichier)
            ):
                print(Fichier)

        if ZipAction == 1:
            print("Zip file")
            print(Dossier)
            sleep(4)
            self.ListeDossierACreer = os.walk(Dossier)
            self.ZipDossier(Dossier, self.ListeDossierACreer)

        if DelAction == 1:
            print("Effacer fichier")
            try:
                ListeDossierEffacer = [x[0] for x in os.walk(Dossier)][1:]
                print(ListeDossierEffacer)
                ListeDossierEffacer = [z.replace("/", "\\") for z in ListeDossierEffacer]

                for Dossier in ListeDossierEffacer:
                    print("Chemin du dossier à Effacer : {0}".format(Dossier))
                    Retour = self.EffaceDossier(Dossier)
            except OSError:
                print("erreur effacement fichier", end='\n')
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
