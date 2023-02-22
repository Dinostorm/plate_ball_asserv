from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

def func_detect_ball(center_x,center_y,camera):
    
    cx = center_x
    cy = center_y
    rawCapture = PiRGBArray(camera, size=(640, 480))
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range of yellow colors in HSV
    lower_yellow = (15, 80, 80)
    upper_yellow = (40, 255, 255)

    # Create a mask that only allows black colors to pass through
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply the mask to the frame
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Detect contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours that are too small
    contours = [c for c in contours if cv2.contourArea(c) > 200]

    # Loop over the contours
    for contour in contours:
        # Get the moments of the contour
        moments = cv2.moments(contour)

        # Calculate the coordinates of the center of the contour
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        # Draw the center of the contour on the original frame
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Print the coordinates of the center of the contour
    print(f"cx = {cx}, cy = {cy}")

    return (cx,cy)