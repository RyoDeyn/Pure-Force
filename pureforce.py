"""Script de génération de listes de mots de passe pour du brute-force.

Usage:
======
    python pureforce.py [OPTIONS]

    OPTIONS:
    -b (or --basic): starts the basic mode.
    -i (or --intelligentia): starts the intelligent mode.
    -h (or --help): shows the possible options.
"""

__authors__ = "Alexandre Quéré aka Ryo"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2022 Alexandre Quéré"

import sys  # sert à prendre les arguments en ligne de commande
import getopt  # sert à parser les arguments en ligne de commande
import array  # sert à stocker les caractères utilisés
import os # sert à vérifier si un fichier existe déjà

# On définit les variables globales :
mode = "mode inconnu"

welcome_text = ("\n=========== Welcome on Pure-Force ! ============\n"
                "====== A free, open and simple password generator. =======\n"
                "--------------------------------------------------")

pain_hint = "Did you know that 'pain' means 'bread' in french ?\n"

usage_text = "Usage : pureforce [OPTION]\n"

options_text = ("Possible options :\n"
                "-b (or --basic)              starts the basic mode, which generate an exhaustive list\n"
                "                             of passwords from a given range. Use basic interactive questions\n"
                "                             to modulate the range. It is the simplest mode but doesn't use\n"
                "                             any optimization.\n"
                "-i (or --intelligentia)      starts the intelligent mode, which generate an optimized list of\n"
                "                             passwords. It will use more interactive questions to select the\n"
                "                             most relevant passwords.\n"
                "-h (or --help)               shows the possible options (this menu).\n")

project_title = r""" ______   __  __     ______     ______        ______   ______     ______     ______     ______    
/\  == \ /\ \/\ \   /\  == \   /\  ___\      /\  ___\ /\  __ \   /\  == \   /\  ___\   /\  ___\   
\ \  _-/ \ \ \_\ \  \ \  __<   \ \  __\      \ \  __\ \ \ \/\ \  \ \  __<   \ \ \____  \ \  __\   
 \ \_\    \ \_____\  \ \_\ \_\  \ \_____\     \ \_\    \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_/     \/_____/   \/_/ /_/   \/_____/      \/_/     \/_____/   \/_/ /_/   \/_____/   \/_____/ 
                                                                                                  """

# Exemples de set de char possibles :
minuscules_set = array.array('u', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

majuscules_set = array.array('u', [letter.upper() for letter in minuscules_set])

digit_set = array.array('u', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

special_char_set = array.array('u', ['&', '#', '@', '$', '*', '%', '/', '?', '!', '<', '>'])


class TColor:
    """
    Stocke les différentes couleurs possibles si on veut afficher du texte dans le terminal en couleur.
    """
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    light_grey = '\033[37m'
    darkgrey = '\033[90m'
    light_red = '\033[91m'
    light_green = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    light_cyan = '\033[96m'
    end = '\033[0m'


def welcome_message():
    """Affiche un message de bienvenue.
    Affiche également des explications sur l'utilisation du script.
    """
    # On affiche le message de bienvenue :
    print(welcome_text)
    print(pain_hint)

    # On affiche la forme d'utilisation de pureforce :
    print(usage_text)

    # On affiche les options possibles :
    print(options_text)


def process_options():
    """Gère les options et les paramètres du script."""
    # couples : liste de couples [options, valeur] ; exemple : (-l, 4);(-p, "er")
    # finArgs : les arguments supplémentaires s'il y en a
    # Ici nos options ne prennent pas d'arguments donc on ne s'occupe pas de 'valeur'.
    # On ne s'occupera pas non plus de argsAfter.
    try:
        couples, args_after = getopt.getopt(sys.argv[1:], "bih", ["basic", "intelligentia", "help"])
    except getopt.GetoptError as error:
        # On affiche un message d'erreur :
        print("\nError : ", error)
        # On termine l'exécution du script :
        sys.exit("Use the option -h (or --help) to view the usage and possible options.\n")

    # Si on lance le script sans aucuns paramètres ou options :
    if len(couples) == 0 and len(args_after) == 0:
        welcome_message()
    # Si on lance le script avec des arguments supplémentaires :
    elif len(args_after) != 0:
        print("\nError : pureforce do not accept additional parameters")
        sys.exit("Use the option -h (or --help) to view the usage and possible options.\n")
    # Si on lance le script avec plusieurs options en même temps :
    elif len(couples) > 1:
        print("\nError : pureforce do not accept several options at the same time.\n"
              "Example of correct use : python pureforce -b\n"
              "Example of incorrect use : python pureforce -b -i\n")
    # Cas où l'usage est correcte :
    else:
        for option, value in couples:
            if option in ("-h", "--help"):
                help_option()
            elif option in ("-b", "--basic"):
                basic_option()
            elif option in ("-i", "--intelligentia"):
                print("you chose the intelligentia command !")


def help_option():
    """Affiche la page d'aide.
    """
    print(welcome_text)
    print(usage_text)
    print(options_text)


def basic_option():
    """Lance le mode basic.
    """
    global mode
    mode = "basic"
    file_name, length_min, length_max, char_used, writing_mode = basic_message()
    write_file(file_name, length_min, length_max, char_used, writing_mode)


def basic_message():
    """Affiche un message de bienvenue lorsque l'on rentre dans le mode basic.
    Un truc sympa et stylé.

    Returns
    -------
    file_name : string
        Name of the file to store the passwords.
    length_min : int
        Longueur minimale des mots de passe (inclus).
    length_max : int
        Longueur maximale des mots de passe (inclus).
    char_used : array
        Contient l'ensemble des char utilisés.
    writing_mode : string
        Le mode d'écriture sur le fichier (write or append).
    """
    print("--------------------------------------------------")
    print(project_title)
    print(f"{TColor.green}Entering basic mode ...{TColor.end}\n"
          "\nLa liste des mots de passe sera écrite dans un fichier txt (nom par défaut : 'pforce-basic.txt')."
          f"\nLes questions obligatoires sont marquées avec un {TColor.red}(*){TColor.end}.\n")

    file_name = ask_file_name("Nom du fichier txt: ")
    writing_mode = 'w'

    # Si le fichier existe déjà :
    if os.path.isfile(f"{os.path.abspath(os.getcwd())}\\{file_name}"):
        print(f"{TColor.yellow}Warning : the file {file_name} already exists. Choose the option you want :"
              f"\n- create a new file (by changing the name) (1)"
              f"\n- override the existing file (2)"
              f"\n- append the generated passwords to the existing file (3){TColor.end}")
        file_option = input("--> ")
        while file_option not in ['1', '2', '3']:
            print(f"{TColor.red}Erreur : Options disponibles : 1, 2 or 3.{TColor.end}")
            file_option = input("--> ")

        # Traitement selon l'option choisie :
        if file_option == '1':
            file_name = ask_file_name("Choose a new file name: ")
        elif file_option == '2':
            writing_mode = 'w'
        elif file_option == '3':
            writing_mode = 'a'
        else:
            sys.exit("Erreur : option inconnue.\nExiting ...")

    length_min = int_input(f"Longueur minimale des mots de passe {TColor.red}(*){TColor.end}: ")
    length_max = int_input(f"Longueur maximale des mots de passe {TColor.red}(*){TColor.end}: ")

    while length_max < length_min:
        print(f"{TColor.red}Erreur : la longueur maximale ne peut être inférieure à la longueur minimale.{TColor.end}")
        length_max = int_input(f"Longueur maximale des mots de passe {TColor.red}(*){TColor.end}: ")

    min_set_used = yes_no_input(f"Voulez-vous utiliser les minuscules (a, b, c, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    maj_set_used = yes_no_input(f"Voulez-vous utiliser les majuscules (A, B, C, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    dig_set_used = yes_no_input(f"Voulez-vous utiliser les chiffres (0, 1, 2, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    spe_set_used = yes_no_input(f"Voulez-vous utiliser des char spéciaux (&, #, @, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")

    # Si aucun char selectionné, on arrete l'execution du script :
    stop_exec = True
    for resp in [min_set_used, maj_set_used, dig_set_used, spe_set_used]:
        if resp == 'Y':
            stop_exec = False
    if stop_exec:
        sys.exit(f"\n{TColor.orange}You did not select any char set, exiting ...{TColor.end}\n")

    char_used = array.array('u')

    if min_set_used == 'Y':
        char_used += minuscules_set
    if maj_set_used == 'Y':
        char_used += majuscules_set
    if dig_set_used == 'Y':
        char_used += digit_set
    if spe_set_used == 'Y':
        char_used += special_char_set

    return file_name, length_min, length_max, char_used, writing_mode


def ask_file_name(question):
    """Demande à l'utilisateur d'entrer un nom de fichier, puis effectue une vérification sur la valeur entrée.

    Parameters
    ----------
    question : string
        La question à afficher à l'utilisateur.

    Returns
    -------
    string
        Le nom de fichier entré par l'utilisateur.
    """
    file_name = input(question)
    if file_name == "":
        file_name = "pforce-basic.txt"
    elif ".txt" not in file_name:
        file_name += ".txt"
    while len(file_name) > 200:
        print(f"{TColor.red}Erreur : le nom du fichier ne doit pas dépasser 200 caractères.{TColor.end}")
        file_name = input(question)

    return file_name


def int_input(question):
    """Demande à l'utilisateur d'entrer un entier, puis effectue une vérification sur la valeur entrée.

    Parameters
    ----------
    question : string
        La question à afficher à l'utilisateur.

    Returns
    -------
    int
        L'entier entré par l'utilisateur.
    """
    v_string = input(question)
    v_int = 0

    # On vérifie que l'utilisateur a bien entré un entier :
    try:
        v_int = int(v_string)
        # On vérifie que l'entier est supérieur à 1 :
        if v_int < 1:
            print(f"{TColor.red}Erreur : vous devez entrer un entier supérieur ou égal à 1.{TColor.end}")
            # On re-demande l'entrée à l'utilisateur :
            int_input(question)
    except ValueError as error:
        # On affiche un message d'erreur :
        print(f"{TColor.red}Erreur : vous devez entrer un entier.{TColor.end}")
        # On re-demande l'entrée à l'utilisateur :
        int_input(question)

    return v_int


def yes_no_input(question):
    """Demande à l'utilisateur d'entrer 'Y' or 'N', puis effectue une vérification sur la valeur entrée.

    Parameters
    ----------
    question : string
        La question à afficher à l'utilisateur.

    Returns
    -------
    string
        La réponse entrée par l'utilisateur.
    """
    rep = input(question)
    while rep not in ['Y', 'N']:
        print(f"{TColor.red}Erreur : vous devez entrer 'Y' or 'N'.{TColor.end}")
        # On re-demande l'entrée à l'utilisateur :
        rep = input(question)

    return rep


def write_file(file_name, length_min, length_max, char_used, writing_mode):
    """Écrit dans un fichier txt une liste de mots de passe.

    Parameters
    ----------
    file_name : string
        Le nom du fichier où seront écrits les mots de passe.
    length_min : int
        La longueur minimale des mots de passe (inclus).
    length_max : int
        La longueur maximale des mots de passe (inclus).
    char_used : array
        Contient l'ensemble des char utilisés.
    writing_mode : string
        Le mode d'écriture sur le fichier (write or append).

        Si le fichier n'existe pas, le crée.
    """
    try:
        with open(file_name, writing_mode) as file:
            generate_basic_passwd(file, length_min, length_max, char_used)
    except PermissionError:
        print("\nError : permission denied.\n"
              "Could not open file : ", file_name)
        sys.exit(f"-> Abandon du mode {mode}\n")
    except OSError:
        print("\nCould not open file : ", file_name)
        sys.exit(f"-> Abandon du mode {mode}\n")


def generate_basic_passwd(file, length_min, length_max, char_set):
    """Génère et écrit des mots de passe pour le mode basic.

    Parameters
    ----------
    file : TextIO
        Le fichier où seront écrits les mots de passe.
    length_min : int
        La longueur minimale des mots de passe (inclus).
    length_max : int
        La longueur maximale des mots de passe (inclus).
    char_set : array
        L'ensemble des caractères utilisés.
    """
    # Boucle qui parcoure chaque longueur possible :
    for length in range(length_min, length_max + 1):

        # file.write(f"mdp de longueur : {length}\n")
        # L'indice du caractère dans char_set :
        indice_cs = 0

        # On écrit le premier mot de passe pour cette longueur :
        mdp = ""
        for j in range(length):
            mdp += char_set[indice_cs]
        file.write(f"{mdp}\n")

        # Indice du caractère à modifier :
        indice_to_modify = length - 1

        # On crée tous les mots de passe pour une longueur donnée :
        for i in range((len(char_set)**length)-1):

            while mdp[indice_to_modify] == char_set[len(char_set)-1]:  # ancien : if indice_cs == (len(char_set) - 1):
                indice_to_modify -= 1

            nouveau_mdp = ""

            # On recopie le mdp précédent dans le nouveau mdp sauf pour 1 caractère qu'on modifie :
            for indice_courant in range(length):
                if indice_courant == indice_to_modify:
                    indice_cs = char_set.index(mdp[indice_to_modify]) + 1
                    nouveau_mdp += char_set[indice_cs]
                    # Si le mot de passe n'est pas terminé, on met tous les caractères suivants à cs[0] :
                    if indice_courant < (length-1):
                        for indice_restant in range(indice_courant+1, length):
                            nouveau_mdp += char_set[0]
                            indice_to_modify = length - 1
                        break
                else:
                    nouveau_mdp += mdp[indice_courant]

            mdp = nouveau_mdp
            # On écrit le nouveau mdp :
            file.write(f"{nouveau_mdp}\n")


def main():
    """Fonction principale."""
    process_options()


if __name__ == '__main__':
    main()
