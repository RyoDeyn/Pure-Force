# Pure-Force

![project category](https://img.shields.io/badge/Project%20Category-Pain-red?style=flat-square)
![project version](https://img.shields.io/badge/Version-1.0-brightgreen?style=flat-square)
![number of available languages](https://img.shields.io/badge/Available%20Languages-2-blue?style=flat-square)

## About

### Project

Pure-force est un outil de génération de listes de mots de passe visant à être utilisé pour du brute-force.

Il propose deux modes de génération :
- un mode "basique" : génération exhaustive de mots de passe
- un mode "intelligent" : génération optimisée des mots de passe grâce à un choix assez large d'options et de données d'entrées. (COMING SOON)

L'objectif du 2e mode est d'optimiser au maximum le temps pris par le brute-force en générant les mots de passe les plus pertinents possibles.
Il se base pour cela sur les données entrées par l'utilisateur.

### Author

Cet outil a été réalisé par Ryo Deyn.

## Getting Started

### Requirements

Il est nécessaire d'avoir Python (version 3.10 ou supérieur) d'installé.   
Lien de téléchargement : https://www.python.org/downloads/

### Installation

Clone the repository with :
```sh
git clone https://github.com/RyoDeyn/Pure-Force.git
```

Or you can directly download the .zip from https://github.com/RyoDeyn/Pure-Force.

## Usage

Dans un terminal :
```
python pureforce.py [OPTIONS]
```
Options possibles :
```
   -b (or --basic)              starts the basic mode, which generate an exhaustive list of
                                passwords from a given range. Use basic interactive questions
                                to modulate the range. It is the simplest mode but doesn't use
                                any optimization.
                                
   -i (or --intelligentia)      starts the intelligent mode, which generate an optimized list of
                                passwords. It will use more interactive questions to select the
                                most relevant passwords. (COMING SOON)
                                
   -v (or --version)            show the current version of the program.
   
   -h (or --help)               shows the possible options.
```
#### Démonstration du mode basic :

(En cours d'écriture ...)

Remarque :
Il est possible de fusionner des listes de mots de passe. Pour cela, il suffit de lancer le mode basic et d'entrer le nom d'un fichier existant.
Il vous sera alors proposé plusieurs options permettant d'ajouter les mots de passe générés au fichier existant.
Utile si par exemple on veut uniquement des mots de passe avec majuscules (AAA, BBB, …) mais aussi les mots de passe avec chiffres (111, 1234, …) mais pas les deux en même temps. Il suffit alors de les générer en utilisant deux fois le mode basic.

#### Démonstration du mode intelligent :

(COMING SOON)

## Roadmap :

- [ ] Mode intelligent
- [ ] Afficher une barre de progression lors de la génération
- [ ] Disponible en plusieurs langues
    - [ ] English
    - [ ] French

## License

This project is licensed under the terms of the MIT license.
