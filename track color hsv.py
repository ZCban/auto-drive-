import cv2
import numpy as np
import mss
import keyboard

# Function to do nothing (used for the trackbar callback)
def nothing(x):
    pass

# Function to capture the screen
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        center_x = (monitor["width"] - 320) // 2
        center_y = (monitor["height"] - 320) // 2
        screenshot = sct.grab({"left": center_x, "top": center_y, "width": 320, "height": 320})
        frame = np.array(screenshot)
        return frame

# Initialize variables
speed = 5

# Create a window to display the result
cv2.namedWindow("Result")

# Create trackbars for color adjustment
cv2.createTrackbar("Hue Lower", "Result", 40, 179, nothing)
cv2.createTrackbar("Saturation Lower", "Result", 40, 255, nothing)
cv2.createTrackbar("Value Lower", "Result", 40, 255, nothing)

cv2.createTrackbar("Hue Upper", "Result", 80, 179, nothing)
cv2.createTrackbar("Saturation Upper", "Result", 255, 255, nothing)
cv2.createTrackbar("Value Upper", "Result", 255, 255, nothing)

while True:
    frame = capture_screen()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbar positions
    h_low = cv2.getTrackbarPos("Hue Lower", "Result")
    s_low = cv2.getTrackbarPos("Saturation Lower", "Result")
    v_low = cv2.getTrackbarPos("Value Lower", "Result")

    h_high = cv2.getTrackbarPos("Hue Upper", "Result")
    s_high = cv2.getTrackbarPos("Saturation Upper", "Result")
    v_high = cv2.getTrackbarPos("Value Upper", "Result")

    # Create lower and upper bounds for the color
    lower_bound = np.array([h_low, s_low, v_low])
    upper_bound = np.array([h_high, s_high, v_high])

    # Create a mask for the specified color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the result
    cv2.imshow("Result", result)

    # Exit on 'q' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
