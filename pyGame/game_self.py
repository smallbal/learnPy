from tkinter import *
import tkinter.messagebox as messagebox
import time

__author__ = 'guest_zjr'
# !/usr/bin/env python3
# -*-coding:utf-8-*-



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


class DoorSprite(Sprite):
    def __init__(self, game, man, x, y):
        Sprite.__init__(self, game)
        self.photo_image = [
            PhotoImage(file='./FUCK/door1.gif'),
            PhotoImage(file='./FUCK/door2.gif')
        ]
        self.man = man
        self.image = game.canvas.create_image(x, y, image=self.photo_image[0], anchor='nw')
        self.coordinates = Coords(x, y, x+27, y+30)

    def coords(self):
        return self.coordinates

    def move(self):
        mans_co = self.man.coords()
        if collision_left(mans_co, self.coordinates) \
                or collision_right(mans_co, self.coordinates):
            self.game.canvas.itemconfig(self.image, image=self.photo_image[1])
            # 弹出消息框提示
            messagebox.showinfo('Win', 'You Get the Fucking Door!')
            # 设置小人为静止状态
            self.game.canvas.itemconfig(self.man.image, image=self.man.image_left[1])
            self.man.x = 0
            # 将小人移动到“下面”重新以便于重新玩。这里只用了move()方法，改进的地方很多，只是目前效果达到了。
            self.game.canvas.move(self.man.image, 0, 400)

        else:
            self.game.canvas.itemconfig(self.image, image=self.photo_image[0])


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
        self.image = game.canvas.create_image(0, 450, image=self.image_left[1], anchor='nw')
        self.current_image_add = 1  # 图片变换的顺序
        self.current_image = 1
        self.x = -2
        self.y = 0
        self.jump_status = False  # 当前小人是否激发了跳跃
        self.jump_count = 0  # 跳跃时间拍数
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2

    def jump(self, event):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0
            self.jump_status = True

    def animate(self):  # 人物动画动作设定
        if self.x != 0 and self.y == 0 \
                and time.time() - self.last_time > 0.1:
            self.current_image += self.current_image_add
            if self.current_image >= 2:
                self.current_image_add = -1
            elif self.current_image <= 0:
                self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.image_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.image_right[2])
            else:
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
        if self.jump_status:
            if self.y <= 0:
                self.jump_count += 1
                if self.jump_count >= 20:
                    self.y = 4
            if self.y > 0:
                self.jump_count -= 1
                if self.jump_count <= 0:
                    self.jump_count = 0
                    self.jump_status = False
        mans_co = self.coords()
        on_bottom = False
        on_top = False
        on_left = False
        on_right = False
        on_platform = False
        on_falling = True
        # 游戏框边缘冲突检测
        if self.y > 0 and mans_co.y2 >= self.game.canvas_height:  # 是否到框底
            on_bottom = True
            self.y = 0
        elif self.y < 0 and mans_co.y1 <= 0:  # 是否到框顶
            on_top = True
            self.y = 4  # 撞到游戏框顶端马上向下反弹
        if self.x > 0 and mans_co.x2 >= self.game.canvas_width:  # 是否到框右边
            on_right = True
            self.x = 0
        elif self.x < 0 and mans_co.x1 <= 0:  # 是否到框左边
            on_left = True
            self.x = 0
        else:
            pass
        # 小人与游戏场景道具的碰撞检测
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if self.y > 0 and collision_bottom(mans_co, sprite_co, 4):
                self.y = sprite_co.y1 - mans_co.y2
                on_bottom = False
                on_platform = True
            if sprite_co.y1 - 1 < mans_co.y2 < sprite_co.y1 + 1 and self.y == 0:
                if (self.x > 0 and sprite_co.x2 - 1 < mans_co.x1 < sprite_co.x2 + 1) \
                        or (self.x < 0 and sprite_co.x1 - 1 <= mans_co.x2 <= sprite_co.x1 + 1):
                    # 当判断条件写成： sprite_co.x1 - 1 < mans_co.x2 < sprite_co.x1 +1 时，
                    # 小人从平台左边落下的检测就会有bug
                    self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)


jump_game = Game()
platform1 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 0, 480, 100, 10)
platform2 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 150, 440, 100, 10)
platform3 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 300, 400, 100, 10)
platform4 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 300, 160, 100, 10)
platform5 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformMiddle.gif'), 175, 350, 66, 10)
platform6 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformMiddle.gif'), 50, 300, 66, 10)
platform7 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformMiddle.gif'), 170, 120, 66, 10)
platform8 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformMiddle.gif'), 45, 60, 66, 10)
platform9 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 200, 270, 100, 10)
platform10 = PlatformSprite(jump_game, PhotoImage(file='./FUCK/platformLong.gif'), 330, 210, 100, 10)
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

door = DoorSprite(jump_game, stick_man, 50, 30)
jump_game.sprites.append(door)

jump_game.mainloop()



