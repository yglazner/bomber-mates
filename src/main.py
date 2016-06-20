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
from kivy.uix.label import Label
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
        
    
    def update(self, plats=[],):
        self.velocity_y -= 2
        self.x += self.velocity_x
        
        for plat in plats:
            if not plat.collide_widget(self): continue
            if self.velocity_x > 0:
                self.right = plat.x - 1
            else:
                self.x = plat.right + 1
        
        self.y += self.velocity_y
        for plat in plats:
            if not plat.collide_widget(self): continue
            if self.velocity_y > 0:
                self.top = plat.y - 1
            else:
                self.y = plat.top  + 1
                self.resting = True
                self.velocity_y = 0
        
class Bomberman(Sprite):
    def __init__(self, **kwargs):
        super(Bomberman, self).__init__(source='./imgs/DUCK.GIF',
                                        **kwargs)
        
        self.bombs = 1
        
        #Image.canvas
        
        
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
        if self.velocity_y < -10: self.velocity_y = -10
        super(Bomberman, self).update(plats)
                
            

    def bomb_done(self, bomb):
        self.bombs += 1
        self.game.remove_bomb(bomb)
        



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
    
    def __init__(self, owner, **kws):
        super(Bomb, self).__init__(source='imgs/bomb.png'
                                   
                                   ,**kws)
        self.owner = owner
        self.count = 70
        
    def blast(self):
        self.source = 'imgs/blast.png'
        
    
    def update(self, plats=[],):
        Sprite.update(self, plats=plats,)
        self.count -= 1
        if self.count == 0:
            self.blast()
        if self.count == -50:
            self.owner.bomb_done(self) 
        
    
    
        


class Game(Screen):
    area = ObjectProperty(None)
    
    def __init__(self, **kw):
        Screen.__init__(self, **kw)
        self.players = [Bomberman(game=self, 
                                  center_x=GlobalStuff.center_x,
                                  center_y=GlobalStuff.center_y,
                                   size=(50,50)) for i in range(5)]
        self.label = Label(text="FPS: ?", pos=(125, 125))
        
        self.bombs = []
        for p in self.players:
            self.area.add_widget(p)
            
        self.platforms = []
        floor = Platform(x= 0,
                         y = 0, 
                         size=(GlobalStuff.width*1.0, 50)
                         )
        walls = (Platform(x=0,y=0, size=(50, GlobalStuff.height)),
                 Platform(x=0,y=GlobalStuff.height-50, size=(GlobalStuff.width*1.0, 50)),
                 Platform(x=GlobalStuff.width-50,y=0, size=(50, GlobalStuff.height)),
                 ) 
     
        self.platforms.append(floor)
        self.platforms.extend(walls)
        for plat in self.platforms:
            self.area.add_widget(plat)
        self.count = 0
        self.frames_count = 0
        Clock.schedule_interval(self._update, 1.0/36)
        self.add_widget(self.label)
        
    def _update(self, dt=None, keys= KEYS):
        
        self.count += dt
        self.frames_count += 1
        plats = self.platforms
        for p in itertools.chain(self.players, self.bombs):
            #print p, p.pos, p.center_x
            
           
                    
            p.update(plats)
        if self.count > 1.0:
            self.label.text = "FPS: %.1f" % (self.frames_count / self.count)
            self.count = self.frames_count = 0.0
            
    def place_bomb(self, player):
        bomb = Bomb(owner=player, game=self, size=[player.width/2, player.height/ 2])
        bomb.center_x = player.center_x
        bomb.center_y = player.center_y
        self.area.add_widget(bomb)
        self.bombs.append(bomb)
        #bomb.start_counting()
        
    def remove_bomb(self, bomb):
        self.bombs.remove(bomb)
        self.area.remove_widget(bomb)
            

class PlatBomberApp(App):
    def on_start(self):
        import cProfile
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')
    
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