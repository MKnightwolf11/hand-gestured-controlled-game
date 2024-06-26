import pygame
from hand_detection import ObjectTracker

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hand-Controlled Game')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize object tracker
tracker = ObjectTracker()

# Game variables
character_x, character_y = screen_width // 2, screen_height // 2
character_speed = 5

# Main game loop
running = True
while running:
    # Get object position from tracker
    object_position = tracker.track_object()

    # Process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state based on object position
    if object_position:
        object_x, object_y = object_position
        # Adjust character position based on object movement
        character_x += (object_x - screen_width // 2) // 10
        character_y += (object_y - screen_height // 2) // 10
    
    # Keep character within screen bounds
    character_x = max(0, min(screen_width - 50, character_x))
    character_y = max(0, min(screen_height - 50, character_y))

    # Update Pygame display
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (character_x, character_y, 50, 50))
    pygame.display.flip()

# Release resources
tracker.release()
pygame.quit()