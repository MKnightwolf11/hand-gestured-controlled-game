import cv2
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hand-Controlled Game')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_hand.xml')

# Game variables
rect_x, rect_y = screen_width // 2, screen_height // 2
rect_speed = 5

# Main game loop
running = True
while running:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale for hand detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect hands using Haar Cascade
    hands = hand_cascade.detectMultiScale(gray, 1.1, 5)
    
    # Draw rectangle around detected hands
    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Center of the hand
        hand_center_x = x + w // 2
        hand_center_y = y + h // 2
        
        # Map hand position to game screen
        rect_x = int(hand_center_x * (screen_width / cap.get(3)))
        rect_y = int(hand_center_y * (screen_height / cap.get(4)))
    
    # Display the captured frame
    cv2.imshow('Hand Tracking', frame)
    
    # Update Pygame display
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (rect_x - 25, rect_y - 25, 50, 50))
    pygame.display.flip()
    
    # Check for user input or events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Exit the game loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close Pygame
cap.release()
cv2.destroyAllWindows()
pygame.quit()