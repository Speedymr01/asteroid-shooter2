import pygame, sys, time, os
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        self.can_shoot = True
        self.shoot_time = None
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.input_position()
        self.laser_timer()
        self.laser_shoot()
        self.meteor_collision()
    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.rect.midtop, laser_group)
            play_sound(4)
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 250:
                self.can_shoot = True
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            if score > open_highscore('read'): open_highscore('write')
            pygame.mixer.stop()
            play_sound(7)
            time.sleep(3)
            pygame.quit()
            sys.exit()

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 1000
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.meteor_collision()
        if self.rect.bottom < 0: self.kill()
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()
            global score
            score += 1
            play_sound(5)
    
class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load('./graphics/meteor.png')
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.scaled_surf

        self.rotation = 0
        self.rotation_speed = randint(20, 50)
    
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = uniform(lb_meteor_speed, ub_meteor_speed)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        #self.meteor_collision()
        if self.rect.top > WINDOW_HEIGHT: self.kill()
    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

class Score:
    def __init__(self):
        self.font = pygame.font.Font('./graphics/subatomic.ttf', 50)
    def display(self):
        score_text = f'Score: {round(score)}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 4, WINDOW_HEIGHT - 50))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width = 8, border_radius = 5)

class Highscore:
    def __init__(self):
        self.font = pygame.font.Font('./graphics/subatomic.ttf', 50)
    def display(self):
        Highscore_text = f'Highscore: {open_highscore('read')}'
        text_surf = self.font.render(Highscore_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 4 * 3, WINDOW_HEIGHT - 50))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width = 8, border_radius = 5)
       
def open_highscore(mode = 'read'):
    if mode == 'read':
        highscorefile = open('HighScore.txt', mode= 'r')
        highscore = highscorefile.read()
        highscore = round(float(highscore))
        highscorefile.close()
        return highscore
    if mode == 'write':
        highscorefile = open('HighScore.txt', mode= 'w')
        highscorefile.write(str(score))
        highscorefile.close()

def init(version = '3.0'):
    global WINDOW_WIDTH, WINDOW_HEIGHT, lb_meteor_speed, ub_meteor_speed, sounds, display_surface, score, clock
    pygame.init()
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f'Asteroid Shooter v{version}')
    clock = pygame.time.Clock()
    score = 0
    lb_meteor_speed = score*1.5 + 200
    ub_meteor_speed = score*1.5 + 400
    sounds = {}
    sounds[1] = pygame.mixer.Sound('./sounds/level1.wav')
    sounds[2] = pygame.mixer.Sound('./sounds/level0.wav')
    sounds[3] = pygame.mixer.Sound('./sounds/level-.wav')
    sounds[4] = pygame.mixer.Sound('./sounds/8-bit-laser-151672.mp3')
    sounds[5] = pygame.mixer.Sound('./sounds/explosion.wav')
    sounds[6] = pygame.mixer.Sound('./sounds/422590-Mobile-Game-Melodic-Stinger-Floating-Level-Up-1.wav') 
    sounds[7] = pygame.mixer.Sound('./sounds/game-over-39-199830.mp3')
    sounds[1].set_volume(0.2)
    sounds[2].set_volume(0.2)
    sounds[3].set_volume(0.2)
    sounds[4].set_volume(0.4)
    sounds[5].set_volume(0.2)
    sounds[6].set_volume(0.5)
    sounds[7].set_volume(0.3)



init('3.0')

    


def play_sound(soundindex):
    sounds[soundindex].play()





# background
background_surface = pygame.image.load('./graphics/background.png').convert()

# Sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

Meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(Meteor_timer, 250)
ship = Ship(spaceship_group)
scoreobj = Score()
highscoreobj = Highscore()
soundindex = 0


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open_highscore('write')
            pygame.quit()
            sys.exit()
        if event.type == Meteor_timer:
            meteor_y_pos = randint(-150, -50)
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Meteor((meteor_x_pos,meteor_y_pos), meteor_group)

    # Sound logic
    if not pygame.mixer.get_busy():
        soundindex += 1
        play_sound(soundindex)



    if score > 5:
        if score % 40 == 0:
            play_sound(6)
            score += 0.1
    dt = clock.tick() / 1000
    lb_meteor_speed = score*1.5 + 200
    ub_meteor_speed = score*1.5 + 400
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()
    display_surface.blit(background_surface, (0,0))
    
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)
    scoreobj.display()
    highscoreobj.display()
    pygame.display.update()