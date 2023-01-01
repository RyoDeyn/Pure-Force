# Pure-Force

![project category](https://img.shields.io/badge/Categorie%20de%20projet-Pain-red?style=flat-square)
![project version](https://img.shields.io/badge/Version-1.0.0-brightgreen?style=flat-square)
![number of available languages](https://img.shields.io/badge/Langages%20disponibles-2-blue?style=flat-square)

## A propos

### Projet

Pure-force est un outil de génération de listes de mots de passe visant à être utilisé pour du brute-force.

Il propose deux modes de génération :
- un mode "basique" : génération exhaustive de mots de passe
- un mode "intelligent" : génération optimisée des mots de passe grâce à un choix assez large d'options et de données d'entrées. (BIENTÔT DISPONIBLE)

L'objectif du 2e mode est d'optimiser au maximum le temps pris par le brute-force en générant les mots de passe les plus pertinents possibles.
Il se base pour cela sur les données entrées par l'utilisateur.

### Auteur

Cet outil a été réalisé par Ryo Deyn.

## Pour commencer

### Eléments requis

Il est nécessaire d'avoir Python (version 3.10 ou supérieur) d'installé.   
Lien de téléchargement : https://www.python.org/downloads/

### Installation

Cloner le répertoire avec git :
```sh
git clone https://github.com/RyoDeyn/Pure-Force.git
```

Il est également possible de télécharger directement le .zip depuis https://github.com/RyoDeyn/Pure-Force.

## Utilisation

Dans un terminal :
```
python pureforce.py [OPTIONS]
```
Options possibles :
```
   -b (ou --basic)              lance le mode basic, qui génère une liste exhaustive de mots
                                de passe à partir des paramètres donnés par l'utilisateur.
                                Utilise des questions interactives basiques afin de modifier
                                ces paramètres. Il s'agit du mode de génération le plus simple
                                mais il n'utilise aucune optimisation.
                                
   -i (ou --intelligentia)      lance le mode intelligent, qui génère une liste optimisée de
                                mots de passe. Il utilise plus de questions interactives afin
                                de sélectionner les mots de passe les plus pertinents.
                                (BIENTÔT DISPONIBLE)
                               
   -v (ou --version)            affiche la version actuelle du programme.
   
   -h (ou --help)               affiche les options disponibles.
```
#### Démonstration du mode basic :

(En cours d'écriture ...)

Remarque :
Il est possible de fusionner des listes de mots de passe. Pour cela, il suffit de lancer le mode basic et d'entrer le nom d'un fichier existant.
Il vous sera alors proposé plusieurs options permettant d'ajouter les mots de passe générés au fichier existant.
Utile si par exemple on veut uniquement des mots de passe avec majuscules (AAA, BBB, …) mais aussi les mots de passe avec chiffres (111, 1234, …) mais pas les deux en même temps. Il suffit alors de les générer en utilisant deux fois le mode basic.

#### Démonstration du mode intelligent :

(BIENTÔT DISPONIBLE)

## Fonctionnalités futures :

- [x] Disponible en plusieurs langues
    - [x] Anglais
    - [x] Français
- [ ] Mode intelligent
- [ ] Afficher une barre de progression lors de la génération

## License

Ce projet est sous license selon les termes de la license MIT.
