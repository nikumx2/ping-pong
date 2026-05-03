from pygame import *


win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption('Space Shooter')
win_background = (190,160,200)
window.fill(win_background)

game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font = font.Font(None, 36)
pL_lose = font.render('игрок слева проиграл', True, (200, 0, 0))
pR_lose = font.render('игрок справа проиграл', True, (200, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()


        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
           
        if keys[K_s] and self.rect.y < win_height - 45:
            self.rect.y += self.speed
   
    def update_r(self):
        keys = key.get_pressed()


        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
           
        if keys[K_DOWN] and self.rect.y < win_height - 75:
            self.rect.y += self.speed

player_left = Player('left.png', 30, 310, 5, 30, 70)
player_right = Player('right.png', win_width - 60, 310, 5, 30, 70)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        window.fill(win_background)
        player_left.update_l()
        player_right.update_r()

        player_left.reset()
        player_right.reset()


        display.update()
        clock.tick(FPS)