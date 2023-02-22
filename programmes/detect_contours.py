from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def detect_center(camera):
    
    sum_cx = 0
    sum_cy = 0

    rawCapture = PiRGBArray(camera, size=(640, 480))
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range of white colors in HSV
    lower_white = (0, 0, 220)
    upper_white = (100, 30, 255)

    # Create a mask that only allows black colors to pass through
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to the frame
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Detect contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours that are too small
    contours = [c for c in contours if cv2.contourArea(c) > 500]

    # Loop over the contours
    for contour in contours:
        
        # Get the moments of the contour
        moments = cv2.moments(contour)

        # Calculate the coordinates of the center of the contour
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        
        # Print the coordinates of the center of the contour
        print(f"cx={cx}, cy={cy}")
        
        sum_cx = sum_cx + cx
        sum_cy = sum_cy + cy
    
    moy_cx = int(sum_cx / 4)
    moy_cy = int(sum_cy / 4)
    
    print(f"moy_cx={moy_cx}, moy_cy={moy_cy}")
    
    return(moy_cx,moy_cy)
    
