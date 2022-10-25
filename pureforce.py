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


def welcome_message():
    """Affiche un message de bienvenue.
    Affiche également des explications sur l'utilisation du script.
    """
    # On affiche le message de bienvenue :
    print("\n=========== Welcome on Pure-Force ! ============\n"
          "====== A free and open password generator. =======\n"
          "--------------------------------------------------\n"
          "Did you know that 'pain' means 'bread' in french ?")

    # On affiche la forme d'utilisation de pureforce :
    print("Usage : pureforce [OPTION]\n")

    # On affiche les options possibles :
    print("Possible options :\n"
          "-b (or --basic)              starts the basic mode, which generate an exhaustive list\n"
          "                             of passwords from a given range. Use basic interactive questions\n"
          "                             to modulate the range. It is the simplest mode but doesn't use\n"
          "                             any optimization.\n"
          "-i (or --intelligentia)      starts the intelligent mode, which generate an optimized list of\n"
          "                             passwords. It will use more interactive questions to select the\n"
          "                             most relevant passwords.\n"
          "-h (or --help)               shows the possible options (this menu).\n")


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
                print("you chose the help command !")
            elif option in ("-b", "--basic"):
                print("you chose the basic command !")
            elif option in ("-i", "--intelligentia"):
                print("you chose the intelligentia command !")


def main():
    """Fonction principale."""
    process_options()


if __name__ == '__main__':
    main()
