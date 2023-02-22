import cv2

def func_detect_ball():
    # Create a VideoCapture object to read from the webcam
    cap = cv2.VideoCapture(0)

    # Read a frame from the webcam
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a range of black colors in HSV
    lower_black = (0, 0, 0)
    upper_black = (180, 255, 30)

    # Create a mask that only allows black colors to pass through
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Apply the mask to the frame
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Detect contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours that are too small
    contours = [c for c in contours if cv2.contourArea(c) > 1000]

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
        print(f"cx={cx}, cy={cy}")

    # Show the original frame and the resulting frame
    #cv2.imshow("Original", frame)
    #cv2.imshow("Result", res)

    # # Check if the user pressed the "q" key
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     break

    # Release the VideoCapture object
    cap.release()

    return (cx,cy)