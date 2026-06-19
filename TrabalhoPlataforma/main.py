import pgzrun
import random

# Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Super Pygame Adventure"

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
state = MENU

# Global Variables
score = 0

class MainMenu:
    def __init__(self):
        self.start_button = Rect((300, 200), (200, 50))
        self.audio_button = Rect((300, 300), (200, 50))
        self.exit_button = Rect((300, 400), (200, 50))
        self.music_on = True
        try: music.play("background_theme.wav")
        except: pass

    def draw(self):
        screen.fill((107, 140, 255)) 
        screen.draw.text("SUPER PYGAME ADVENTURE", center=(400, 100), fontsize=60, color="white", shadow=(2,2))

        screen.draw.filled_rect(self.start_button, "green")
        screen.draw.text("START GAME", center=self.start_button.center, color="white")

        audio_color = "orange" if self.music_on else "gray"
        screen.draw.filled_rect(self.audio_button, audio_color)
        audio_text = "MUSIC: ON" if self.music_on else "MUSIC: OFF"
        screen.draw.text(audio_text, center=self.audio_button.center, color="white")

        screen.draw.filled_rect(self.exit_button, "red")
        screen.draw.text("EXIT", center=self.exit_button.center, color="white")

    def handle_click(self, pos):
        if self.start_button.collidepoint(pos):
            try: sounds.click.play()
            except: pass
            reset_game() 

        elif self.audio_button.collidepoint(pos):
            try: sounds.click.play()
            except: pass
            self.music_on = not self.music_on
            
            if self.music_on:
                music.unpause()
            else:
                music.pause()

        elif self.exit_button.collidepoint(pos):
            exit()

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect((x, y), (width, height))

    def draw(self):
        screen.draw.filled_rect(self.rect, (139, 69, 19))
        grass_rect = Rect((self.rect.x, self.rect.y), (self.rect.width, 10))
        screen.draw.filled_rect(grass_rect, (34, 139, 34))

class Player:
    def __init__(self, x, y):
        self.actor = Actor("player_idle_right", (x, y))
        self.velocity_y = 0
        self.speed = 5
        self.gravity = 0.8
        self.jump_strength = -15
        self.is_grounded = False
        self.facing_right = True
        self.animation_timer = 0
        self.run_frame = 1

    def draw(self):
        self.actor.draw()

    def update(self, platforms):
        # Movimentação Lateral: Aceita Setas ou A/D
        if keyboard.left or keyboard.a:
            self.actor.x -= self.speed
            self.facing_right = False
        elif keyboard.right or keyboard.d:
            self.actor.x += self.speed
            self.facing_right = True

        # Gravidade
        self.velocity_y += self.gravity
        self.actor.y += self.velocity_y
        self.is_grounded = False

        # Colisão com Plataformas
        for plat in platforms:
            if self.actor.colliderect(plat.rect):
                if self.velocity_y > 0 and self.actor.bottom >= plat.rect.top:
                    self.actor.bottom = plat.rect.top
                    self.velocity_y = 0
                    self.is_grounded = True

        # Pulo: Aceita Seta para Cima ou W
        if (keyboard.up or keyboard.w) and self.is_grounded:
            self.velocity_y = self.jump_strength
            self.is_grounded = False

        self.update_animation()

    def update_animation(self):
        direction = "right" if self.facing_right else "left"
        if not self.is_grounded:
            self.actor.image = f"player_jump_{direction}"
        # Ativa a animação de corrida se qualquer uma das teclas de andar estiver pressionada
        elif keyboard.left or keyboard.right or keyboard.a or keyboard.d:
            self.animation_timer += 1
            if self.animation_timer > 6:
                self.run_frame = 2 if self.run_frame == 1 else 1
                self.animation_timer = 0
            self.actor.image = f"player_run{self.run_frame}_{direction}"
        else:
            self.actor.image = f"player_idle_{direction}"

class Enemy:
    def __init__(self, x, y, patrol_distance):
        self.actor = Actor("enemy_run1_left", (x, y))
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.speed = 2
        self.moving_left = True
        self.animation_timer = 0
        self.run_frame = 1

    def draw(self):
        self.actor.draw()

    def update(self):
        if self.moving_left:
            self.actor.x -= self.speed
            if self.actor.x <= self.start_x - self.patrol_distance:
                self.moving_left = False
        else:
            self.actor.x += self.speed
            if self.actor.x >= self.start_x + self.patrol_distance:
                self.moving_left = True

        self.update_animation()

    def update_animation(self):
        direction = "left" if self.moving_left else "right"
        self.animation_timer += 1
        if self.animation_timer > 8:
            self.run_frame = 2 if self.run_frame == 1 else 1
            self.animation_timer = 0
        self.actor.image = f"enemy_run{self.run_frame}_{direction}"

class Coin:
    def __init__(self, x, y):
        self.actor = Actor("coin", (x, y))

    def draw(self):
        self.actor.draw()

class Flag:
    def __init__(self, x, y):
        self.actor = Actor("flag", (x, y))

    def draw(self):
        self.actor.draw()

# ================= Funções do Jogo =================

def reset_game():
    global state, player, level_enemies, level_coins, score, level_platforms, level_flag
    score = 0
    player = Player(100, 100) 
    
    level_platforms = [
        Platform(0, 500, 800, 100)
    ]
    
    plat1_x = random.randint(50, 200)
    plat1_y = random.randint(350, 450)
    level_platforms.append(Platform(plat1_x, plat1_y, 150, 20))
    
    plat2_x = random.randint(300, 450)
    plat2_y = random.randint(250, 350)
    level_platforms.append(Platform(plat2_x, plat2_y, 150, 20))
    
    plat3_x = random.randint(550, 650)
    plat3_y = random.randint(150, 250)
    level_platforms.append(Platform(plat3_x, plat3_y, 150, 20))

    level_flag = Flag(plat3_x + 50, plat3_y - 40)
    
    enemy_floor_x = random.randint(300, 600)
    level_enemies = [
        Enemy(enemy_floor_x, 480, 100), 
        Enemy(plat2_x + 50, plat2_y - 20, 50)   
    ]
    
    level_coins = [
        Coin(plat1_x + 50, plat1_y - 40),
        Coin(plat2_x + 50, plat2_y - 40),
        Coin(random.randint(200, 600), 460) 
    ]
    
    state = PLAYING

# Inicialização
menu = MainMenu()
player = Player(100, 100)
level_platforms = [Platform(0, 500, 800, 100)]
level_enemies = []
level_coins = []
level_flag = Flag(700, 160)

def draw():
    screen.clear()
    if state == MENU:
        menu.draw()
        
    elif state == PLAYING:
        screen.fill((107, 140, 255)) 
        for plat in level_platforms:
            plat.draw()
            
        level_flag.draw()
            
        for coin in level_coins:
            coin.draw()
            
        for enemy in level_enemies:
            enemy.draw()
            
        player.draw()
        
        # Interface na tela
        screen.draw.text("Press ESC to return to Menu", topright=(WIDTH - 20, 20))
        screen.draw.text(f"SCORE: {score}", topleft=(20, 20), fontsize=40, color="yellow", shadow=(1,1))
        
    elif state == GAME_OVER:
        screen.fill((0, 0, 0)) 
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2 - 30), fontsize=80, color="red")
        screen.draw.text("Press ENTER to try again", center=(WIDTH/2, HEIGHT/2 + 30), fontsize=40, color="white")
        
    elif state == VICTORY:
        screen.fill((0, 150, 0)) 
        screen.draw.text("LEVEL COMPLETE!", center=(WIDTH/2, HEIGHT/2 - 50), fontsize=80, color="yellow", shadow=(2,2))
        screen.draw.text(f"FINAL SCORE: {score}", center=(WIDTH/2, HEIGHT/2 + 20), fontsize=50, color="white")
        screen.draw.text("Press ENTER to play again", center=(WIDTH/2, HEIGHT/2 + 80), fontsize=30, color="white")

def on_mouse_down(pos):
    if state == MENU:
        menu.handle_click(pos)

def update():
    global state, score
    if keyboard.escape:
        state = MENU
        
    if state == PLAYING:
        player.update(level_platforms)
        
        for enemy in level_enemies:
            enemy.update()
            
        for enemy in level_enemies[:]: 
            if player.actor.colliderect(enemy.actor):
                if player.velocity_y > 0 and player.actor.bottom <= enemy.actor.top + 20:
                    level_enemies.remove(enemy) 
                    player.velocity_y = -12     
                    score += 50 
                else:
                    state = GAME_OVER
                    
        for coin in level_coins[:]:
            if player.actor.colliderect(coin.actor):
                level_coins.remove(coin)
                score += 10
                
        if player.actor.colliderect(level_flag.actor):
            state = VICTORY
                    
    elif state == GAME_OVER or state == VICTORY:
        if keyboard.RETURN or keyboard.KP_ENTER:
            reset_game()

pgzrun.go()
