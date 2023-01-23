import arcade
import random
import time


class Spaceship(arcade.Sprite):
    def __init__(self,game):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png")
        self.center_x=game.width // 2
        self.center_y=60
        self.change_x=0
        self.change_y=0
        self.width=40
        self.height=50
        self.speed=4
        self.game_width=game.width
        self.bullet_list=[]

    def move(self):
        if self.change_x==-1:
            if self.center_x > 0:
                self.center_x -= self.speed
        elif self.change_x==1:
            if self.center_x < self.game_width:
                self.center_x += self.speed

    def fire(self):
        new_bullet=Bullet(self)
        self.bullet_list.append(new_bullet)

class Enemy(arcade.Sprite):
    def __init__(self,w,h):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png")
        self.center_x=random.randint(0,w)
        self.center_y=h+24
        self.change_x=0
        self.change_y=-1
        self.width=40
        self.height=50
        self.angle=180
        self.speed=1
        

    def move(self):
        self.center_y-=self.speed

class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed=20
        self.change_x=0
        self.change_y=1

    def move(self):
        self.center_y += self.speed
        

class Heart(arcade.Sprite):
    def __init__(self, x):
        super().__init__('istockphoto-1128400054-612x612.jpg')
        self.center_x = 30*x
        self.center_y = 20
        self.width = 35
        self.height = 30

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=800,height=800,title="Interstellar")
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)
        self.background=arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.fire_sound=arcade.load_sound(":resources:sounds/hurt5.wav")
        self.explosion_sound=arcade.load_sound(":resources:sounds/explosion1.wav")
        self.me=Spaceship(self)
        self.enemy_list=[]
        self.heart_list = []
        self.time=time.time()
        self.speed_increas=0.3
        for i in range(3):
            heart = Heart(i+1)
            self.heart_list.append(heart)
        self.game_status="run"
        self.score=0



    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,self.width,self.height,self.background)
        self.me.draw()
        for enemy in self.enemy_list:
            enemy.draw()
       
        for bullet in self.me.bullet_list:
            bullet.draw()
            arcade.play_sound(self.fire_sound, volume=0.2)

        for heart in self.heart_list:
            heart.draw()

        arcade.draw_text(f"Score: {self.score}", 9*self.width//10, 20 , arcade.color.WHITE  , bold=True)

        if self.game_status=="Game Over" or len(self.heart_list)==0:
            arcade.draw_lrtb_rectangle_filled(0,self.width,self.height,0,arcade.color.BLACK)
            arcade.draw_text("GAME OVER!", self.width//2 , self.height//2 , arcade.color.RED , 50)

        arcade.finish_render()


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol==arcade.key.LEFT or symbol==arcade.key.A: 
            self.me.change_x=-1
        elif symbol==arcade.key.RIGHT or symbol==arcade.key.D: 
            self.me.change_x=1
        elif symbol==arcade.key.SPACE:
            self.me.fire()




    def on_key_release(self, symbol: int, modifiers: int):
        self.me.change_x=0

    def on_update(self, delta_time: float):
        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy , self.me):
                self.heart_list.pop(-1)
                arcade.play_sound(self.explosion_sound)
                self.enemy_list.remove(enemy)
                self.score -=1
    

        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(enemy , bullet):
                    self.enemy_list.remove(enemy)
                    self.me.bullet_list.remove(bullet)
                    self.score+=1

       
        self.me.move()

        for enemy in self.enemy_list:
            enemy.move()

        for bullet in self.me.bullet_list:
            bullet.move()


        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.enemy_list.remove(enemy)
                if len (self.heart_list)>0:
                    self.heart_list.pop(-1)

        if len(self.heart_list)==0:
            self.game_status="Game Over"

        for bullet in self.me.bullet_list:
            if bullet.center_y > self.width:
                self.me.bullet_list.remove(bullet)
        


        if time.time() - self.time > 3:
            new_enemy=Enemy(self.width,self.height)
            self.enemy_list.append(new_enemy)
            for enemy in self.enemy_list:
                enemy.speed+=self.speed_increas
            self.speed_increas+=0.3

            
            self.time = time.time()

window = Game()
arcade.run()