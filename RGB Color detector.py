import cv2
import numpy as np

# Initialize webcam
vid = cv2.VideoCapture(0)
# Define color ranges in HSV space
color_ranges = {
    'Blue': ([100, 140], [100, 255], [0, 255]),  # HSV range for blue
    'Green': ([40, 80], [40, 255], [0, 255]),    # HSV range for green
    'Red': ([0, 10], [170, 180], [0, 255]),      # HSV range for red
    'Yellow': ([20, 40], [100, 255], [100, 255]), # HSV range for yellow
    'Purple': ([130, 160], [100, 255], [100, 255]), # HSV range for purple
    'Orange': ([10, 20], [100, 255], [100, 255])  # HSV range for orange
}

# Function to get the most prominent color
def detect_prominent_color(hsv_frame):
    max_color = None
    max_count = 0
    
    for color, (hue_range, sat_range, val_range) in color_ranges.items():
        # Create the mask for each color
        lower_bound = np.array([hue_range[0], sat_range[0], val_range[0]])
        upper_bound = np.array([hue_range[1], sat_range[1], val_range[1]])
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        
        # Count the number of pixels in the color range
        color_count = np.sum(mask)
        
        if color_count > max_count:
            max_count = color_count
            max_color = color
    
    # If no color reaches a sufficient count, consider it a mixed color
    if max_count < 5000:  # Adjust the threshold depending on the sensitivity you want
        return "Mixed color"
    
    return max_color

# Running the loop to keep capturing frames
while True:
    # Capture the current frame
    _, frame = vid.read()

    # Convert to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect the most prominent color
    dominant_color = detect_prominent_color(hsv_frame)

    # Display the current frame
    cv2.imshow("Frame", frame)

    # Print the dominant color
    if dominant_color:
        print(f"Dominant color: {dominant_color}")
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
vid.release()
cv2.destroyAllWindows()
