import pygame, numba, random, colorsys, math, socket, sys, json, threading, math, time
import numpy as np

screen_width, screen_height = 1280, 720

# Color blob settings
num_blobs = 100  # Number of color blobs
blob_radius = random.randint(25, 75)  # Radius of each blob
blob_speed = random.uniform(0.25, 0.45)  # Movement speed of each blob
color_change_speed = random.uniform(0.0005, 0.001)  # Speed of color transition
reset = False

blobs = []
for _ in range(num_blobs):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    hue = random.random()  # Initial random color
    blobs.append({'pos': [x, y], 'hue': hue, 'direction': [random.uniform(-1, 1), random.uniform(-1, 1)]})

#Convert HSV to RGB for smooth color transitions
def hsv_to_rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

#Draw blobs with varying colors that blend together
def draw_blurred_blobs(screen, blobs, blob_radius):
    for blob in blobs:
        # Update color and position of each blob
        blob['hue'] = (blob['hue'] + color_change_speed) % 1  # Update hue for color change
        color = hsv_to_rgb(blob['hue'], 0.8, 1)  # Convert to RGB with high saturation for vivid colors

        # Draw a partially transparent circle for each blob
        surface = pygame.Surface((blob_radius * 2, blob_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color + (100,), (blob_radius, blob_radius), blob_radius)
        screen.blit(surface, (blob['pos'][0] - blob_radius, blob['pos'][1] - blob_radius))

        # Update position with drifting motion
        blob['pos'][0] += blob['direction'][0] * blob_speed
        blob['pos'][1] += blob['direction'][1] * blob_speed

        # Bounce blobs off screen edges
        if blob['pos'][0] <= 0 or blob['pos'][0] >= screen_width:
            blob['direction'][0] *= -1
        if blob['pos'][1] <= 0 or blob['pos'][1] >= screen_height:
            blob['direction'][1] *= -1

def apply_blur(surface, scale_factor=0.3):
    small_surface = pygame.transform.smoothscale(surface, 
                    (int(screen_width * scale_factor), int(screen_height * scale_factor)))
    return pygame.transform.smoothscale(small_surface, (screen_width, screen_height))

def death_screen(screen, screen_width, screen_height):
    font = pygame.font.SysFont('Arial', 30)

    #Draw pause menu background
    menu_rect = pygame.Rect(320, 180, 640, 360)
    pygame.draw.rect(screen, (0, 0, 0, 150), menu_rect)
    
    #Draw text
    text_surface = font.render("Mission Failed", True, (255, 255, 255))
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 4 + 30))

    time.sleep(3)

    quit()
    
    pygame.display.update()

def start_screen_logic(screen, screen_width, screen_height):
    global start_screen, num_blobs, blob_radius, blob_speed, color_change_speed, reset

    if blob_radius <= 45 and reset == False:
        blob_radius += 0.075
        if blob_radius >= 45:
            reset = True
    elif blob_radius >= 25:
        blob_radius -= 0.075
    else:
        reset = False

    screen.fill((0, 0, 0))

    # Draw the color-changing blobs onto a temporary surface
    temp_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    draw_blurred_blobs(temp_surface, blobs, blob_radius)

    # Apply the blur effect to the temporary surface
    blurred_surface = apply_blur(temp_surface)

    # Draw the blurred surface onto the main screen
    screen.blit(blurred_surface, (0, 0))

    font = pygame.font.SysFont('Arial', 30)

    #Display Start Screen Title
    title_text = font.render("OIF", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - 30))

    #Start Game Button
    start_button = pygame.Rect(440, 280, 400, 50)
    pygame.draw.rect(screen, (42, 212, 65), start_button, 0, 4)
    start_text = font.render("Freeplay", True, (255, 255, 255))
    screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))

    #Host Game Button
    host_button = pygame.Rect(440, 360, 400, 50)
    pygame.draw.rect(screen, (52, 177, 235), host_button, 0, 4)
    host_text = font.render("Host", True, (255, 255, 255))
    screen.blit(host_text, (host_button.centerx - host_text.get_width() // 2, host_button.centery - host_text.get_height() // 2))

    #Join Game Button
    join_button = pygame.Rect(440, 440, 400, 50)
    pygame.draw.rect(screen, (37, 125, 184), join_button, 0, 4)
    join_text = font.render("Join", True, (255, 255, 255))
    screen.blit(join_text, (join_button.centerx - join_text.get_width() // 2, join_button.centery - join_text.get_height() // 2))

    #Quit Game Button
    quit_button = pygame.Rect(440, 520, 400, 50)
    pygame.draw.rect(screen, (212, 42, 42), quit_button, 0, 4)
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    #Handle user input on the start screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                start_screen = False  #Start the game
            if quit_button.collidepoint(event.pos):
                pygame.quit()
                quit()
            if join_button.collidepoint(event.pos):
                start_screen = False
                return True
                #join(screen)
                
            if host_button.collidepoint(event.pos):
                start_screen = False
                return False
                #host()
                

    pygame.display.update()
