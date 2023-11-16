import cv2
import numpy as np
import mss
import keyboard

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        center_x = (monitor["width"] - 320) // 2
        center_y = (monitor["height"] - 320) // 2
        screenshot = sct.grab({"left": center_x, "top": center_y, "width": 320, "height": 320})
        frame = np.array(screenshot)
        return frame

# Green color thresholds
#green_lower = np.array([57, 28, 178])
#green_upper = np.array([75, 255, 255])

green_lower = np.array([57, 28, 178])
green_upper = np.array([75, 255, 255])


# Initialize variables
speed = 5

while True:
    frame = capture_screen()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for green color
    mask = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours in the green mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the contour with the maximum height
        max_height_contour = max(contours, key=lambda c: cv2.boundingRect(c)[3])

        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(max_height_contour)

        # Find the center of the bounding box
        center_x = x + w // 2

        # Draw a line at the center of the bounding box
        cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0, 255, 0), 2)

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
