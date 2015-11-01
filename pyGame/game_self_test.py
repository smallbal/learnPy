from tkinter import *
import random
import time

# !/usr/bin/env python3
# -*-coding:utf-8-*-

__author__ = 'guest_zjr'




class Game:
   def __init__(self):
        self.tk = Tk()
        self.tk.title("Run and Fucking escape!")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.bg = PhotoImage(file="./FUCK/background.gif")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x*w, y*h, image=self.bg, anchor='nw')
        self.sprites = []  # sprite:精灵
        self.running = True

   def mainloop(self):
        while True:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


# 坐标类
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


# x轴方向检测碰撞
def collision_x(co1, co2):
    if co2.x1 <= co1.x1 <= co2.x2:
        return True
    elif co2.x1 <= co1.x2 <= co2.x2:
        return True
    elif co1.x1 <= co2.x1 <= co1.x2:
        return True
    elif co1.x1 <= co2.x2 <= co1.x2:
        return True
    else:
        return False


# y轴方向检测碰撞
def collision_y(co1, co2):
    if co2.y1 <= co1.y1 <= co2.y2:
        return True
    elif co2.y1 <= co1.y2 <= co2.y2:
        return True
    elif co1.y1 <= co2.y1 <= co1.y2:
        return True
    elif co1.y1 <= co2.y2 <= co1.y2:
        return True
    else:
        return False


# 左边碰撞检测
def collision_left(colliding, collided):
    if collision_y(colliding, collided):
        if collided.x1 <= colliding.x1 <= collided.x2:
            return True
    return False


# 右边碰撞检测
def collision_right(colliding, collided):
    if collision_y(colliding, collided):
        if collided.x1 <= colliding.x2 <= collided.x2:
            return True
    return False


# 底部碰撞检测
def collision_bottom(colliding, collided, y):
    if collision_x(colliding, collided):
        y_calc = colliding.y2 + y
        if collided.y1 <= y_calc <= collided.y2:
            return True
    return False


# 顶端碰撞检测
def collision_top(colliding, collided):
    if collision_x(colliding, collided):
        if collided.y1 <= collided.y1 <= collided.y2:
            return True
    return False


class Sprite:
    def __init__(self, game):
        self.game = game
        self.end_game = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x+width, y+height)


class Man(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.image_left = [
            PhotoImage(file='./FUCK/kidL1.gif'),
            PhotoImage(file='./FUCK/kidL2.gif'),
            PhotoImage(file='./FUCK/kidL3.gif')
        ]
        self.image_right = [
            PhotoImage(file='./FUCK/kidR1.gif'),
            PhotoImage(file='./FUCK/kidR2.gif'),
            PhotoImage(file='./FUCK/kidR3.gif')
        ]
        self.image = game.canvas.create_image(20, 40, image=self.image_left[1], anchor='nw')
        self.current_image_add = 1  # 图片变换的顺序
        self.current_image = 1
        self.x = 0
        self.y = 4
        self.jump_status = False  # 当前小人是否激发了跳跃
        self.jump_count = 0  # 跳跃时间拍数
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

        self.on_bottom = False
        self.on_top = False
        self.on_left = False
        self.on_right = False
        self.on_platform = False
        self.on_falling = True

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2

    def jump(self, event):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0
            self.jump_status = True
            self.on_falling = False

    def animate(self):  # 人物动画动作设定
        if self.x != 0 and self.y == 0 \
                and time.time() - self.last_time > 0.1:
            self.current_image += self.current_image_add
            if self.current_image >= 2:
                self.current_image_add = -1
            elif self.current_image <= 0:
                self.current_image_add = 1
            #else:
                #self.current_image_add = 0
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_left[2])
            else:
            #   print('Left Flash',self.current_image, self.current_image_add)
                self.game.canvas.itemconfig(self.image, image=self.image_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_right[2])
            else:
            #    print('Right Flash', self.current_image, self.current_image_add)
                self.game.canvas.itemconfig(self.image, image=self.image_right[self.current_image])
        else:
            if self.y == 0:
                self.game.canvas.itemconfig(self.image, image=self.image_right[1])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        self.animate()
        mans_co = self.coords()
        if self.y == 0 and (not self.on_platform) and (not self.on_bottom):
            self.y = 4
            self.on_falling = True
        if self.y > 0 and mans_co.y2 >= self.game.canvas_height:
            self.y = 0
            self.on_bottom = True
            self.on_platform = False
            self.on_falling = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coordinates
            if self.y > 0 and collision_bottom(mans_co, sprite_co, 0):
                self.y = 0
                self.on_platform = True
                self.on_bottom = False
                self.on_falling = False
                break
            else:
                self.on_platform = False
                self.on_bottom = False
                self.on_falling = True


        if self.jump_status:
            pass
        self.game.canvas.move(self.image, self.x, self.y)
        print(self.y, self.on_platform, self.on_bottom, self.on_falling)



jump_game = Game()
platform1 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 0, 480, 100, 10)
platform2 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 150, 440, 100, 10)
platform3 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 300, 400, 100, 10)
platform4 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 300, 160, 100, 10)
platform5 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformMiddle.gif'), 175, 350, 66, 10)
platform6 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformMiddle.gif'), 50, 300, 66, 10)
platform7 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformMiddle.gif'), 170, 120, 66, 10)
platform8 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformMiddle.gif'), 45, 60, 66, 10)
platform9 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 200, 270, 100, 10)
platform10 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/plateformLong.gif'), 330, 210, 100, 10)
jump_game.sprites.append(platform1)
jump_game.sprites.append(platform2)
jump_game.sprites.append(platform3)
jump_game.sprites.append(platform4)
jump_game.sprites.append(platform5)
jump_game.sprites.append(platform6)
jump_game.sprites.append(platform7)
jump_game.sprites.append(platform8)
jump_game.sprites.append(platform9)
jump_game.sprites.append(platform10)

stick_man = Man(jump_game)
jump_game.sprites.append(stick_man)

jump_game.mainloop()



'''
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and mans_co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and mans_co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and mans_co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and mans_co.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collision_top(mans_co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collision_bottom(mans_co, sprite_co, self.y):
                self.y = sprite_co.y1 - mans_co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and mans_co.y2 < self.game.canvas_height \
                and collision_bottom(mans_co, sprite_co, 1):
                falling = False
            if left and self.x < 0 and collision_left(mans_co, sprite_co):
                self.x = 0
                right = False
                if sprite.end_game:
                    self.game.running = False
            if right and self.x > 0 and collision_right(mans_co, sprite_co):
                self.x = 0
                right = False
                if sprite.end_game:
                    self.game.running = False
        if falling and bottom and self.y == 0 and mans_co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)
        '''