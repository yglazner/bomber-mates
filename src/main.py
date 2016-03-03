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
sm = ScreenManager()

KEYS = defaultdict(lambda: None)

class Bomberman(Image):
    def __init__(self, *arg, **kwargs):
        Image.__init__(self,  *arg, **kwargs)
        self.source = './imgs/DUCK.GIF'
        self.velocity_x = 0
        self.velocity_y = 0
        self.resting=True
        
    def update(self, keys=KEYS):
        if keys[276]:
            self.velocity_x = -5
        elif keys[273]:    
            self.velocity_x = +5
        else:
            self.velocity_x = 0
        if keys[274] and self.resting:
            self.velocity_y = 16
            self.resting = False
        
        self.velocity_y -= 2    
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        

class Game(Screen):
    area = ObjectProperty(None)
    
    def __init__(self, **kw):
        Screen.__init__(self, **kw)
        self.players = [Bomberman() for i in range(5)]
        for p in self.players:
            self.add_widget(p)
            
        Clock.schedule_interval(self._update, 1.0/36)
    
    def _update(self, dt=None, keys= KEYS):
        print keys
        for p in self.players:
            p.update()


class PlatBomberApp(App):
    def build(self):
        def on_key_down(window, keycode, *rest):
            KEYS[keycode] = True
        def on_key_up(window, keycode, *rest):
            KEYS[keycode] = False
        Window.bind(on_key_down=on_key_down, on_key_up=on_key_up)
        game = Game(name='game')
        sm.add_widget(game)
        return sm

if __name__ == '__main__':
    PlatBomberApp().run()