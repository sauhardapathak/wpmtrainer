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
lives = 3
missed_words = 0
game_over = False


last_spawn_time = pygame.time.get_ticks()
spawn_delay = 4000  # Spawn a new word every 4 seconds

run = True
while run:
    clock.tick(60)
    window.fill((25,25,35))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()               
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]  # Remove last character
            elif event.unicode:  # Only add if it's a printable character
                user_text += event.unicode

    current_time = pygame.time.get_ticks()

    if not game_over and lives <= 0:
        game_over = True

    if not game_over and current_time - last_spawn_time > spawn_delay:
        words.append({
            "text": generate_text(6),
            "x": random.randint(100, 1100),
            "y": 0,
            "speed": 3
        })
        last_spawn_time = current_time

    # 2. Update ALL words (ALWAYS - every frame)
    if not game_over:
        for word in words:
            word["y"] += word["speed"]

        if user_text:
            any_match = any(word["text"].startswith(user_text) for word in words)
            if not any_match:
                user_text = ''  # Clear input if no match

        # Check for user input and remove matched words
        for word in words[:]:
            if user_text == word["text"]:
                words.remove(word)
                user_text = ''
                break
    
    for word in words[:]:  # Iterate over a copy of the list
        if user_text and word["text"].startswith(user_text):
            matched_length = len(user_text)
        else:
            matched_length = 0

        if matched_length > 0:
            matched_part = word["text"][:matched_length]
            remaining_part = word["text"][matched_length:]

            matched_surface = tfont.render(matched_part, True, (100, 255, 150))  # Soft green
            remaining_surface = tfont.render(remaining_part, True, (120, 120, 130))  # Dimmed gray
            window.blit(matched_surface, (word["x"], word["y"]))

            if remaining_part:
                remaining_surface = tfont.render(remaining_part, True, (0,0,0))
                window.blit(remaining_surface, (word["x"] + matched_surface.get_width(), word["y"]))
        else:
            normal_surface = tfont.render(word["text"], True, (200, 200, 210))  # Light gray-blue
            window.blit(normal_surface, (word["x"], word["y"]))

    if not game_over:
        newly_missed = sum(1 for word in words if word["y"] >= 720)
        missed_words += newly_missed
        words = [word for word in words if word["y"] < 720]
        lives = max(0, 3 - missed_words)
    
    # Display UI
    lives_text = tfont.render(f"Lives: {lives}", True, (255, 100, 100))  # Soft red
    window.blit(lives_text, (50, 0))

     # Game over screen
    if game_over:
        window.fill((15, 15, 20))  # Very dark background
        
        # Game over text
        game_over_text = tfont.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(640, 300))  # Screen width / 2 = 640
        window.blit(game_over_text, game_over_rect)
        
        # Stats text
        stats_text = tfont.render(f"Words Missed: {missed_words}", True, (180, 180, 200))
        stats_rect = stats_text.get_rect(center=(640, 400))
        window.blit(stats_text, stats_rect)
        
    pygame.display.update() 