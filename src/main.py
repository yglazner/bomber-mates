'''
Created on Mar 2, 2016

@author: yoav
'''
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window
from collections import defaultdict
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import itertools
from kivy.uix.floatlayout import FloatLayout
sm = ScreenManager()

KEYS = defaultdict(lambda: None)


class Sprite(Image):
   
    def __init__(self, game, **kwargs):
        self.game = game
        super(Sprite, self).__init__(allow_stretch = True,
                                     size_hint=(None,None), **kwargs)
        self.velocity_x = 0
        self.velocity_y = 0
        self.resting=True
        
    
    def update(self, plats=[]):
        self.velocity_y -= 2
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        for plat in plats:
            if (plat.y+plat.size[1]) > self.y: #hit from below
                self.resting = True
                self.velocity_y = 0
                self.y = plat.y+plat.size[1]

        
class Bomberman(Sprite):
    def __init__(self, **kwargs):
        super(Bomberman, self).__init__(source='./imgs/DUCK.GIF',
                                        **kwargs)
        
        self.bombs = 1
        
        
    def update(self, plats, keys=KEYS):
        if keys[276]:
            self.velocity_x = -5
        elif keys[275]:    
            self.velocity_x = +5
        else:
            self.velocity_x = 0
        if keys[273] and self.resting:
            self.velocity_y = 32
            self.resting = False
        if keys[32] and self.bombs:
            self.bombs -= 1
            self.game.place_bomb(self)
            
        super(Bomberman, self).update(plats)
                
            

        
        



class Platform(Button):
    
    
    
    def __init__(self, **kwargs):
        super(Platform,self).__init__(**kwargs)
        


class GlobalStuff(object):
    
    
    @classmethod
    def init(cls):
        
        cls.center_x = Window.width / 2
        cls.center_y = Window.height / 2
        cls.size = cls.width, cls.height = Window.width, Window.height


class Bomb(Sprite):
    
    def __init__(self, **kws):
        super(Bomb, self).__init__(source='imgs/bomb.png'
                                   
                                   ,**kws)


class Game(Screen):
    area = ObjectProperty(None)
    
    def __init__(self, **kw):
        Screen.__init__(self, **kw)
        self.players = [Bomberman(game=self, 
                                  center_x=GlobalStuff.center_x,
                                  center_y=GlobalStuff.center_y,
                                   size=(50,50)) for i in range(5)]
        self.bombs = []
        for p in self.players:
            self.area.add_widget(p)
            
        self.platforms = []
        floor = Platform(x= 0,
                         y = 0, 
                         size=(GlobalStuff.width*1.2, 50)
                         )
     
        self.platforms.append(floor)
        for plat in self.platforms:
            self.area.add_widget(plat)
        Clock.schedule_interval(self._update, 1.0/36)
        
    def _update(self, dt=None, keys= KEYS):
        
        for p in itertools.chain(self.players, self.bombs):
            print p, p.pos, p.center_x
            plats = []
            for plat in self.platforms:
                if plat.collide_widget(p):
                    plats.append(plat)
                    
            p.update(plats)
        
            
    def place_bomb(self, player):
        bomb = Bomb(game=self, size=[player.width/2, player.height/ 2])
        bomb.center_x = player.center_x
        bomb.center_y = player.center_y
        self.area.add_widget(bomb)
        self.bombs.append(bomb)
            

class PlatBomberApp(App):
    def build(self):
        def on_key_down(window, keycode, *rest):
            KEYS[keycode] = True
        def on_key_up(window, keycode, *rest):
            KEYS[keycode] = False
        Window.bind(on_key_down=on_key_down, on_key_up=on_key_up)
        GlobalStuff.init()
        game = Game(name='game')
        sm.add_widget(game)
        
        return sm

if __name__ == '__main__':
    PlatBomberApp().run()