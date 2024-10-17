import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH , HEIGHT  = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WIDTH_SPACESHIP , HEIGHT_SPACESHIP = 150,80
NAIVY = (0,0,80)
VEL = 10
BULLET_VEL = 15
MAX_BULLET = 3

ORANGE_HIT = pygame.USEREVENT + 1
PURPLE_HIT = pygame.USEREVENT + 2

#images
BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/background.jpg"), (WIDTH, HEIGHT))
pygame.display.set_caption("WAR")

PURPLE_SPACESHIP = pygame.transform.scale(pygame.image.load("Assets/spaceship_purple.png").convert_alpha(), (WIDTH_SPACESHIP, HEIGHT_SPACESHIP))
ORANGE_SPACESHIP = pygame.transform.scale(pygame.image.load("Assets/spaceship_orange.png").convert_alpha(), (WIDTH_SPACESHIP, HEIGHT_SPACESHIP))

PURPLE_BEAM_IMAGE = pygame.image.load("Assets/beam_purple.png").convert_alpha()
PURPLE_BEAM = pygame.transform.scale(PURPLE_BEAM_IMAGE, (60,30))

ORANGE_BEAM_IMAGE = pygame.image.load("Assets/beam_orange.png").convert_alpha()
ORANGE_BEAM = pygame.transform.scale(ORANGE_BEAM_IMAGE, (60,30))


BORDER = pygame.Rect(WIDTH//2 - 5 , 0, 10, HEIGHT)


#load music and sounds
pygame.mixer.music.load('Assets/bg_music.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hit.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/fire.mp3')
WIN_SOUND = pygame.mixer.Sound('Assets/win.mp3')


HEALTH_FONT = pygame.font.SysFont("Comicsans", 40)
WINNER_FONT = pygame.font.SysFont("Comicsans", 100)

def draw_window(purple, orange, purple_bullets, orange_bullets, purple_health, orange_health):
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(PURPLE_SPACESHIP, (purple.x, purple.y))
    WIN.blit(ORANGE_SPACESHIP, (orange.x, orange.y))

    purple_health_text = HEALTH_FONT.render("Health: "+ str(purple_health), True, (255,255,255))
    orange_health_text = HEALTH_FONT.render("Health: "+ str(orange_health), True, (255,255,255))

    WIN.blit(purple_health_text, (10, 10))

    WIN.blit(orange_health_text, (WIDTH - orange_health_text.get_width() - 10, 10))
    for bullet in purple_bullets:
        WIN.blit(PURPLE_BEAM, bullet)
    for bullet in orange_bullets:
        WIN.blit(ORANGE_BEAM, bullet)
    pygame.draw.rect(WIN, NAIVY, BORDER)
    pygame.display.update()

def purple_handle_movement(keys_pressed, purple):
    if keys_pressed[pygame.K_a] and purple.x - VEL > 0:  # LEFT
        purple.x -= VEL
    if keys_pressed[pygame.K_d] and purple.x + VEL + purple.width < BORDER.x:  # RIGHT
        purple.x += VEL
    if keys_pressed[pygame.K_w] and purple.y - VEL > 0:  # UP
        purple.y -= VEL
    if keys_pressed[pygame.K_s] and purple.y + VEL + purple.height < HEIGHT - 15:  # DOWN
        purple.y += VEL


def orange_handle_movement(keys_pressed, orange):
    if keys_pressed[pygame.K_LEFT] and orange.x - VEL > BORDER.x + BORDER.width:  # LEFT
        orange.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and orange.x + VEL + orange.width < WIDTH:  # RIGHT
        orange.x += VEL
    if keys_pressed[pygame.K_UP] and orange.y - VEL > 0:  # UP
        orange.y -= VEL
    if keys_pressed[pygame.K_DOWN] and orange.y + VEL + orange.height < HEIGHT - 15:  # DOWN
        orange.y += VEL

def handle_bullets(purple_bullets, orange_bullets, purple, orange):
    for bullet in purple_bullets:
        bullet.x += BULLET_VEL
        if orange.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ORANGE_HIT))
            purple_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            purple_bullets.remove(bullet) 

    for bullet in orange_bullets:
        bullet.x -= BULLET_VEL
        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            orange_bullets.remove(bullet)

        elif bullet.x < 0:
            orange_bullets.remove(bullet)         

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    WIN_SOUND.play()
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    purple = pygame.Rect(80,HEIGHT//2 - HEIGHT_SPACESHIP//2 , WIDTH_SPACESHIP, HEIGHT_SPACESHIP)
    orange = pygame.Rect(WIDTH - 80 - WIDTH_SPACESHIP ,HEIGHT//2 - HEIGHT_SPACESHIP//2 , WIDTH_SPACESHIP, HEIGHT_SPACESHIP)
    
    purple_bullets = []
    orange_bullets = []

    purple_health = 10
    orange_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(purple_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(purple.x+purple.width, purple.y+ purple.height//2 - 15 ,60, 30)
                    purple_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(orange_bullets) < MAX_BULLET:
                        bullet = pygame.Rect(orange.x - 60 , orange.y + orange.height//2 - 15 , 60, 30)
                        orange_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

            if event.type == PURPLE_HIT:
                purple_health -=1
                BULLET_FIRE_SOUND.play()

            if event.type == ORANGE_HIT:
                orange_health -= 1
                BULLET_FIRE_SOUND.play()

        Winner_text = ""
        if orange_health <= 0:
            Winner_text = "Purple Wins!"
        if purple_health <= 0:
            Winner_text = "Orange Wins!"

        if Winner_text != "":
            draw_winner(Winner_text)
            break
        
        draw_window(purple, orange, purple_bullets, orange_bullets, purple_health, orange_health)
        keys_pressed = pygame.key.get_pressed()
        purple_handle_movement(keys_pressed, purple)
        orange_handle_movement(keys_pressed, orange)
        handle_bullets(purple_bullets, orange_bullets, purple, orange)
    main()

if __name__ == "__main__":
    main()