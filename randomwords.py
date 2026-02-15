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
game_duration = 60


last_spawn_time = pygame.time.get_ticks()
spawn_delay = 4000  # Spawn a new word every 3 seconds

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
        words.append({
            "text": generate_text(6),
            "x": random.randint(100, 1100),
            "y": 0,
            "speed": 3
        })
        last_spawn_time = current_time
        # 2. Update ALL words (ALWAYS - every frame)
    for word in words:
        word["y"] += word["speed"]

    # 3. Draw ALL words (ALWAYS - every frame)
    for word in words:
        draw_text(word["text"], tfont, (0,0,0), word["x"], word["y"])
    
    for word in words[:]:  # Iterate over a copy of the list
        if user_text == word["text"]:
            words.remove(word)
            user_text = ''
            last_spawn_time = current_time
    
    window.blit(countdown, (1200, 0))
    pygame.display.update() 