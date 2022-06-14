# программа с двумя экранами
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from random import randint

class Tile:
    def __init__(self,value=0):
        self.value = value
        self.neighs = []
        self.button = Button(text=str(value))
    
    def add_neig(self,tile):
        self.neighs.append(tile)

class Fied:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.tiles = []
        self.restart_field()

    def restart_field(self):
        self.fill_tiles() #заполнить массив клеточками
        self.set_neighs() #проставить соседей у клеточек

    def fill_tiles(self):
        self.tiles = []
        for i in range(self.h):
            self.tiles.append([]) #создаем строчки
            for j in range(self.w):
                self.tiles[i].append(Tile(value=randint(0,1)))

    def set_neighs(self):
        for line_count,line in enumerate(self.tiles):
            before_line = line_count-1
            next_line = line_count+1
            need_lines = [line_count]
            if before_line > 0: need_lines.append(before_line)
            if next_line < len(self.tiles): need_lines.append(next_line)

            for tile_count,tile in enumerate(line):
                
                before_tile = tile_count - 1
                next_tile = tile_count + 1
                need_tiles = [tile_count]
                if before_tile > 0: need_tiles.append(before_tile)
                if next_tile < len(line): need_tiles.append(next_tile)

                for line_index in need_lines:
                    for tile_index in need_tiles:
                        tile.add_neig(self.tiles[line_index][tile_index])

class GameScr(Screen):
    def __init__(self,w,h, name='game'):
        super().__init__(name=name)
        self.w = w
        self.h = h
        self.field = Fied(w, h)
        vertical_layout = BoxLayout(orientation='vertical')
        self.lines = []
        for i in range(h):
            layout = BoxLayout(orientation='horizontal')
            self.lines.append(layout)
            vertical_layout.add_widget(layout)
            for j in range(w):
                self.lines[i].add_widget(self.field.tiles[i][j].button)
                
        self.add_widget(vertical_layout)

    def restart_all(self):
        self.field.restart_field()

    def next(self):
        self.manager.transition.direction = 'left' 
        self.manager.current = 'restart'

class RestartScr(Screen):
    def __init__(self, name='restart'):
        super().__init__(name=name)
        btn = Button(text="начать игру")
        btn.on_press = self.next
        self.add_widget(btn)
        
    def next(self):
        game_screen = self.manager.get_screen('game')
        game_screen.restart_all()

        self.manager.transition.direction = 'right'
        self.manager.current = 'game'
        

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScr(10,10))
        sm.add_widget(RestartScr())
        sm.current = "restart"
        return sm

app = MyApp()
app.run()