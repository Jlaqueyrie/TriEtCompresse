# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:52:37 2018

# 1 - liste tout les fichiers d'un dossier
# 2 - récupère le numéros de la semaine de création du fichier
# 3 - Cherche si un dossier pour la semaine existe déjà (formatage des nom pour logmatic), si le dossier existe pas il le créer
# 4 - Une fois tout les fichiers dans des dossiers, compress le tout.

Modifed on Fri Jui 26 08:30:00 2019

# 1 - add choices to choose teh date format ISO8601

@author: jlaqueyr
"""

# ------------------Import des modules ---------------------------------------#

import glob
import datetime
import os
import shutil
from pathlib import Path
import sys
import isoweek
import time
import send2trash as go

#---------------------- Fonctions --------------------------------------------#
DOCUMENTATION ="""Script pour tri et compressage des logs testeurs.


    Ce script permet le tri par semaine et Années des logs présents sur les équipements
    de test.
    Le format du Nom du dossier suis l'iso 8601.

    Args:
        param1 (str): Chemin du dossier à trier entouré de guillemet.
        param2 (str): Extension des fichiers à trier ex: txt.

    Returns:
        Le script fait apparaitre un message à l'écran quand il se termine..

"""
def EffaceDossier(Dossier):
    try:
        go.send2trash(Dossier)
        Ret = 0
    except:
        Ret = 1
        return Ret
    
def ZipDossier(DossierSource, ListeDossier):
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

def getArg():    
    if len(sys.argv) > 1 :
        ListeArgument = sys.argv
        print("Liste de paramètre : {}".format(sys.argv))
    else :
        print("Nombre d'argument insufissant")
        print(DOCUMENTATION)
        sys.exit()
        ListeArgument = []
    return ListeArgument

def ExtractDatetime(Chemin):
    EpochDatefichier = os.path.getmtime(Chemin)
    DateTimefichier = datetime.datetime.fromtimestamp(
    EpochDatefichier)
    return DateTimefichier

def ExtractSemaine(objDate):
    WeekDateTime = isoweek.Week.withdate(objDate)
    WeekDateTime = WeekDateTime.isoformat()
    return WeekDateTime
    
def main():

    try :
      
        ListeArg = getArg()

        
        DossierLog = ListeArg[1].replace("/", "\\")
        ExtensionFichier = '*.{}'.format(ListeArg[2])
        Zip = ListeArg[3]


        CompteurFichier  = 0
        CompteurErreur = 0
            
        print("Chemin du dossier de log : {}".format(DossierLog))
        print("Extension des fichiers à Trier".format(ExtensionFichier))
        print("Option Zip {}".format(Zip))

        ListeDeFichier = glob.glob(os.path.join(DossierLog, '*.txt'))

        for Fichier in ListeDeFichier:
            try:
                AncienDossier = os.path.dirname(Fichier)
                print("Ancien Dosssier = {}".format(AncienDossier))
                DateFichier = ExtractDatetime(Fichier)
                print(DateFichier)
                SemaineFichier = ExtractSemaine(DateFichier)

                #actualise la liste des dossiers disponible pour déplacer les fichiers
                        
                NomNouveauxDossier = "{}\\{}\\".format(AncienDossier,
                        SemaineFichier)
                print("Nvx : {}".format(NomNouveauxDossier))

                if os.path.isdir(NomNouveauxDossier):

                    print("Dossier Existe")

                    try:
                        shutil.move(Fichier, os.path.join(NomNouveauxDossier, os.path.basename(Fichier)))
                    except shutil.Error as err:
                        print(err.args[0])
                                
                else:
                                
                    try:                            
                        os.mkdir(NomNouveauxDossier)
                        shutil.move(Fichier, os.path.join(NomNouveauxDossier, os.path.basename(Fichier)))
                        print("Nvx dossier créer")
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                        pass

if __name__ == '__main__':
    main()
