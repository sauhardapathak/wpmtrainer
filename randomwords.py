import pygame, random, string, sys

pygame.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
tfont = pygame.font.SysFont("Impact", 50)


def generate_text(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img,(x,y))

user_text = ''
words = []
start_time = pygame.time.get_ticks()
game_duration = 10


last_spawn_time = pygame.time.get_ticks()
spawn_delay = 1500
words = generate_text(6)

run = True
while run:
    clock.tick(60)
    window.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()               
        if event.type == pygame.KEYDOWN:
            user_text += event.unicode

    current_time = pygame.time.get_ticks()
    elapsed = (current_time - start_time) / 1000
    remaining = max(0, game_duration - elapsed)

    countdown = tfont.render(str(int(remaining)),True,(0,0,0))

    if current_time - last_spawn_time > spawn_delay:
        draw_text(words, tfont, (0,0,0), 220, 220)
        if user_text == words:
            words = generate_text(6)
            user_text = ''
            last_spawn_time = current_time
    
    window.blit(countdown, (1200, 0))
    pygame.display.update()


    