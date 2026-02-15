import pygame, random, string, sys
from highscore import check_and_update_highscore, load_highscore

pygame.init()
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
tfont = pygame.font.SysFont("Impact", 50)

# Get difficulty from command line argument
if len(sys.argv) > 1:
    difficulty = sys.argv[1]
else:
    difficulty = "medium"  # Default

# Set parameters based on difficulty
if difficulty == "easy":
    spawn_delay = 5000  # 5 seconds
    word_speed = 2
    word_length = 4
elif difficulty == "medium":
    spawn_delay = 4000  # 4 seconds
    word_speed = 3
    word_length = 6
elif difficulty == "hard":
    spawn_delay = 2500  # 2.5 seconds
    word_speed = 5
    word_length = 8
else:
    # Default to medium
    spawn_delay = 4000
    word_speed = 3
    word_length = 6


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
score = 0


last_spawn_time = pygame.time.get_ticks()

run = True
while run:
    clock.tick(60)
    window.fill((25,25,35))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()               
        if event.type == pygame.KEYDOWN:
            # ESC to quit anytime
            if event.key == pygame.K_ESCAPE:
                run = False
            
            # Typing only when game is active
            if not game_over:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode:
                    user_text += event.unicode

    current_time = pygame.time.get_ticks()

    if not game_over and lives <= 0:
        game_over = True

    if not game_over and current_time - last_spawn_time > spawn_delay:
        words.append({
            "text": generate_text(word_length),
            "x": random.randint(100, 1100),
            "y": 0,
            "speed": word_speed
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
                score += 1
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
    heart_x = 50
    for i in range(lives):
        heart_text = tfont.render("♥", True, (255, 100, 100))
        window.blit(heart_text, (heart_x + i * 50, 0))

    # Display empty hearts
    for i in range(3 - lives):
        empty_heart = tfont.render("", True, (80, 80, 90))
        window.blit(empty_heart, (heart_x + (lives + i) * 50, 0))

    # Score display
    score_text = tfont.render(f"Score: {score}", True, (100, 255, 150))
    window.blit(score_text, (1050, 0))

     # Game over screen
    if game_over:
        window.fill((15, 15, 20))

        # New high score indicator
        current_high = load_highscore()
        is_new_high = score > current_high
        
        if is_new_high:
            game_over_text = tfont.render("NEW HIGH SCORE!", True, (255, 215, 0))
        else:
            game_over_text = tfont.render("GAME OVER", True, (255, 100, 100))

        game_over_rect = game_over_text.get_rect(center=(640, 200))
        window.blit(game_over_text, game_over_rect)


        # Stats box background
        stats_bg = pygame.Surface((600, 300))
        stats_bg.fill((30, 30, 40))
        stats_bg.set_alpha(230)
        window.blit(stats_bg, (340, 280))
        
        # Stats
        smaller_font = pygame.font.SysFont("Impact", 35)
        
        score_final = smaller_font.render(f"Words Typed: {score}", True, (100, 255, 150))
        score_rect = score_final.get_rect(center=(640, 340))
        window.blit(score_final, score_rect)
        
        missed_final = smaller_font.render(f"Words Missed: {missed_words}", True, (255, 100, 100))
        missed_rect = missed_final.get_rect(center=(640, 400))
        window.blit(missed_final, missed_rect)
        
        accuracy = (score / (score + missed_words) * 100) if (score + missed_words) > 0 else 0
        accuracy_text = smaller_font.render(f"Accuracy: {accuracy:.1f}%", True, (180, 180, 200))
        accuracy_rect = accuracy_text.get_rect(center=(640, 460))
        window.blit(accuracy_text, accuracy_rect)
        
        # Restart hint
        hint_font = pygame.font.SysFont("Impact", 25)
        hint = hint_font.render("Press ESC to quit", True, (120, 120, 130))
        hint_rect = hint.get_rect(center=(640, 550))
        window.blit(hint, hint_rect)

    if not game_over and user_text:
        input_bg = pygame.Surface((400, 60))
        input_bg.fill((40, 40, 50))
        input_bg.set_alpha(200)
        window.blit(input_bg, (440, 640))
        
        input_text = tfont.render(user_text, True, (100, 255, 150))
        input_rect = input_text.get_rect(center=(640, 670))
        window.blit(input_text, input_rect)


    pygame.display.update()

if score > 0:
    is_new_high = check_and_update_highscore(score)

pygame.quit()