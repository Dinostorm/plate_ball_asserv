> [Kentin LE HIR](https://github.com/Dinostorm) - FIPA SE 2023

## Introduction

Plate Ball Asserv est programme permettant l'asservissement d'une bille sur la maquette dédiée. 

Le but de cette programme est d'assurer la présence de la bille au milieu de la maquette. 

## Installation

Le projet se base sur l'utilisation d'une Raspberry Pi, d'une caméra Raspberry et de servomoteurs. 

Copie des fichiers sources depuis Github :

```shell
git clone https://github.com/Dinostorm/plate_ball_asserv.git
```

Le projet fonctionne avec Python :

    3.7
    3.8
    3.9
    3.10
    3.11

Et dépend des bibliothèques suivantes :

- OpenCV
- RPi.GPIO
- picamera
- piServoCtl (version : 1.1.0)

## Lancement

Il faut d'abord initiliser les servomoteurs pigpio daemon grâce à la commande suivante :

```shell
sudo pigpiod
```

Puis aller dans le dossier `programmes` du projet :

```shell
cd programme
```

Et exécuter la commande suivante :

```shell
python3 plate_ball_asserv.py
```

Et voilà !