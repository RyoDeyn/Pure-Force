"""A python script that generates a list of passwords. To be used for brute-force.

Usage:
======
    python pureforce.py [OPTIONS]

    OPTIONS:
    -b (or --basic): start the basic mode.
    -i (or --intelligentia): start the intelligent mode. (COMING SOON)
    -v (or --version): display the current version of the program.
    -h (or --help): display the possible options.
"""

__author__ = "Alexandre Quéré aka Ryo Deyn"
__version__ = "v1.0.0-en"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2022 Alexandre Quéré"

import sys
import getopt
import array
import os


class TColor:
    """
    Store the different possible colors if we want to display colored text in the terminal.
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


mode = "unknown"

welcome_text = ("\n============ Welcome on Pure-Force ! ============\n"
                "== A free, open and simple password generator. ==\n"
                "-------------------------------------------------")

pain_hint = "Did you know that 'pain' means 'bread' in french ?\n"

usage_text = "Usage : pureforce [OPTION]\n"

options_text = ("Possible options :\n"
                "-b (or --basic)              start the basic mode, that generate an exhaustive list of\n"
                "                             passwords from a given range. Use basic interactive questions\n"
                "                             to modulate the range. It is the simplest mode but doesn't use\n"
                "                             any optimization.\n\n"
                "-i (or --intelligentia)      start the intelligent mode, that generate an optimized list of\n"
                "                             passwords. It will use more interactive questions to select the\n"
                f"                             most relevant passwords. {TColor.pink}(COMING SOON){TColor.end}\n\n"
                "-v (or --version)            display the current version of the program.\n\n"
                "-h (or --help)               display the possible options (this menu).\n")

project_title = r""" ______   __  __     ______     ______        ______   ______     ______     ______     ______    
/\  == \ /\ \/\ \   /\  == \   /\  ___\      /\  ___\ /\  __ \   /\  == \   /\  ___\   /\  ___\   
\ \  _-/ \ \ \_\ \  \ \  __<   \ \  __\      \ \  __\ \ \ \/\ \  \ \  __<   \ \ \____  \ \  __\   
 \ \_\    \ \_____\  \ \_\ \_\  \ \_____\     \ \_\    \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_/     \/_____/   \/_/ /_/   \/_____/      \/_/     \/_____/   \/_/ /_/   \/_____/   \/_____/ 
                                                                                                  """

version_text = "Pureforce version 1.0.0 english (https://github.com/RyoDeyn/Pure-Force)\n"

# Possible character sets :
minuscules_set = array.array('u', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

majuscules_set = array.array('u', [letter.upper() for letter in minuscules_set])

digit_set = array.array('u', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

special_char_set = array.array('u', ['&', '#', '@', '$', '*', '%', '/', '?', '!', '<', '>'])


def welcome_message():
    """Display a welcome message as wall as explanations about the use of this script.
    """
    # Display welcome message :
    print(welcome_text)
    print(pain_hint)

    # Display the usage of pureforce :
    print(usage_text)

    # Display possible options :
    print(options_text)


def process_options():
    """Manage script options and parameters."""

    try:
        couples, args_after = getopt.getopt(sys.argv[1:], "bivh", ["basic", "intelligentia", "version", "help"])
    except getopt.GetoptError as error:
        # Display error message :
        print("\nError : ", error)
        # We end the execution of the script :
        sys.exit("Use the option -h (or --help) to view the usage and possible options.\n")

    # If we run the script without any parameters or options :
    if len(couples) == 0 and len(args_after) == 0:
        welcome_message()
    # If we run the script with additional parameters :
    elif len(args_after) != 0:
        print("\nError : pureforce do not accept additional parameters")
        sys.exit("Use the option -h (or --help) to view the usage and possible options.\n")
    # If we run the script with several options at the same time :
    elif len(couples) > 1:
        print("\nError : pureforce do not accept several options at the same time.\n"
              "Example of correct use : python pureforce -b\n"
              "Example of incorrect use : python pureforce -b -i\n")
    # Case where the usage is correct :
    else:
        for option, value in couples:
            if option in ("-h", "--help"):
                help_option()
            elif option in ("-v", "--version"):
                version_option()
            elif option in ("-b", "--basic"):
                basic_option()
            elif option in ("-i", "--intelligentia"):
                print(f"{TColor.pink}The pain is cooking ...\n"
                      f"(The intelligent mode is not available yet.){TColor.end}")
                print("Beginning of beta intelligent mode ...")
                intelligent_option()


def help_option():
    """Display the help page.
    """
    print(welcome_text)
    print(usage_text)
    print(options_text)


def version_option():
    """Display the current version of the program.
    """
    print(version_text)


def basic_option():
    """Start the basic mode.
    """
    global mode
    mode = "basic"
    file_name, length_min, length_max, char_used, writing_mode = basic_message()

    # We check that the number of passwords to generate is not too high :
    pwd_number_ok, pwd_nb = check_pwd_number(length_min, length_max, len(char_used))

    if not pwd_number_ok:
        pwd_approximation = approximation(pwd_nb)
        print(f"\n{TColor.yellow}Warning : the number of passwords to generate is > "
              f"{format(pwd_approximation, '_d')}."
              f"\nThe generation time as well as the file size may be very high.\n"
              f"(Since these two parameters depend on the power of the machine as well as"
              f"the available storage, it may not be necessary to heed this warning.){TColor.end}\n")

        # The user is offered the choice to launch or abort the generation :
        do_we_exec = input(f"Do you still want to start the generation ? (Y/N) {TColor.red}(*){TColor.end}: ")
        while do_we_exec not in ['Y', 'N']:
            print(f"{TColor.red}Error : Available options : Y or N{TColor.end}")
            do_we_exec = input(f"Do you still want to start the generation ? (Y/N) {TColor.red}(*){TColor.end}: ")

        if do_we_exec == 'N':
            sys.exit("\nThe generation was cancelled successfully.\nExiting ...\n")

    print("\nGenerating passwords in progress...\n"
          f"\nOverview :\n"
          f"output file -> {file_name}\n"
          f"minimum length -> {length_min}\n"
          f"maximum length -> {length_max}\n"
          f"characters used -> {print_set_char(char_used)}\n")
    write_file(file_name, length_min, length_max, char_used, writing_mode)

    print(f"{TColor.green}Password generation completed successfully.{TColor.end}\n")


def intelligent_option():
    """Start the intelligent mode.
    """
    global mode
    mode = "intelligent"

    # We get the information needed for the generation :
    # file_name, length_min, length_max, char_used, writing_mode = intelligent_message()


def intelligent_message():
    # """Displays a welcome message when entering basic mode and
    # ask the user about information needed for the generation.
    #
    # Returns
    # -------
    # file_name : string
    #     Name of the file to store the passwords.
    # length_min : int
    #     Minimum length of passwords (included).
    # length_max : int
    #     Maximum length of passwords (included).
    # char_used : array
    #     Contains all the characters used.
    # writing_mode : string
    #     The mode to use on the file (write or append).
    # """
    # print("--------------------------------------------------")
    # print(project_title)
    # print(f"{TColor.green}Entering basic mode ...{TColor.end}\n"
    #       "\nThe list of passwords will be written to a txt file (default name: 'pforce-basic.txt')."
    #       f"\nRequired questions are marked with an {TColor.red}(*){TColor.end}.\n")
    #
    # file_name = ask_file_name("File name: ")
    # writing_mode = 'w'
    #
    # # If the file already exists :
    # if os.path.isfile(f"{os.path.abspath(os.getcwd())}/{file_name}"):
    #     print(f"{TColor.yellow}Warning : the file {file_name} already exists. Choose the option you want :"
    #           f"\n- create a new file (by changing the name) (1)"
    #           f"\n- override the existing file (2)"
    #           f"\n- append the generated passwords to the existing file (3){TColor.end}")
    #     file_option = input("--> ")
    #     while file_option not in ['1', '2', '3']:
    #         print(f"{TColor.red}Error : Available options : 1, 2 or 3.{TColor.end}")
    #         file_option = input("--> ")
    #
    #     # Traitement selon l'option choisie :
    #     if file_option == '1':
    #         file_name = ask_file_name("Choose a new file name: ")
    #     elif file_option == '2':
    #         writing_mode = 'w'
    #     elif file_option == '3':
    #         writing_mode = 'a'
    #     else:
    #         sys.exit("Error : unknown option.\nExiting ...")
    #
    # length_min = int_input(f"Minimum length of passwords {TColor.red}(*){TColor.end}: ")
    # length_max = int_input(f"Maximum length of passwords {TColor.red}(*){TColor.end}: ")
    #
    # while length_max < length_min:
    #     print(f"{TColor.red}Error : the maximum length cannot be less than the minimum length.{TColor.end}")
    #     length_max = int_input(f"Maximum length of passwords {TColor.red}(*){TColor.end}: ")
    #
    # min_set_used = yes_no_input(f"Do you want to use lowercase (a, b, c, ...) ? (Y/N) "
    #                             f"{TColor.red}(*){TColor.end}: ")
    # maj_set_used = yes_no_input(f"Do you want to use uppercase (A, B, C, ...) ? (Y/N) "
    #                             f"{TColor.red}(*){TColor.end}: ")
    # dig_set_used = yes_no_input(f"Do you want to use digits (0, 1, 2, ...) ? (Y/N) "
    #                             f"{TColor.red}(*){TColor.end}: ")
    # spe_set_used = yes_no_input(f"Do you want to use special characters (&, #, @, ...) ? (Y/N) "
    #                             f"{TColor.red}(*){TColor.end}: ")
    #
    # # If no character set selected, we stop the execution of the script:
    # stop_exec = True
    # for resp in [min_set_used, maj_set_used, dig_set_used, spe_set_used]:
    #     if resp == 'Y':
    #         stop_exec = False
    # if stop_exec:
    #     sys.exit(f"\n{TColor.orange}You did not select any character set, exiting ...{TColor.end}\n")
    #
    # char_used = array.array('u')
    #
    # if min_set_used == 'Y':
    #     char_used += minuscules_set
    # if maj_set_used == 'Y':
    #     char_used += majuscules_set
    # if dig_set_used == 'Y':
    #     char_used += digit_set
    # if spe_set_used == 'Y':
    #     char_used += special_char_set
    #
    # return file_name, length_min, length_max, char_used, writing_mode


def print_set_char(char_set):
    """
    Parameters
    ----------
    char_set : array
        An array containing all the characters to use.

    Returns
    -------
    string
        A clean display of all the characters of the array.
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
        The number to approximate.

    Returns
    -------
    int
        The approximation.
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
        The minimum length of passwords to generate.
    l_max : int
        The maximum length of passwords to generate.
    nb_char : int
        The number of possible characters.

    Returns
    -------
    pwd_number_ok : boolean
        If the number of passwords to generate is not too high.
    pwd_nb : int
        An approximation of the number of passwords to generate (less than or equal to the actual number).
    """

    pwd_nb = 0
    # We calculate the number of passwords to generate:
    for i in range(l_min, l_max + 1):
        pwd_nb += nb_char ** i

    pwd_number_ok = True

    if pwd_nb > 1_000_000_000:
        pwd_number_ok = False

    return pwd_number_ok, pwd_nb


def basic_message():
    """Displays a welcome message when entering basic mode and
    ask the user about information needed for the generation.

    Returns
    -------
    file_name : string
        Name of the file to store the passwords.
    length_min : int
        Minimum length of passwords (included).
    length_max : int
        Maximum length of passwords (included).
    char_used : array
        Contains all the characters used.
    writing_mode : string
        The mode to use on the file (write or append).
    """
    print("--------------------------------------------------")
    print(project_title)
    print(f"{TColor.green}Entering basic mode ...{TColor.end}\n"
          "\nThe list of passwords will be written to a txt file (default name: 'pforce-basic.txt')."
          f"\nRequired questions are marked with an {TColor.red}(*){TColor.end}.\n")

    file_name = ask_file_name("File name: ")
    writing_mode = 'w'

    # If the file already exists :
    if os.path.isfile(f"{os.path.abspath(os.getcwd())}/{file_name}"):
        print(f"{TColor.yellow}Warning : the file {file_name} already exists. Choose the option you want :"
              f"\n- create a new file (by changing the name) (1)"
              f"\n- override the existing file (2)"
              f"\n- append the generated passwords to the existing file (3){TColor.end}")
        file_option = input("--> ")
        while file_option not in ['1', '2', '3']:
            print(f"{TColor.red}Error : Available options : 1, 2 or 3.{TColor.end}")
            file_option = input("--> ")

        # Traitement selon l'option choisie :
        if file_option == '1':
            file_name = ask_file_name("Choose a new file name: ")
        elif file_option == '2':
            writing_mode = 'w'
        elif file_option == '3':
            writing_mode = 'a'
        else:
            sys.exit("Error : unknown option.\nExiting ...")

    length_min = int_input(f"Minimum length of passwords {TColor.red}(*){TColor.end}: ")
    length_max = int_input(f"Maximum length of passwords {TColor.red}(*){TColor.end}: ")

    while length_max < length_min:
        print(f"{TColor.red}Error : the maximum length cannot be less than the minimum length.{TColor.end}")
        length_max = int_input(f"Maximum length of passwords {TColor.red}(*){TColor.end}: ")

    min_set_used = yes_no_input(f"Do you want to use lowercase (a, b, c, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    maj_set_used = yes_no_input(f"Do you want to use uppercase (A, B, C, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    dig_set_used = yes_no_input(f"Do you want to use digits (0, 1, 2, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")
    spe_set_used = yes_no_input(f"Do you want to use special characters (&, #, @, ...) ? (Y/N) "
                                f"{TColor.red}(*){TColor.end}: ")

    # If no character set selected, we stop the execution of the script:
    stop_exec = True
    for resp in [min_set_used, maj_set_used, dig_set_used, spe_set_used]:
        if resp == 'Y':
            stop_exec = False
    if stop_exec:
        sys.exit(f"\n{TColor.orange}You did not select any character set, exiting ...{TColor.end}\n")

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
    """Asks the user to enter a file name, then performs a check on the entered value.

    Parameters
    ----------
    question : string
        The question to display to the user.

    Returns
    -------
    string
        The file name entered by the user.
    """
    file_name = input(question)
    if file_name == "":
        file_name = "pforce-basic.txt"
    elif ".txt" not in file_name:
        file_name += ".txt"
    while len(file_name) > 200:
        print(f"{TColor.red}Error : the file name must not exceed 200 characters.{TColor.end}")
        file_name = input(question)

    return file_name


def int_input(question):
    """Asks the user to enter an integer, then performs a check on the entered value.

    Parameters
    ----------
    question : string
        The question to display to the user.

    Returns
    -------
    int
        The integer entered by the user.
    """
    v_string = input(question)
    v_int = 0

    # We check that the user has indeed entered an integer:
    try:
        v_int = int(v_string)
        # Check that the integer is greater than 1:
        if v_int < 1:
            print(f"{TColor.red}Error : you must enter an integer greater than or equal to 1.{TColor.end}")
            # We ask the user again for input:
            v_int = int_input(question)
    except ValueError as error:
        # We display an error message :
        print(f"{TColor.red}Error : you must enter an integer.{TColor.end}")
        # We ask the user again for input:
        v_int = int_input(question)

    return v_int


def yes_no_input(question):
    """Asks the user to enter 'Y' or 'N', then performs a check on the entered value.

    Parameters
    ----------
    question : string
        The question to display to the user.

    Returns
    -------
    string
        The response entered by the user.
    """
    rep = input(question)
    while rep not in ['Y', 'N']:
        print(f"{TColor.red}Error : you must enter 'Y' or 'N'.{TColor.end}")
        # We ask the user again for input :
        rep = input(question)

    return rep


def write_file(file_name, length_min, length_max, char_used, writing_mode):
    """Writes a list of passwords to a txt file.

    Parameters
    ----------
    file_name : string
        The name of the file where the passwords will be written.
    length_min : int
        The minimum length of passwords (included).
    length_max : int
        The maximum length of passwords (included).
    char_used : array
        The characters used.
    writing_mode : string
        The mode to use on the file (write or append).

        If the file does not exist, create it.
    """
    try:
        with open(file_name, writing_mode) as file:
            generate_basic_passwd(file, length_min, length_max, char_used)
    except PermissionError:
        print("\nError : permission denied.\n"
              "Could not open file : ", file_name)
        sys.exit(f"-> Exiting {mode} mode ...\n")
    except OSError:
        print("\nCould not open file : ", file_name)
        sys.exit(f"-> Exiting {mode} mode ...\n")


def generate_basic_passwd(file, length_min, length_max, char_set):
    """Generates and writes passwords for the basic mode.

    Parameters
    ----------
    file : TextIO
        The file where the passwords will be written.
    length_min : int
        The minimum length of passwords (included).
    length_max : int
        The maximum length of passwords (included).
    char_set : array
        The characters used.
    """
    # Loop that goes through every possible length :
    for length in range(length_min, length_max + 1):

        # The character index in char_set :
        indice_cs = 0

        # We write the first password for this length:
        mdp = ""
        for j in range(length):
            mdp += char_set[indice_cs]
        file.write(f"{mdp}\n")

        # Index of the character to modify:
        indice_to_modify = length - 1

        # We create all the passwords for a given length:
        for i in range((len(char_set) ** length) - 1):

            while mdp[indice_to_modify] == char_set[len(char_set) - 1]:
                indice_to_modify -= 1

            nouveau_mdp = ""

            # We copy the previous password in the new password except for 1 character that we modify :
            for indice_courant in range(length):
                if indice_courant == indice_to_modify:
                    indice_cs = char_set.index(mdp[indice_to_modify]) + 1
                    nouveau_mdp += char_set[indice_cs]
                    # If the password is not complete, we set all the following characters to cs[0] :
                    if indice_courant < (length - 1):
                        for indice_restant in range(indice_courant + 1, length):
                            nouveau_mdp += char_set[0]
                            indice_to_modify = length - 1
                        break
                else:
                    nouveau_mdp += mdp[indice_courant]

            mdp = nouveau_mdp
            # We write the new password :
            file.write(f"{nouveau_mdp}\n")


def main():
    """Main function."""
    process_options()


if __name__ == '__main__':
    main()
