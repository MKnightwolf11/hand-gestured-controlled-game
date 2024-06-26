import cv2
import numpy as np

class ObjectTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.lower_color = np.array([0, 100, 100])  # Adjust based on your object's color
        self.upper_color = np.array([10, 255, 255])  # Adjust based on your object's color

    def track_object(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only your object color
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Get the largest contour (assuming it's your object)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calculate the centroid of the largest contour
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return cx, cy
        
        return None

    def release(self):
        self.cap.release()

if __name__ == "__main__":
    tracker = ObjectTracker()

    while True:
        object_position = tracker.track_object()
        if object_position:
            print("Detected object position:", object_position)

            # Optionally, draw a circle or marker on the object's position in the frame for visual feedback
            frame = cv2.circle(frame, object_position, 10, (0, 255, 0), -1)

        # Display the frame with object position
        cv2.imshow('Object Tracking', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tracker.release()
    cv2.destroyAllWindows()