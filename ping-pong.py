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
main_font = font.Font(None, 36)
pL_lose = main_font.render('Игрок слева проиграл', True, (78,13,104))
pR_lose = main_font.render('Игрок справа проиграл', True, (78,13,104))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
        self.player_image = player_image
        self.height = height
   
    def change_size(self, new_width, new_hight):
        self.image = transform.scale(image.load(self.player_image), (new_width, new_hight))
        old_rect_x = self.rect.x
        old_rect_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_rect_x
        self.rect.y = old_rect_y

    def change_speed(self, new_speed):
        self.speed = new_speed

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

class TextArea():
    def __init__(self, x=0, y=0, width=10, height=10, color=(255, 255, 255)):
        self.rect = Rect(x, y, width, height)
        self.fill_color = color
    def set_text(self, text, fsize=18, text_color = (0, 0, 0)):
        self.text = text
        self.image = font.Font(None, fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        draw.rect(window, self.fill_color, self.rect)
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def collide_point(self, x, y):
        return self.rect.collidepoint(x, y)
        



player_left = Player('left.png', 30, 310, 5, 30, 70)
player_right = Player('right.png', win_width - 60, 310, 5, 30, 70)
ball = GameSprite('ball.png', win_width / 2 - 15, win_height / 2 - 15, 5, 30, 30)
speed_x = 5
speed_y = 5
ball_start_x = win_width / 2 - 15
ball_start_y = win_height / 2 - 15

btn_start = TextArea(win_width /2 - 90, win_height /2 - 70, 200, 100)
btn_start.set_text('Старт', 40)

btn_settings = TextArea(win_width / 2 - 90, win_height /2 + 70, 200, 100)
btn_settings.set_text('Настройки', 40)

counter_L = 0
counter_R = 0
in_game = False
in_settings = False
main_menu = False



# настройки
btn_easy = TextArea(win_width / 2 - 90, win_height /2 - 250, 200, 100)
btn_easy.set_text('Easy', 40)

btn_middle = TextArea(win_width / 2 - 90, win_height /2 - 130, 200, 100)
btn_middle.set_text('Middle', 40)

btn_hard = TextArea(win_width / 2 - 90, win_height /2 - 10, 200, 100)
btn_hard.set_text('Hard', 40)

btn_back = TextArea(win_width / 2 - 90, win_height /2 + 110, 200, 100)
btn_back.set_text('Back', 40)





while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos

            if main_menu:
                if btn_start.collide_point(x, y):
                    finish = False
                    main_menu = False
                    in_game = True
                elif btn_settings.collide_point(x,y):
                    in_settings = True
                    main_menu = False

            if btn_back.collide_point(x, y) and in_settings:
                in_settings = False
                main_menu = True
            
            if btn_easy.collide_point(x, y) and in_settings:
                speed_x = 5
                speed_y = 5
                player_left.change_size(15, 80)
                player_right.change_size(15, 80)
                player_left.change_speed(15)
                player_right.change_speed(15)
            
            if btn_middle.collide_point(x, y) and in_settings:
                speed_x = 7.5
                speed_y = 7.5
                player_left.change_size(15, 55)
                player_right.change_size(15, 55)
                player_left.change_speed(17)
                player_right.change_speed(17)

            if btn_hard.collide_point(x, y) and in_settings:
                speed_x = 10
                speed_y = 10
                player_left.change_size(15, 40)
                player_right.change_size(15, 40)
                player_left.change_speed(19)
                player_right.change_speed(19)  
        
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                finish = True
                main_menu = True
                in_settings = True

    if finish == False:
        in_game = True
        in_settings = False
        main_menu = False
        window.fill(win_background)
        player_left.update_l()
        player_right.update_r()

        # перемещение мяча
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # отскоки мяча от стен сверху и снизу
        if ball.rect.y <= 0 or ball.rect.y >= win_height - 30:
            speed_y *= -1
        
        # отскоки мяча от ракеток
        if sprite.collide_rect(player_left, ball) or sprite.collide_rect(player_right, ball):
            speed_x *= -1
        
        # проверка, что мяч ушел за край экрана (кто-то из игроков проиграл)
        if ball.rect.x <= 0:
            finish = True
            main_menu = True
            ball.rect.x = ball_start_x
            ball.rect.y = ball_start_y
            window.blit(pL_lose, (260, 180))
        
        if ball.rect.x >= win_width - 30:
            finish = True
            main_menu = True
            ball.rect.x = ball_start_x
            ball.rect.y = ball_start_y
            window.blit(pR_lose, (260, 180))

        player_left.reset()
        player_right.reset()
        ball.reset()

    elif in_settings:
        window.fill(win_background)
        btn_easy.draw(15, 40)
        btn_middle.draw(15, 40)
        btn_hard.draw(15, 40)
        btn_back.draw(15, 40)

    elif main_menu:
        window.fill(win_background)
        if in_game:
            btn_start.set_text('Продолжить игру', 30)
            btn_start.draw(15, 40)
        else:
            btn_start.set_text('Начать игру', 40)
            btn_start.draw(20, 40)
        btn_settings.draw(30, 40)

        


    display.update()
    clock.tick(FPS)