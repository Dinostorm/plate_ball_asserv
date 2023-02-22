## Contrôle servo moteur en fonction des coordonnées de la bille et du PID
# Importez les bibliothèques nécessaires
from detect_ball import *
import time
from PID import PID
import subprocess

# Initialisez les paramètres du PID
pid_x =  PID(P=1, I=0, D=0.000)
pid_y =  PID(P=1, I=0, D=0.000)

print(pid_x)
print(pid_y)

#Setpoint du centre du plateau
pid_x.SetPoint=319
pid_y.SetPoint=239
while True:

    #Récupération des valeurs de cx et cy
    cx,cy=func_detect_ball()

    pid_y.update(cy)
    pid_x.update(cx)

    #Output = pid_x.SetPoint - cx
    output_x = pid_x.output
    output_y = pid_y.output

    print(output_x)
    print(output_y)

    # Angle a transmettre aux servomoteurs
