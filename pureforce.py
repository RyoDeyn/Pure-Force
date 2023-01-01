"""Script de génération de listes de mots de passe pour du brute-force.

Utilisation:
======
    python pureforce.py [OPTIONS]

    OPTIONS:
    -b (ou --basic): lance le mode basic.
    -i (ou --intelligentia): lance le mode intelligent. (BIENTÔT DISPONIBLE)
    -v (ou --version): affiche la version actuelle du programme.
    -h (or --help): affiche les options disponibles.
"""

__author__ = "Alexandre Quéré aka Ryo Deyn"
__version__ = "v1.0.0-fr"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2022 Alexandre Quéré"

import sys
import getopt
import array
import os


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


# On définit les variables globales :
mode = "inconnu"

welcome_text = ("\n=================== Bienvenue sur Pure-Force ! ===================\n"
                "== Un générateur de mots de passe gratuit et simple à utiliser. ==\n"
                "------------------------------------------------------------------")

pain_hint = "Savais-tu que 'pain' veut dire 'douleur' en anglais ?\n"

usage_text = "Utilisation : pureforce [OPTION]\n"

options_text = ("Options possibles :\n"
                "-b (ou --basic)              lance le mode basic, qui génère une liste exhaustive de mots\n"
                "                             de passe à partir des paramètres donnés par l'utilisateur.\n"
                "                             Utilise des questions interactives basiques afin de modifier\n"
                "                             ces paramètres. Il s'agit du mode de génération le plus simple\n"
                "                             mais il n'utilise aucune optimisation.\n\n"
                "-i (ou --intelligentia)      lance le mode intelligent, qui génère une liste optimisée de\n"
                "                             mots de passe. Il utilise plus de questions interactives afin\n"
                "                             de sélectionner les mots de passe les plus pertinents.\n"
                f"                             {TColor.pink}(BIENTÔT DISPONIBLE){TColor.end}\n\n"
                "-v (ou --version)            affiche la version actuelle du programme.\n\n"
                "-h (ou --help)               affiche les options disponibles (ce menu).\n")

project_title = r""" ______   __  __     ______     ______        ______   ______     ______     ______     ______    
/\  == \ /\ \/\ \   /\  == \   /\  ___\      /\  ___\ /\  __ \   /\  == \   /\  ___\   /\  ___\   
\ \  _-/ \ \ \_\ \  \ \  __<   \ \  __\      \ \  __\ \ \ \/\ \  \ \  __<   \ \ \____  \ \  __\   
 \ \_\    \ \_____\  \ \_\ \_\  \ \_____\     \ \_\    \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_/     \/_____/   \/_/ /_/   \/_____/      \/_/     \/_____/   \/_/ /_/   \/_____/   \/_____/ 
                                                                                                  """

version_text = "Pureforce version 1.0.0 français (https://github.com/RyoDeyn/Pure-Force)\n"

# Exemples d'ensembles de caractères possibles :
minuscules_set = array.array('u', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

majuscules_set = array.array('u', [letter.upper() for letter in minuscules_set])

digit_set = array.array('u', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

special_char_set = array.array('u', ['&', '#', '@', '$', '*', '%', '/', '?', '!', '<', '>'])


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
        couples, args_after = getopt.getopt(sys.argv[1:], "bivh", ["basic", "intelligentia", "version", "help"])
    except getopt.GetoptError as error:
        # On affiche un message d'erreur :
        print("\nErreur : ", error)
        # On termine l'exécution du script :
        sys.exit("Utilisez l'option -h (ou --help) pour afficher les options possibles.\n")

    # Si on lance le script sans aucuns paramètres ou options :
    if len(couples) == 0 and len(args_after) == 0:
        welcome_message()
    # Si on lance le script avec des arguments supplémentaires :
    elif len(args_after) != 0:
        print("\nErreur : pureforce n'accepte pas de paramètres supplémentaires.")
        sys.exit("Utilisez l'option -h (ou --help) pour afficher les options possibles.\n")
    # Si on lance le script avec plusieurs options en même temps :
    elif len(couples) > 1:
        print("\nErreur : pureforce n'accepte pas plusieurs options en même temps.\n"
              "Exemple d'utilisation correcte : python pureforce -b\n"
              "Exemple d'utilisation incorrecte : python pureforce -b -i\n")
    # Cas où l'usage est correcte :
    else:
        for option, value in couples:
            if option in ("-h", "--help"):
                help_option()
            elif option in ("-v", "--version"):
                version_option()
            elif option in ("-b", "--basic"):
                basic_option()
            elif option in ("-i", "--intelligentia"):
                print(f"{TColor.pink}Le pain est en train de cuire ...\n"
                      f"(Le mode intelligent n'est pas encore disponible.){TColor.end}")


def help_option():
    """Affiche la page d'aide.
    """
    print(welcome_text)
    print(usage_text)
    print(options_text)


def version_option():
    """Affiche la version actuelle du programme
    """
    print(version_text)


def basic_option():
    """Lance le mode basic.
    """
    global mode
    mode = "basic"
    file_name, length_min, length_max, char_used, writing_mode = basic_message()

    # On vérifie que le nombre de mdp à générer n'est pas trop élevé :
    pwd_number_ok, pwd_nb = check_pwd_number(length_min, length_max, len(char_used))

    if not pwd_number_ok:
        pwd_approximation = approximation(pwd_nb)
        print(f"\n{TColor.yellow}Attention : le nombre de mots de passe à générer est > "
              f"{format(pwd_approximation, '_d')}."
              f"\nLe temps de génération ainsi que la taille du fichier peuvent être très élevés.\n"
              f"(Étant donné que ces deux paramètres dépendent de la puissance de la machine ainsi "
              f"que du stockage disponible, il n'est peut-être pas nécessaire de tenir compte de cet "
              f"avertissement.){TColor.end}\n")

        # On offre à l'utilisateur le choix de lancer ou d'avorter la génération :
        do_we_exec = input(f"Voulez-vous tout de même lancer la génération ? (O/N) {TColor.red}(*){TColor.end}: ")
        while do_we_exec not in ['O', 'N']:
            print(f"{TColor.red}Erreur : Options disponibles : O ou N{TColor.end}")
            do_we_exec = input(f"Voulez-vous tout de même lancer la génération ? (O/N) {TColor.red}(*){TColor.end}: ")

        if do_we_exec == 'N':
            sys.exit("\nAnnulation du lancement de la génération.\nSortie ...\n")

    print("\nGénération des mots de passe en cours ...\n"
          f"\nRécapitulatif :\n"
          f"fichier de sortie -> {file_name}\n"
          f"longueur minimale -> {length_min}\n"
          f"longueur maximale -> {length_max}\n"
          f"caractères utilisés -> {print_set_char(char_used)}\n")
    write_file(file_name, length_min, length_max, char_used, writing_mode)

    print(f"{TColor.green}La génération des mots de passe est terminée.{TColor.end}\n")


def print_set_char(char_set):
    """
    Parameters
    ----------
    char_set : array
        Un tableau contenant tous les caractères à utiliser.

    Returns
    -------
    string
        Un affichage propre des caractères de ce tableau.
    """

    clean_affichage = "["
    for char in char_set:
        clean_affichage += char + " ; "

    clean_affichage = clean_affichage[:-3] + "]"

    return clean_affichage


def approximation(nb):
    """
    Parameters
    ----------
    nb : int
        Le nombre à approximer.

    Returns
    -------
    int
        L'approximation.
    """

    # On définit les 8 premiers chiffres à 0 :
    nb = int(nb / 10 ** 8)
    nb = nb * (10 ** 8)

    return nb


def check_pwd_number(l_min, l_max, nb_char):
    """
    Parameters
    ----------
    l_min : int
        La longueur minimale des mots de passe à générer.
    l_max : int
        La longueur maximale des mots de passe à générer.
    nb_char : int
        Le nombre de caractères possibles.

    Returns
    -------
    pwd_number_ok : boolean
        Si le nombre de mots de passe à générer est trop élevé.
    pwd_nb : int
        Une approximation du nombre de mots de passe à générer (valeur inférieure ou égale au nombre réelle).
    """

    pwd_nb = 0
    # On calcule le nombre de mots de passe à générer :
    for i in range(l_min, l_max + 1):
        pwd_nb += nb_char ** i

    pwd_number_ok = True

    if pwd_nb > 1_000_000_000:
        pwd_number_ok = False

    return pwd_number_ok, pwd_nb


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
    print(f"{TColor.green}Mode basic démarré ...{TColor.end}\n"
          "\nLa liste des mots de passe sera écrite dans un fichier txt (nom par défaut : 'pforce-basic.txt')."
          f"\nLes questions obligatoires sont marquées avec un {TColor.red}(*){TColor.end}.\n")

    file_name = ask_file_name("Nom du fichier txt: ")
    writing_mode = 'w'

    # Si le fichier existe déjà :
    if os.path.isfile(f"{os.path.abspath(os.getcwd())}\\{file_name}"):
        print(f"{TColor.yellow}Attention : le fichier {file_name} existe déjà. Choisissez parmi une des options :"
              f"\n- créer un nouveau fichier (en changeant le nom) (1)"
              f"\n- ré-écrire le fichier existant (2)"
              f"\n- ajouter les mots de passe générés au fichier existant (3){TColor.end}")
        file_option = input("--> ")
        while file_option not in ['1', '2', '3']:
            print(f"{TColor.red}Erreur : Options disponibles : 1, 2 ou 3.{TColor.end}")
            file_option = input("--> ")

        # Traitement selon l'option choisie :
        if file_option == '1':
            file_name = ask_file_name("Choisissez un nouveau nom de fichier: ")
        elif file_option == '2':
            writing_mode = 'w'
        elif file_option == '3':
            writing_mode = 'a'
        else:
            sys.exit("Erreur : option inconnue.\nSortie ...")

    length_min = int_input(f"Longueur minimale des mots de passe {TColor.red}(*){TColor.end}: ")
    length_max = int_input(f"Longueur maximale des mots de passe {TColor.red}(*){TColor.end}: ")

    while length_max < length_min:
        print(f"{TColor.red}Erreur : la longueur maximale ne peut être inférieure à la longueur minimale.{TColor.end}")
        length_max = int_input(f"Longueur maximale des mots de passe {TColor.red}(*){TColor.end}: ")

    min_set_used = yes_no_input(f"Voulez-vous utiliser les minuscules (a, b, c, ...) ? (O/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    maj_set_used = yes_no_input(f"Voulez-vous utiliser les majuscules (A, B, C, ...) ? (O/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    dig_set_used = yes_no_input(f"Voulez-vous utiliser les chiffres (0, 1, 2, ...) ? (O/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    spe_set_used = yes_no_input(f"Voulez-vous utiliser des char spéciaux (&, #, @, ...) ? (O/N) "
                                f"{TColor.red}(*){TColor.end}: ")

    # Si aucun char selectionné, on arrete l'execution du script :
    stop_exec = True
    for resp in [min_set_used, maj_set_used, dig_set_used, spe_set_used]:
        if resp == 'O':
            stop_exec = False
    if stop_exec:
        sys.exit(f"\n{TColor.orange}Vous n'avez sélectionné aucuns caractères, sortie ...{TColor.end}\n")

    char_used = array.array('u')

    if min_set_used == 'O':
        char_used += minuscules_set
    if maj_set_used == 'O':
        char_used += majuscules_set
    if dig_set_used == 'O':
        char_used += digit_set
    if spe_set_used == 'O':
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
            v_int = int_input(question)
    except ValueError as error:
        # On affiche un message d'erreur :
        print(f"{TColor.red}Erreur : vous devez entrer un entier.{TColor.end}")
        # On re-demande l'entrée à l'utilisateur :
        v_int = int_input(question)

    return v_int


def yes_no_input(question):
    """Demande à l'utilisateur d'entrer 'O' ou 'N', puis effectue une vérification sur la valeur entrée.

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
    while rep not in ['O', 'N']:
        print(f"{TColor.red}Erreur : vous devez entrer 'O' ou 'N'.{TColor.end}")
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
        print("\nErreur : permission refusée.\n"
              "Le fichier ", file_name, " n'a pas pu être ouvert.")
        sys.exit(f"-> Abandon du mode {mode}\n")
    except OSError:
        print("\nLe fichier ", file_name, " n'a pas pu être ouvert.")
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
        for i in range((len(char_set) ** length) - 1):

            while mdp[indice_to_modify] == char_set[len(char_set) - 1]:  # ancien : if indice_cs == (len(char_set) - 1):
                indice_to_modify -= 1

            nouveau_mdp = ""

            # On recopie le mdp précédent dans le nouveau mdp sauf pour 1 caractère qu'on modifie :
            for indice_courant in range(length):
                if indice_courant == indice_to_modify:
                    indice_cs = char_set.index(mdp[indice_to_modify]) + 1
                    nouveau_mdp += char_set[indice_cs]
                    # Si le mot de passe n'est pas terminé, on met tous les caractères suivants à cs[0] :
                    if indice_courant < (length - 1):
                        for indice_restant in range(indice_courant + 1, length):
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
