# Système

## PID
### Présentation de la classe PID
La classe PID est un contrôleur de rétroaction pour réguler un processus. PID est l'abréviation de "Proportional-Integral-Derivative", ce qui signifie que le contrôleur ajuste la sortie en utilisant trois termes : proportionnel, intégral et dérivé.

Les coefficients P, I et D (Kp, Ki et Kd) sont utilisés pour régler les trois termes de manière à obtenir la réponse désirée du processus de contrôle. Le coefficient P est proportionnel à l'erreur actuelle, le coefficient I est proportionnel à l'intégrale des erreurs passées et le coefficient D est proportionnel à la dérivée de l'erreur actuelle.

La méthode *init()* initialise les coefficients PID avec les valeurs P, I et D fournies et définit le temps d'échantillonnage à zéro. Le temps d'échantillonnage est le temps entre chaque mesure de l'entrée et de la sortie.

La méthode *clear()* réinitialise les calculs PID et les coefficients.

La méthode *update()* calcule la valeur PID pour une valeur de retour donnée en utilisant la formule PID. Il calcule l'erreur entre la valeur de consigne (SetPoint) et la valeur de retour (feedback_value), puis calcule les termes proportionnel, intégral et dérivé. Il applique ensuite la somme pondérée de ces termes pour calculer la sortie du contrôleur.

Les méthodes *setKp(), setKi(), setKd()* sont utilisées pour régler les coefficients PID de manière indépendante.

La méthode *setWindup()* est utilisée pour définir une valeur de garde contre les erreurs d'intégration accumulées.

La méthode *setSampleTime()* est utilisée pour définir le temps d'échantillonnage pour le calcul PID.

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

    Servo(gpio, min_value=0, max_value=180, min_pulse=0.5, max_pulse=2.4, frequency=50)

gpio : Le numéro de la broche gpio à laquelle le servomoteur est connecté.

min_value : Angle minimum du servomoteur (vitesse si c'est un servomoteur de rotation).

max_value : Angle maximum du servomoteur (vitesse si c'est un servomoteur de rotation).

min_pulse : Largeur minimale de l'impulsion de commande du servomoteur (milliseconde).

max_pulse : Largeur maximale de l'impulsion de commande du servomoteur (milliseconde).

frequency : Fréquence PWM du servomoteur.

### Utilisation de la classe Servo

Dans un premier temps, deux servomoteurs sont initialisés , un pour l'axe X et l'autre pour l'axe Y, en utilisant les numéros de broches GPIO 13 et 18. Ensuite, les servos sont créés en utilisant la classe Servo de piServoCtl.

```python
# GPIO servo
GPIO_servo_x = 13
GPIO_servo_y = 18

# Init Servo
servo_x = Servo(GPIO_servo_x, min_value=0, max_value=180)
servo_y = Servo(GPIO_servo_y, min_value=0, max_value=180)

servo_x.start()
servo_y.start()
```

En outre, la valeur minimale et maximale pour la position du servo sont définies à 0 et 180 degrés respectivement, ce qui signifie que le servo peut tourner de 0 à 180 degrés. Enfin, la méthode start() est appelée pour commencer à générer les signaux PWM et faire tourner les servos.

Ensuite l'angle_inital_x et l'angle_inital_y sont initialisés. Ils représentent les angles pour lequelles la planche est droite. Puis le calcule des commandes est envoyées aux servos X et Y en additionnant à ces angles les valeurs de sortie (output_x et output_y) du PID calculé précédemment.
```python
# Command to send to servo
angle_inital_x=68
angle_inital_y=137

commande_servoX = int(angle_inital_x+output_x)
commande_servoY = int(angle_inital_y+output_y)
```
Les variables commande_servoX et commande_servoY contiennent respectivement les commandes à envoyer aux servos X et Y. Ces commandes sont exprimées en degrés et sont obtenues en additionnant la valeur de la sortie output_x à l'angle initial angle_inital_x pour le servo X, et en additionnant la valeur de la sortie output_y à l'angle initial angle_inital_y pour le servo Y.

Il faut ensuite délimiter les limites d'angles de commandes envoyés aux servos pour éviter qu'ils ne dépassent les limites physiques de leurs mouvements et pour éviter des angles de commandes trop importants. La valeur de la variable angle_limite est la valeur maximale de l'angle que les servos peuvent atteindre par rapport à leur position initiale.
```python 
# Angle max of the servo
angle_limite = 5
if commande_servoX > angle_inital_x + angle_limite :
    commande_servoX = angle_inital_x + angle_limite
    
if commande_servoX < angle_inital_x - angle_limite :
    commande_servoX = angle_inital_x - angle_limite
    
if commande_servoY > angle_inital_y + angle_limite:
    commande_servoY = angle_inital_y + angle_limite
    
if commande_servoY < angle_inital_y - angle_limite :
    commande_servoY = angle_inital_y - angle_limite
```
Les quatre instructions if comparent les valeurs de commande_servoX et commande_servoY avec les angles initiaux angle_inital_x et angle_inital_y respectivement, et ajustent les valeurs si nécessaire pour s'assurer qu'elles ne dépassent pas les limites.

Ainsi, si la commande envoyée pour le servo X dépasse la limite supérieure (angle initial + limite d'angle), la commande est ajustée pour être égale à la limite supérieure. De même, si la commande est inférieure à la limite inférieure (angle initial - limite d'angle), elle est ajustée pour être égale à la limite inférieure. Les mêmes ajustements sont appliqués à la commande envoyée pour le servo Y.

Par la suite, les servomoteurs se déplaces vers les nouvelles positions déterminées par les variables "commande_servoX" et "commande_servoY" qui ont été calculées en fonction de la sortie des PID et de la valeur initiale de l'angle.
```python    
# Give the serve new angle
servo_x.write(commande_servoX)
servo_y.write(commande_servoY)
```
La méthode "write" est utilisée pour envoyer les nouvelles positions de commande aux servomoteurs. Elle prend un argument qui est la valeur de la commande à envoyer, qui est exprimée en degrés. Les servomoteurs sont ainsi déplacés vers les angles correspondants.

Ainsi de suite, à chaque nouvelle coordonnées de la balle envoyée par la caméra au PID, les servomoteurs sont déplacés vers les angles correspondants.