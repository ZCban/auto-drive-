import cv2
import numpy as np
import mss
import keyboard

mid = 320 / 2


screenshot = 160
screenshotx = 160
height_center_correction = +30
adjust_large_screenshot = -128
with mss.mss() as sct:
    monitor = sct.monitors[0]
    center_x = (monitor["width"] - screenshotx) // 2
    center_y = (monitor["height"] - screenshot) // 2 

# Green color thresholds
green_lower = np.array([57, 28, 150])
green_upper = np.array([70, 255, 255])

# Red color thresholds
red_lower = np.array([0, 100, 100])
red_upper = np.array([10, 255, 255])

# Orange/Yellow color thresholds
orange_lower = np.array([20, 100, 100])
orange_upper = np.array([30, 255, 255])

# Initialize variables
speed = 5

while True:
    frame = np.array(sct.grab({"left": center_x, "top": center_y, "width": screenshotx, "height": screenshot}))

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for green color
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    orange_mask = cv2.inRange(hsv, orange_lower, orange_upper)

    kernel = np.ones((3,3), np.uint8)
    green_dilated = cv2.dilate(green_mask, kernel, iterations=5)
    red_dilated = cv2.dilate(red_mask, kernel, iterations=5)
    orange_dilated = cv2.dilate(orange_mask, kernel, iterations=5)

    # Find contours in the green mask
    green_contours, _ = cv2.findContours(green_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    orange_contours, _ = cv2.findContours(orange_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if green_contours:
        # Find the contour with the minimum distance from the center
        green_centers = np.array([cv2.minEnclosingCircle(c)[0] for c in green_contours])
        green_distances = np.linalg.norm(green_centers - mid, axis=-1)
        closest_green_contour_idx = np.argmin(green_distances)

        # Get the bounding box of the green contour
        x, y, w, h = cv2.boundingRect(green_contours[closest_green_contour_idx])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Find the center of the bounding box
        center_linex = x + w // 2

        # Draw a line at the center of the bounding box
        cv2.line(frame, (center_linex, 0), (center_linex, frame.shape[0]), (0, 255, 0), 2)

        # Adjust the movement based on the center_x position
        if center_linex < frame.shape[1] // 2:
            print("Move left")
            # Add code to move the object left (adjust as needed)
        else:
            print("Move right")
            # Add code to move the object right (adjust as needed)

    elif red_contours:
        # Find the contour with the minimum distance from the center
        red_centers = np.array([cv2.minEnclosingCircle(c)[0] for c in red_contours])
        red_distances = np.linalg.norm(red_centers - mid, axis=-1)
        closest_red_contour_idx = np.argmin(red_distances)

        # Get the bounding box of the red contour
        x, y, w, h = cv2.boundingRect(red_contours[closest_red_contour_idx])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Find the center of the bounding box
        #center_x = x + w // 2
        

        # Adjust the movement based on the center_x position
        if center_x < frame.shape[1] // 2:
            print("hold Brake + left")
            # Add code to move the object left (adjust as needed)
        else:
            print("hold Brake + right")
            # Add code to move the object right (adjust as needed)


    elif orange_contours:
        # Find the contour with the minimum distance from the center
        orange_centers = np.array([cv2.minEnclosingCircle(c)[0] for c in orange_contours])
        orange_distances = np.linalg.norm(orange_centers - mid, axis=-1)
        closest_orange_contour_idx = np.argmin(orange_distances)

        # Get the bounding box of the orange contour
        x, y, w, h = cv2.boundingRect(orange_contours[closest_orange_contour_idx])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)  # Orange color

        # Find the center of the bounding box
        #center_x = x + w // 2
        

        # Adjust the movement based on the center_x position
        if center_x < frame.shape[1] // 2:
            print("release accelerator + left")
            # Add code to move the object left (adjust as needed)
        else:
            print("release accelerator + right")
            # Add code to move the object right (adjust as needed)

    # Show the frame
    cv2.imshow("Frame", frame)

    # Exit on 'q' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
