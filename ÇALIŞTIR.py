import pygame
import sys
import random
import os  # For dynamic file paths

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Oyunu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_size = (40, 40)
player_x, player_y = WIDTH // 2, HEIGHT - 90  # Start in the middle of the screen
player_speed = 5
player_jump = -15
player_velocity_y = 0
gravity = 0.8
is_jumping = False
facing_right = True  # Tracks the direction the player is facing

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load player image
player_image_path = os.path.join(current_dir, "character.png")  # Dynamically locate the file
player_image_right = pygame.image.load(player_image_path)  # Load the image
player_image_right = pygame.transform.scale(player_image_right, player_size)  # Scale the image to fit the player size
player_image_left = pygame.transform.flip(player_image_right, True, False)  # Flip the image for left-facing

# Load brick block image
brick_block_path = os.path.join(current_dir, "Brick_Block.jpg")  # Dynamically locate the file
brick_block_image = pygame.image.load(brick_block_path)  # Load the image
brick_block_image = pygame.transform.scale(brick_block_image, (40, 40))  # Scale to block size

# World settings
world_shift = 0  # Tracks how much the world has shifted
block_size = 40  # Size of each block
platforms = [
    pygame.Rect(x * block_size, HEIGHT - block_size, block_size, block_size) for x in range(WIDTH // block_size)
]

# Add some initial floating platforms
floating_platforms = [
    pygame.Rect(200, HEIGHT - 150, 100, 20),
    pygame.Rect(400, HEIGHT - 200, 150, 20),
    pygame.Rect(600, HEIGHT - 250, 120, 20)
]

# Distance tracker
distance_traveled = 0
font = pygame.font.SysFont(None, 36)

def generate_new_blocks():
    """Generate new blocks dynamically as the world shifts."""
    # Generate ground blocks forward
    while len(platforms) < 20:  # Ensure there are always enough ground blocks
        new_block_x = platforms[-1].x + block_size
        new_block_y = HEIGHT - block_size
        platforms.append(pygame.Rect(new_block_x, new_block_y, block_size, block_size))

    # Generate ground blocks backward
    while platforms[0].x + world_shift > 0:  # Ensure blocks exist behind the player
        new_block_x = platforms[0].x - block_size
        new_block_y = HEIGHT - block_size
        platforms.insert(0, pygame.Rect(new_block_x, new_block_y, block_size, block_size))

    # Generate new floating platforms forward
    while len(floating_platforms) < 10:  # Ensure there are always enough floating platforms
        last_platform_x = floating_platforms[-1].x if floating_platforms else WIDTH
        new_platform_x = last_platform_x + random.randint(200, 400)  # Ensure platforms are spaced apart
        new_platform_y = random.randint(HEIGHT - 300, HEIGHT - 150)  # Adjusted height range
        new_platform_width = random.randint(60, 150)
        floating_platforms.append(pygame.Rect(new_platform_x, new_platform_y, new_platform_width, 20))

    # Generate new floating platforms backward
    while floating_platforms and floating_platforms[0].x + world_shift > 0:
        first_platform_x = floating_platforms[0].x
        new_platform_x = first_platform_x - random.randint(200, 400)  # Ensure platforms are spaced apart
        new_platform_y = random.randint(HEIGHT - 300, HEIGHT - 150)
        new_platform_width = random.randint(60, 150)
        floating_platforms.insert(0, pygame.Rect(new_platform_x, new_platform_y, new_platform_width, 20))

# Main game loop
def main():
    global player_x, player_y, player_velocity_y, is_jumping, distance_traveled, world_shift, facing_right

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            world_shift += player_speed  # Shift the world right
            distance_traveled -= player_speed / block_size  # Decrease distance by block size
            facing_right = False  # Face left
        if keys[pygame.K_RIGHT]:
            world_shift -= player_speed  # Shift the world left
            distance_traveled += player_speed / block_size  # Increase distance by block size
            facing_right = True  # Face right
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = player_jump
            is_jumping = True

        # Gravity and jumping
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Collision detection
        player_rect = pygame.Rect(WIDTH // 2, player_y, *player_size)  # Player stays in the middle
        for platform in platforms + floating_platforms:
            shifted_platform = platform.move(world_shift, 0)  # Adjust platform position based on world shift
            if player_rect.colliderect(shifted_platform) and player_velocity_y > 0:
                player_y = shifted_platform.top - player_size[1]
                player_velocity_y = 0
                is_jumping = False

        # Remove blocks that are out of view
        platforms[:] = [block for block in platforms if block.x + world_shift > -block_size]
        floating_platforms[:] = [platform for platform in floating_platforms if platform.x + world_shift > -block_size]

        # Generate new blocks dynamically
        generate_new_blocks()

        # Draw ground blocks
        for platform in platforms:
            shifted_platform = platform.move(world_shift, 0)  # Adjust platform position based on world shift
            screen.blit(brick_block_image, (shifted_platform.x, shifted_platform.y))

        # Draw floating platforms
        for platform in floating_platforms:
            shifted_platform = platform.move(world_shift, 0)  # Adjust platform position based on world shift
            for x in range(shifted_platform.width // block_size):
                screen.blit(brick_block_image, (shifted_platform.x + x * block_size, shifted_platform.y))

        # Draw player (using the PNG image)
        if facing_right:
            screen.blit(player_image_right, (WIDTH // 2, player_y))
        else:
            screen.blit(player_image_left, (WIDTH // 2, player_y))

        # Display distance
        distance_text = font.render(f"Mesafe: {int(distance_traveled)} blok", True, BLACK)
        screen.blit(distance_text, (10, 10))  # Fixed position on the top-left corner

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()