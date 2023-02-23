> [Kentin LE HIR](https://github.com/Dinostorm) - FIPA SE 2023

## Introduction

Plate Ball Asserv est un programme permettant l'asservissement d'une bille sur la maquette dédiée. 

Le but de cette programme est d'assurer la présence de la bille au milieu de la maquette. 

![photo_maquette](https://github.com/Dinostorm/plate_ball_asserv/blob/main/image/photo_maquette.jpg)

## Installation

Le projet se base sur l'utilisation d'une Raspberry Pi, d'une caméra Raspberry et de servomoteurs. 

Copie des fichiers sources depuis Github :

```shell
git clone https://github.com/Dinostorm/plate_ball_asserv.git
```

Le projet fonctionne avec Python et dépend des bibliothèques suivantes :

- OpenCV
- RPi.GPIO
- picamera
- piservo

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
