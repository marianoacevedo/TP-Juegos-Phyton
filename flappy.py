import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 576, 900
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")
clock = pygame.time.Clock()

# Fonts
#game_font = pygame.font.Font(None, 36)
font = pygame.font.Font(None, 36)

# Carga la imagen de fondo del menu 
background_image = pygame.image.load('assets/background-day.png').convert()
background_image = pygame.transform.scale2x(background_image)
#background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Function draw menu
def draw_menu():
    screen.blit(background_image, (WIDTH, HEIGHT))


# Function to create buttons
def create_button(x, y, width, height, image_path, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        screen.blit(pygame.transform.scale(button_image, (width + 10, height + 10)), (x - 5, y - 5))
        
        if click[0] == 1 and action is not None:
            action(parameter)
    else:
        screen.blit(button_image, (x, y))
       

# Function to start the game loop
def start_game(difficulty):
    print(f"Game is starting with difficulty: {difficulty}")
    # Set the game state to "running"
    game_loop(difficulty)

# Main game loop
def game_loop(difficulty):

    def draw_floor():
        screen.blit(floor_surface, (floor_x_pos, 900))
        screen.blit(floor_surface, (floor_x_pos + 576, 900))


    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
        return bottom_pipe, top_pipe


    def move_pipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
        return visible_pipes


    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)


    def check_collision(pipes):
        global can_score
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                death_sound.play()
                can_score = True
                return False

        if bird_rect.top <= -100 or bird_rect.bottom >= 900:
            can_score = True
            return False

        return True


    def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
        return new_bird


    def bird_animation():
        new_bird = bird_frames[bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
        return new_bird, new_bird_rect


    def score_display(game_state):
        if game_state == 'main_game':
            score_surface = font.render(
                str(int(score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = font.render(
                f'Score: {int(score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            screen.blit(score_surface, score_rect)

            high_score_surface = font.render(
                f'High score: {int(high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            screen.blit(high_score_surface, high_score_rect)


    def update_score(score, high_score):
        if score > high_score:
            high_score = score
        return high_score


    def pipe_score_check():
        global score, can_score

        if pipe_list:
            for pipe in pipe_list:
                if 95 < pipe.centerx < 105 and can_score:
                    score += 1
                    score_sound.play()
                    can_score = False
                if pipe.centerx < 0:
                    can_score = True


    def quit_game(): # Funcion que sirve para salir del juego.
        pygame.quit()
        sys.exit()

    global score, can_score
    
    gravity = 0.25
    bird_movement = 0
    game_active = False
    score = 0
    high_score = 0
    can_score = True
    bg_surface = pygame.image.load('assets/background-night.png').convert()
    bg_surface = pygame.transform.scale2x(bg_surface)

    floor_surface = pygame.image.load('assets/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_pos = 0

    bird_downflap = pygame.transform.scale2x(pygame.image.load(
        'assets/abajo.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load(
        'assets/medio.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load(
        'assets/arriba.png').convert_alpha())
    bird_frames = [bird_downflap, bird_midflap, bird_upflap]
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center=(100, 512))

    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, 200)

    if difficulty == 'Easy':
        pipe_surface = pygame.image.load('assets/pipe-green.png')
        pipe_surface = pygame.transform.scale2x(pipe_surface)
        pipe_list = []
        SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWNPIPE, 2000)
        pipe_height = [400, 600, 800]
    elif difficulty == 'Medium':
        pipe_surface = pygame.image.load('assets/pipe-red.png')
        pipe_surface = pygame.transform.scale2x(pipe_surface)
        pipe_list = []
        SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWNPIPE, 1200)
        pipe_height = [400, 600, 800]
    elif difficulty == 'Hard':
        pipe_surface = pygame.image.load('assets/edificio.png')
        pipe_surface = pygame.transform.scale2x(pipe_surface)
        pipe_list = []
        SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(SPAWNPIPE, 900)
        pipe_height = [400, 600, 800]

    game_over_surface = pygame.transform.scale2x(
        pygame.image.load('assets/message.png').convert_alpha())
    game_over_rect = game_over_surface.get_rect(center=(288, 512))

    # Creo el botón de "Salir"
    exit_button = pygame.Rect(10, 70, 100, 50)  # Posición y tamaño del botón
    exit_font = pygame.font.Font(None, 36) # Tipo y tamaño de letra
    exit_text = exit_font.render('Salir', True, (255, 255, 255)) # renderizo el texto en color blanco

    flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
    death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
    score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
    score_sound_countdown = 100
    SCOREEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SCOREEVENT, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Manejar clics de ratón
                if event.button == 1:  # Verifico si el clic es el botón izquierdo
                    mouse_pos = event.pos  # Posición del clic
                    if exit_button.collidepoint(mouse_pos):  # Verifico si se hizo clic en el texto
                        
                        quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 8
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 512)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation()
        
        screen.blit(bg_surface, (0, 0))

        if game_active:
            # Bird
            bird_movement += 0.25
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
        
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)

            # Pipes
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            # Score
            pipe_score_check()
            score_display('main_game')
        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')
            screen.blit(exit_text, (10, 70))  # Dibuja el texto de "Salir".
        

        # Floor
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)

# Initial game state
game_state = "menu"
selected_difficulty = None

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Check the game state
    if game_state == "menu":
       
        screen.blit(background_image, (0, 0))

        #dibuja el menu
        draw_menu()
        # Draw buttons
        create_button(188, 150, 200, 50, "menu/easy.png", start_game, "Easy")
        create_button(188, 250, 200, 50, "menu/medium.png", start_game, "Medium")
        create_button(188, 350, 200, 50, "menu/hard.png", start_game, "Hard")

        # Update the display
        pygame.display.flip()

    elif game_state == "running":
        # If in the running state, call the game loop function
        game_loop(selected_difficulty)
        # Set the game state back to menu when the game loop exits
        game_state = "menu"
    
    # Cap the frame rate
    clock.tick(FPS)