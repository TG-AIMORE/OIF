import pygame, numba, random, colorsys, math, socket, sys, json
import numpy as np

#Global Variables
pause = False
horizontal_res, vertical_res = 640, 360  #Default resolution
screen_width, screen_height = 1280, 720  #Default screen size
start_screen = True
lan = False
hosting = False

# Color blob settings
num_blobs = 100  # Number of color blobs
blob_radius = random.randint(25, 75)  # Radius of each blob
blob_speed = random.uniform(0.25, 0.45)  # Movement speed of each blob
color_change_speed = random.uniform(0.0005, 0.001)  # Speed of color transition
reset = False


#LAN INIT
try:
    # Method 1: Use a connection to obtain the local IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # External IP (no actual connection is made)
        HOST_IP = s.getsockname()[0]
except Exception:
    # Method 2: Fallback to localhost
    HOST_IP = "127.0.0.1"

print("HOST_IP:", HOST_IP) # Automatically fetches the local IP
PORT = 5555  # Default port for connection
join_code = None  # Code generated by host for the client to enter

# Create blob data (position, color)
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


#The main function starts everything in the program.
def main():
    global pause, horizontal_res, vertical_res, screen_width, screen_height, start_screen, conn, addr, client_socket



    pygame.init()  #Start the pygame library, which helps create games.
    screen = pygame.display.set_mode((screen_width, screen_height))  #Make a screen that’s 1280x720 pixels.
    running = True
    clock = pygame.time.Clock()  #Keeps track of time so we can control the game’s speed.

    #Camera Settings
    fov_value = 60  #Field of View: how much of the scene the player can see at once.
    fov = horizontal_res / fov_value  #This helps to calculate distances correctly.

    #Player Position and Rotation (direction player is facing)
    pos_x, pos_y, rotation = 5, 5, 180  #Player starts near the center of the map.

    #Frame buffer to hold the image before showing it on the screen
    current_frame = np.zeros((horizontal_res, vertical_res * 2, 3))

    #Load the lamp texture
    lamp_texture = pygame.image.load('lamp.jpg')
    lamp_texture = pygame.surfarray.array3d(pygame.transform.scale(lamp_texture, (horizontal_res * 2, vertical_res * 4))) / 255

    #Load the textures (pictures) for the sky, floor, and walls
    sky = pygame.image.load('skybox2.jpg')
    sky = pygame.surfarray.array3d(pygame.transform.scale(sky, (horizontal_res * 4, vertical_res * 2))) / 255

    floor = pygame.surfarray.array3d(pygame.image.load('floor.jpg')) / 255

    wall_texture = pygame.image.load('wall.jpg')
    wall_texture = pygame.surfarray.array3d(pygame.transform.scale(wall_texture, (horizontal_res * 2, vertical_res * 4))) / 255

    #Define a simple map where 1 is a wall, and 0 is open space
    map_data = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

    #Initialize a light map with the same dimensions as map_data
    light_map = np.zeros_like(map_data, dtype=float)

    add_light_source(light_map, 4, 3, intensity=0.8)
    add_light_source(light_map, 7, 5, intensity=0.8)
    #MEISH
    #Main loop keeps the game running
    while running:
        #Handle events like closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = not pause  #Toggle pause when P is pressed

        #If the game is paused, show the pause menu
        if pause:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            pause_menu(screen)
            continue  #Skip the rest of the game logic when paused

        #Show the start screen if it's the start of the game
        if start_screen:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            start_screen_logic(screen)
            continue

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        #Render frame (create the 3D image from the map and textures)
        frame = render_frame(pos_x, pos_y, rotation, current_frame, sky, floor, wall_texture, lamp_texture,
                             horizontal_res, vertical_res, fov, fov_value, map_data, light_map)

        #Convert the frame into an image for pygame and display it on the screen
        surf = pygame.surfarray.make_surface(frame * 255)
        surf = pygame.transform.scale(surf, (screen_width, screen_height))
        screen.blit(surf, (0, 0))
        pygame.display.update()

        #Update player position and rotation based on keys pressed
        pos_x, pos_y, rotation = movement(pos_x, pos_y, rotation, clock.tick() / 500, map_data)

        #Display the Frames Per Second (FPS) in the window title
        fps = int(clock.get_fps())
        pygame.display.set_caption("Raycasting Test - FPS: " + str(fps))

        game_state = {
            "players": [
                {"x": 100, "y": 200, "rotation": 0, "damage": 10, "health": 100},
                {"x": 150, "y": 250, "rotation": 90, "damage": 15, "health": 120}
            ]
            }   
        if lan:
            try:
                if hosting:
                    # Send game state
                    conn.sendall(json.dumps(game_state).encode())
        
                    # Receive updated state from the client
                    received_data = receive_data_host(conn)
                    if received_data:
                        print(f"Updated state from client: {received_data}")
                else:
                    # Send game state
                    client_socket.send(json.dumps(game_state).encode())
        
                    # Receive updated state from the host
                    received_data = receive_data_client(client_socket)
                    if received_data:
                        print(f"Updated state from host: {received_data}")
            except Exception as e:
                print(f"Error during LAN communication: {e}")
                lan = False  # Exit LAN mode on error


    pygame.quit()

def add_light_source(light_map, x, y, intensity, decay=0.1):
    """Add a light source and propagate its brightness."""
    max_radius = int(intensity / decay)
    for i in range(-max_radius, max_radius + 1):
        for j in range(-max_radius, max_radius + 1):
            #Calculate distance from light source
            dist = np.sqrt(i**2 + j**2)
            if dist <= max_radius:
                brightness = max(0, intensity - decay * dist)
                light_x, light_y = x + i, y + j
                if 0 <= light_x < light_map.shape[0] and 0 <= light_y < light_map.shape[1]:
                    light_map[light_x][light_y] = max(light_map[light_x][light_y], brightness)

def receive_data_host(conn):
    try:
        conn.settimeout(0.1)  # Avoid blocking indefinitely
        data = conn.recv(1024).decode()  # Adjust buffer size as needed
        if data:
            print(f"Received from client: {data}")
            return json.loads(data)  # Parse JSON data
    except socket.timeout:
        return None  # No data received
    except Exception as e:
        print(f"Error receiving data from client: {e}")
        return None

def receive_data_client(client_socket):
    try:
        client_socket.settimeout(0.1)  # Avoid blocking indefinitely
        data = client_socket.recv(1024).decode()  # Adjust buffer size as needed
        if data:
            print(f"Received from host: {data}")
            return json.loads(data)  # Parse JSON data
    except socket.timeout:
        return None  # No data received
    except Exception as e:
        print(f"Error receiving data from host: {e}")
        return None

def host():
    global HOST_IP, PORT, join_code, conn, addr, hosting, lan
    join_code = str(random.randint(1000, 9999))  # Random 4-digit code for joining
    print(f"Hosting on {HOST_IP}:{PORT} with join code: {join_code}")

    # Start a socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, PORT))

    server_socket.listen(1)
    print("Waiting for client to join...")

    try:
        # Accept client connection
        conn, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        
        client_code = conn.recv(1024).decode()
        print(client_code)

        if client_code == join_code:
            print("Join code was correct!")
            lan, hosting = True
        else:
            print("Join code was incorrect")
    except Exception as e:
        print(f"Error while hosting: {e}")

def join(screen):
    global horizontal_res, vertical_res, num_blobs, blob_radius, blob_speed, color_change_speed, reset, lan, client_socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    input_box = pygame.Rect(screen_width // 2 - 75, screen_height // 4 + 60, 150, 25)
    input_box2 = pygame.Rect(screen_width // 2 - 75, screen_height // 4 + 180, 150, 25)
    color = (255, 255, 255)
    color2 = (255, 255, 255)
    active = False
    active2 = False
    host_ip = ''
    code_input = ''
    host_ip = ''

    contin = False

    while contin == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                    color = (52, 177, 235)
                else:
                    active = False
                    color = (255, 255, 255)
                if input_box2.collidepoint(event.pos):
                    active2 = True
                    color2 = (52, 177, 235)
                else:
                    active2 = False
                    color2 = (255, 255, 255)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(f"Entered: {host_ip}")
                        contin = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        host_ip = host_ip[:-1]
                    else:
                        host_ip += event.unicode
                elif active2:
                    if event.key == pygame.K_RETURN:
                        print(f"Entered: {code_input}")
                        contin = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        code_input = code_input[:-1]
                    else:
                        code_input += event.unicode

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


        font = pygame.font.SysFont('Arial', 40)

        title_text = font.render("Join Game", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - 30))

        font = pygame.font.SysFont('Arial', 25)

        title_text = font.render("Enter host's ip:", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 + 20))

        back = pygame.Rect(screen_width // 2 - 75, screen_height // 4 + 60, 150, 25)
        pygame.draw.rect(screen, (255, 255, 255), back)

        font = pygame.font.Font(None, 20)

        txt_surface = font.render(host_ip, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        pygame.draw.rect(screen, color, input_box, 2)

        font = pygame.font.SysFont('Arial', 25)

        title_text = font.render("Enter game code:", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 + 140))

        back2 = pygame.Rect(screen_width // 2 - 75, screen_height // 4 + 180, 150, 25)
        pygame.draw.rect(screen, (255, 255, 255), back2)

        font = pygame.font.Font(None, 20)

        txt_surface = font.render(code_input, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box2.x+5, input_box2.y+5))

        pygame.draw.rect(screen, color2, input_box2, 2)

        pygame.display.flip()

    try:
        print(host_ip)
        client_socket.connect((host_ip, PORT))
        print("Connected to the host!")

        client_socket.send(str(code_input).encode())
        lan = True
        return
    except socket.error as e:
        print(f"Failed to connect: {e}")

def movement(posx, posy, rot, et, map_data):
    pressed_keys = pygame.key.get_pressed()
    x, y = posx, posy
    p_mouse = pygame.mouse.get_rel()  #Get mouse movement to change view
    rotation = rot + np.clip(p_mouse[0] / 200, -0.2, .2)  #Limit rotation speed

    #Add a small padding to prevent moving too close to walls
    padding = 0.1  

    #Move forward (W key)
    if pressed_keys[pygame.K_w]:
        new_x, new_y = x + et * np.cos(rotation), y + et * np.sin(rotation)
        if not is_collision(new_x, new_y, map_data, padding):
            x, y = new_x, new_y

    #Move backward (S key)
    if pressed_keys[pygame.K_s]:
        new_x, new_y = x - et * np.cos(rotation), y - et * np.sin(rotation)
        if not is_collision(new_x, new_y, map_data, padding):
            x, y = new_x, new_y

    #Strafe left (A key)
    if pressed_keys[pygame.K_a]:
        new_x, new_y = x + et * np.sin(rotation), y - et * np.cos(rotation)
        if not is_collision(new_x, new_y, map_data, padding):
            x, y = new_x, new_y

    #Strafe right (D key)
    if pressed_keys[pygame.K_d]:
        new_x, new_y = x - et * np.sin(rotation), y + et * np.cos(rotation)
        if not is_collision(new_x, new_y, map_data, padding):
            x, y = new_x, new_y

    return x, y, rotation

def is_collision(x, y, map_data, padding):
    if map_data[int(x - padding)][int(y)] == 1 or \
       map_data[int(x + padding)][int(y)] == 1 or \
       map_data[int(x)][int(y - padding)] == 1 or \
       map_data[int(x)][int(y + padding)] == 1:
        return True
    return False

def pause_menu(screen):
    global horizontal_res, vertical_res  #Ensure these variables are global
    
    font = pygame.font.SysFont('Arial', 30)

    #Draw pause menu background
    menu_rect = pygame.Rect(320, 180, 640, 360)
    pygame.draw.rect(screen, (0, 0, 0, 150), menu_rect)
    
    #Draw text
    text_surface = font.render("Pause Menu", True, (255, 255, 255))
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 4 + 30))

    #Quit Button
    quit_button = pygame.Rect(540, 230, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    #Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.collidepoint(event.pos):
                pygame.quit()
                quit()
    
    pygame.display.update()

def apply_blur(surface, scale_factor=0.3):
    small_surface = pygame.transform.smoothscale(surface, 
                    (int(screen_width * scale_factor), int(screen_height * scale_factor)))
    return pygame.transform.smoothscale(small_surface, (screen_width, screen_height))

def start_screen_logic(screen):
    global start_screen, horizontal_res, vertical_res, num_blobs, blob_radius, blob_speed, color_change_speed, reset

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
                join(screen)
            if host_button.collidepoint(event.pos):
                host()

    pygame.display.update()


@numba.njit(parallel=True)
def render_frame(pos_x, pos_y, rotation, frame, sky_texture, floor_texture, wall_texture, lamp_texture,
                 horizontal_res, vertical_res, fov, fov_value, map_data, light_map):
    halfvres = vertical_res
    for i in numba.prange(horizontal_res):
        rot_i = rotation + np.deg2rad(i / (horizontal_res / fov_value) - fov_value / 2)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / (horizontal_res / fov_value) - fov_value / 2))
        
        #Render sky
        sky_x = int((np.rad2deg(rot_i) % 360) / 360 * sky_texture.shape[0])

        frame[i][:] = sky_texture[sky_x][:]

        x, y = pos_x, pos_y
        while map_data[int(x) % map_data.shape[0]][int(y) % map_data.shape[1]] == 0:
            x, y = x + 0.01 * cos, y + 0.01 * sin

        n = abs((x - pos_x) / cos)
        wall_height = int(halfvres / (n * cos2 + 0.001))

        texture_x = int((x % 1) * wall_texture.shape[0])
        if x % 1 < 0.02 or x % 1 > 0.98:
            texture_x = int((y % 1) * wall_texture.shape[0])

        #Check if the wall is a light source
        brightness = light_map[int(x) % map_data.shape[0]][int(y) % map_data.shape[1]]
        is_light_source = brightness > 0.7  #Adjust threshold as needed

        #Select texture based on light source presence
        current_texture = lamp_texture if is_light_source else wall_texture

        #Render wall or lamp with chosen texture
        for k in range(-wall_height, wall_height):
            pixel_y = halfvres + k
            if 0 <= pixel_y < 2 * halfvres:
                texture_y = int((k + wall_height) / (2 * wall_height) * current_texture.shape[1])
                if 0 <= texture_y < current_texture.shape[1]:  #Ensure texture_y is within bounds
                    frame[i][pixel_y] = brightness * current_texture[texture_x % current_texture.shape[0]][texture_y]

        #Floor rendering with light effect
        for j in range(halfvres - wall_height):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = pos_x + cos * n, pos_y + sin * n
            floor_x = int(x / 2 % 1 * floor_texture.shape[0])
            floor_y = int(y / 2 % 1 * floor_texture.shape[1])

            brightness = light_map[int(x) % map_data.shape[0]][int(y) % map_data.shape[1]]
            shade = 0.2 + 0.8 * brightness
            frame[i][2 * halfvres - j - 1] = shade * floor_texture[floor_x][floor_y]

    return frame



main()  #Start the game
