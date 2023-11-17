import cv2
import numpy as np
import mss
import keyboard

def capture_screen():
    screenshot = 320
    height_center_correction = +100
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        center_x = (monitor["width"] - screenshot) // 2
        center_y = (monitor["height"] - screenshot) // 2 - height_center_correction
        screenshot = sct.grab({"left": center_x, "top": center_y, "width": screenshot, "height": screenshot})
        frame = np.array(screenshot)
        return frame

# White color thresholds
white_lower = np.array([0, 0, 180])
white_upper = np.array([255, 30, 255])

# Initialize variables
speed = 5

while True:
    frame = capture_screen()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for white color
    mask = cv2.inRange(hsv, white_lower, white_upper)

    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=3)

    # Find contours in the white mask
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the contour with the maximum area (assuming lanes are large)
        max_area_contour = max(contours, key=lambda c: cv2.contourArea(c))

        # Draw the lane contour
        cv2.drawContours(frame, [max_area_contour], -1, (0, 255, 0), 2)

        # Get the bounding box of the lane
        x, y, w, h = cv2.boundingRect(max_area_contour)

        # Find the center of the lane
        center_x = x + w // 2

        # Adjust the movement based on the center_x position
        if center_x < frame.shape[1] // 2:
            print("Move left")
            # Add code to move the object left (adjust as needed)
        else:
            print("Move right")
            # Add code to move the object right (adjust as needed)

    # Show the frame
    cv2.imshow("Frame", frame)

    # Exit on 'q' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
