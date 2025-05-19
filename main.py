import cv2
import mediapipe as mp
import threading

import pygame
from sys import exit
import random


pygame.init()
hand_position_y = None  # en başta global değişken
lives = 3
heart_image = pygame.image.load("assets/redHeart.png")
do_not_collide_timer = 0 #“Kuş şu anda çarpışmaya açık mı, değil mi?”
input_lock_timer = 0

clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images
bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

# Game
scroll_speed = 1
bird_start_position = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True


class Bird(pygame.sprite.Sprite):
    def __init__(self, pos=None):
        super().__init__()
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = bird_start_position[0]
        self.rect.y = bird_start_position[1]
        self.alive = True

    def update(self, user_input):
        global hand_position_y

        if not self.alive:
            return  # Ölü kuş hareket etmez

        if input_lock_timer > 0 and lives < 3:
         # El kontrolü kilitliyken kuşu ortalama bir pozisyonda sabitle
            self.rect.y = 250
            return


        if hand_position_y is not None:
            # Elin Y konumuna göre kuşun yüksekliği ayarlanır
            screen_y = int(hand_position_y * win_height)
            self.rect.y = screen_y

        # Kuş zeminin altına düşmesin
        if self.rect.bottom > 520:
            self.rect.bottom = 520



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        # Move Pipe
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

        # Score
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def detect_hand_position():
    global hand_position_y

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    cap = cv2.VideoCapture(0)

    try:
        while True:
            success, image = cap.read()
            if not success:
                continue

            # Görüntüyü RGB'ye çevir
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = hands.process(image)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                tip_y = hand_landmarks.landmark[8].y  # İşaret parmağı ucu (tip_y 0-1 arası bir oran)
                hand_position_y = tip_y
            else:
                hand_position_y = None

    except Exception as e:
        print(f"Hata oluştu: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()



def game_over_screen():
    global lives
    global score
    window.fill((0, 0, 0))  # Ekranı temizle
    window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                  win_height // 2 - game_over_image.get_height() // 2))  # Bitiş ekranını yerleştir

    # Skoru göster
    score_text = font.render(f'Your Score: {score}', True, pygame.Color(255, 255, 255))
    window.blit(score_text, (win_width // 2 - score_text.get_width() // 2, win_height // 2 + 50))

    # Yeniden başlatma için talimatlar
    restart_text = font.render("Press SPACE to Restart", True, pygame.Color(255, 255, 255))
    window.blit(restart_text, (win_width // 2 - restart_text.get_width() // 2, win_height // 2 + 100))

    pygame.display.update()

    # Kullanıcıdan giriş al
    waiting_for_restart = True
    while waiting_for_restart:
        quit_game()
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:  # Yeniden başlatma tuşu
            restart_game()  # Yeni bir oyun başlat
            waiting_for_restart = False

# Yeni bir oyun başlatmak için fonksiyon
def restart_game():
    global lives, score
    lives = 3  # Canları sıfırla
    score = 0  # Skoru sıfırla
    # Oyun döngüsünü yeniden başlat
    main()  # Ana oyun fonksiyonunu tekrar çağır


# Game Main Method
def main():
    global score, lives, do_not_collide_timer, input_lock_timer
    score = 0
    lives = 3
    do_not_collide_timer = 0
    input_lock_timer = 0

    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())


    # Setup Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))
        for i in range(lives):
            window.blit(heart_image, (win_width - (i + 1) * (heart_image.get_width() + 10) - 10, 10))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        hit_ground_by_position = bird.sprite.rect.bottom >= 520  # zemine değmişse

        # Only lose life if bird is alive and collided
        if bird.sprite.alive and do_not_collide_timer == 0 and (collision_pipes or hit_ground_by_position):
            lives -= 1
            if lives <= 0:
                bird.sprite.alive = False
                game_over_screen()
                return  # oyun baştan başlasın
            else:
                bird.empty()
                bird.add(Bird())  # Yeni bir kuş ekle
                pipes.empty()  # Engelleri temizle
                ground.empty()  # Zemini temizle
                ground.add(Ground(0, 520))  # Yeniden zemin ekle
                do_not_collide_timer = 30  # 30 frame boyunca çarpışma algılanmasın
                input_lock_timer = 20  # 20 frame boyunca input yok sayılacak
                pipe_timer = 0   # Boruların hemen spawn olmasına izin ver
                
                if collision_ground:
                    bird.sprite.rect.bottom = 520  # Kuşun altını zeminin üstüne sabitle


        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(70)
        pygame.display.update()

        if do_not_collide_timer > 0:
            do_not_collide_timer -= 1
        
        if input_lock_timer > 0 and lives < 3:
            input_lock_timer -= 1

threading.Thread(target=detect_hand_position, daemon=True).start()


# Menu
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        ground_temp = Ground(0, 520)
        window.blit(ground_temp.image, ground_temp.rect)
        window.blit(bird_images[0], (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            game_stopped = False
            main()
            game_stopped = True  # tekrar menüye dön


        pygame.display.update()


menu()
