import pgzrun

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
        music.play("background_theme.wav")

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
            sys.exit()

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
        if keyboard.left:
            self.actor.x -= self.speed
            self.facing_right = False
        elif keyboard.right:
            self.actor.x += self.speed
            self.facing_right = True

        self.velocity_y += self.gravity
        self.actor.y += self.velocity_y
        self.is_grounded = False

        for plat in platforms:
            if self.actor.colliderect(plat.rect):
                if self.velocity_y > 0 and self.actor.bottom >= plat.rect.top:
                    self.actor.bottom = plat.rect.top
                    self.velocity_y = 0
                    self.is_grounded = True

        if keyboard.up and self.is_grounded:
            self.velocity_y = self.jump_strength
            self.is_grounded = False

        self.update_animation()

    def update_animation(self):
        direction = "right" if self.facing_right else "left"
        if not self.is_grounded:
            self.actor.image = f"player_jump_{direction}"
        elif keyboard.left or keyboard.right:
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
    global state, player, level_enemies, level_coins, score
    score = 0
    player = Player(100, 100) 
    
    level_enemies = [
        Enemy(400, 480, 100), 
        Enemy(675, 180, 50)   
    ]
    
    level_coins = [
        Coin(200, 360),
        Coin(250, 360),
        Coin(450, 260)
    ]
    
    state = PLAYING

# Inicialização
menu = MainMenu()
player = None
level_enemies = []
level_coins = []
level_flag = Flag(700, 160) # Bandeira no final da fase

level_platforms = [
    Platform(0, 500, 800, 100),   
    Platform(150, 400, 150, 20),  
    Platform(400, 300, 150, 20),  
    Platform(600, 200, 150, 20)   
]

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
        screen.fill((0, 150, 0)) # Fundo verde para vitória
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
            
        # Lógica de Colisão com Inimigos (Mario)
        for enemy in level_enemies[:]: 
            if player.actor.colliderect(enemy.actor):
                if player.velocity_y > 0 and player.actor.bottom <= enemy.actor.top + 20:
                    level_enemies.remove(enemy) 
                    player.velocity_y = -12     
                    score += 50 # Ganha pontos ao derrotar inimigo!
                else:
                    state = GAME_OVER
                    
        # Lógica de Coleta de Moedas
        for coin in level_coins[:]:
            if player.actor.colliderect(coin.actor):
                level_coins.remove(coin)
                score += 10
                
        # Lógica de Chegada na Bandeira
        if player.actor.colliderect(level_flag.actor):
            state = VICTORY
                    
    elif state == GAME_OVER or state == VICTORY:
        if keyboard.RETURN or keyboard.KP_ENTER:
            reset_game()

pgzrun.go()
