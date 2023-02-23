# Système

## PID
### Présentation de la classe PID
La classe PID est un contrôleur de rétroaction pour réguler un processus. PID est l'abréviation de "Proportional-Integral-Derivative", ce qui signifie que le contrôleur ajuste la sortie en utilisant trois termes : proportionnel, intégral et dérivé.

Les coefficients P, I et D (Kp, Ki et Kd) sont utilisés pour régler les trois termes de manière à obtenir la réponse désirée du processus de contrôle. Le coefficient P est proportionnel à l'erreur actuelle, le coefficient I est proportionnel à l'intégrale des erreurs passées et le coefficient D est proportionnel à la dérivée de l'erreur actuelle.

La méthode init() initialise les coefficients PID avec les valeurs P, I et D fournies et définit le temps d'échantillonnage à zéro. Le temps d'échantillonnage est le temps entre chaque mesure de l'entrée et de la sortie.

La méthode clear() réinitialise les calculs PID et les coefficients.

La méthode update() calcule la valeur PID pour une valeur de retour donnée en utilisant la formule PID. Il calcule l'erreur entre la valeur de consigne (SetPoint) et la valeur de retour (feedback_value), puis calcule les termes proportionnel, intégral et dérivé. Il applique ensuite la somme pondérée de ces termes pour calculer la sortie du contrôleur.

Les méthodes setKp(), setKi(), setKd() sont utilisées pour régler les coefficients PID de manière indépendante.

La méthode setWindup() est utilisée pour définir une valeur de garde contre les erreurs d'intégration accumulées.

La méthode setSampleTime() est utilisée pour définir le temps d'échantillonnage pour le calcul PID.

### Utilisation de la classe PID
``` python
# Init PID 
pid_x =  PID(P=coefX, I=coefIX, D=coefVX)
pid_y =  PID(P=coefY, I=coefIY, D=coefVY)

# Setpoint the center of plate
pid_x.SetPoint=center_x
pid_y.SetPoint=center_y
```

Ce code, un régulateur PID est initialisé pour les axes x et y avec des gains proportionnels, intégraux et dérivés spécifiés par coefX, coefIX, coefVX pour l'axe x, et coefY, coefIY, coefVY pour l'axe y.

Ensuite, le code définit un point de consigne (SetPoint) pour chaque contrôleur, qui représente le centre de la plaque en x et en y. Ce point de consigne est utilisé comme référence pour le contrôleur, qui ajuste la sortie en fonction de l'erreur entre la position actuelle de la cible (récupérée à partir de la vidéo) et la position souhaitée (SetPoint).

``` python
pid_y.update(cy)
pid_x.update(cx)

# Get the feedback of the PID
output_x = int(pid_x.output)
output_y = int(pid_y.output)
```
Ces deux lignes de code appellent la méthode update de l'objet pid_x et pid_y pour calculer la valeur de la sortie (output) du PID en utilisant la valeur courante de la variable de retour (feedback_value).

Ensuite, la sortie (output) du PID pour l'axe X est stockée dans la variable output_x et la sortie (output) pour l'axe Y est stockée dans la variable output_y. Les deux variables output_x et output_y seront utilisées pour calculer l'angle à envoyer au servomoteur pour recentrer la bille au centre du plateau.

## Servomoteur

### Présentation de la classe Servo

La classe Servo de piServoCtl est une classe permettant de contrôler les servomoteurs sur Raspberry Pi. Elle utilise une bibliothèque de contrôle de servomoteurs appelée "pigpio" pour envoyer des signaux PWM aux servomoteurs.

La classe Servo de piServoCtl a plusieurs méthodes pour configurer et contrôler les servomoteurs.

Dans notre cas, les méthodes utilisées sont :

- *Servo* : Pour initialiser le servomoteur
- *write* : Pour envoyer un angle au servomoteur
- *stop* : Pour arrêter le servomoteur
- *start* : Pour démarrer le servomoteur 

La classe Servo est initialisée avec un numéro de GPIO sur lequel le servomoteur est connecté. 