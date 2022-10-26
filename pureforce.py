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
    # # finArgs : les arguments supplémentaires s'il y en a
    # # Ici nos options ne prennent pas d'arguments donc on ne s'occupe pas de 'valeur'.
    # # On ne s'occupera pas non plus de argsAfter.
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
    """???
    """
    global mode
    mode = "basic"
    write_file('pforce-basic.txt')


def write_file(file_name):
    """Écrit dans un fichier txt un string quelconque.

    Parameters
    ----------
    file_name : string
        Le nom du fichier où seront écrits les mots de passe.

        Si le fichier n'existe pas, le créé.
    """
    try:
        with open(file_name, 'w') as file:
            file.write("YESSSSS")
    except PermissionError:
        print("\nError : permission denied.\n"
              "Could not open file : ", file_name)
        sys.exit(f"-> Abandon du mode {mode}\n")
    except OSError:
        print("\nCould not open file : ", file_name)
        sys.exit(f"-> Abandon du mode {mode}\n")


def main():
    """Fonction principale."""
    process_options()


if __name__ == '__main__':
    main()
