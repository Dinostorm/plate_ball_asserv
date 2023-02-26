# Import libraries
from detect_ball import *
from detect_contours import *
from piservo import Servo
from PID import PID
import time

# GPIO servo
GPIO_servo_x = 13
GPIO_servo_y = 18

# Init Servo
servo_x = Servo(GPIO_servo_x, min_value=0, max_value=180)
servo_y = Servo(GPIO_servo_y, min_value=0, max_value=180)

servo_x.start()
servo_y.start()

time.sleep(0.05)

# Init of the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

# allow the camera to warmup
time.sleep(0.5)

# PID parameters
coefX = 0.05
coefY = 0.05
coefIX = 0.02
coefIY = 0.02
coefVX = 0.002
coefVY = 0.002 

# Init PID 
pid_x =  PID(P=coefX, I=coefIX, D=coefVX)
pid_y =  PID(P=coefY, I=coefIY, D=coefVY)

print(pid_x)
print(pid_y)

center_x,center_y = detect_center(camera)

# Setpoint the center of plate
pid_x.SetPoint=center_x
pid_y.SetPoint=center_y

while True:
    
    # Reset of servo command
    commande_servoX = 0
    commande_servoY = 0
    
    # Get the center of the ball
    cy,cx=func_detect_ball(center_x,center_y,camera)

    pid_y.update(cy)
    pid_x.update(cx)

    # Get the feedback of the PID
    output_x = int(pid_x.output)
    output_y = int(pid_y.output)
    
    print(f"output_x = {output_x}, output_y = {output_y}")

    # Command to send to servo
    angle_inital_x=68
    angle_inital_y=137
    
    commande_servoX = int(angle_inital_x+output_x)
    commande_servoY = int(angle_inital_y+output_y)
    
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
    
    print(f"commande_servoX = {commande_servoX}, commande_servoY = {commande_servoY}")
    
    # Give the serve new angle
    servo_x.write(commande_servoX)
    servo_y.write(commande_servoY)