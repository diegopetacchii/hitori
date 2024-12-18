#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

try:
    from __main__ import g2d
except:
    import g2d
from boardgame import BoardGame

W, H = 40, 40
counterLevel=-1
l=["6-medium.csv", "8-hard.csv", 
    "9-veryhard.csv", "12-superhard.csv", "15-imppossible.csv"]

class BoardGameGui:
    def __init__(self, game: BoardGame):
        self._game = game
        self.update_buttons()

    def tick(self):
        global counterLevel
        game = self._game
        mouse_x, mouse_y = g2d.mouse_pos()
        x, y = mouse_x // W, mouse_y // H
        released = set(g2d.previous_keys()) - set(g2d.current_keys())
        if game.finished():
            g2d.alert(game.status())

            counterLevel+=1
            
            if(counterLevel==6):
                g2d.close_canvas()

            g2d.alert("Next level: "+str(l[counterLevel]))           
            game.level(counterLevel)

            
        elif "Escape" in released: 
            g2d.close_canvas()
        elif "LeftButton" in released and y < game.rows():
            game.play(x, y, "black")
            self.update_buttons((x, y))
        elif "RightButton" in released and y < game.rows():
            if "#" in game.read(x, y):
                game.play(x, y, "cerchia_adiacenti")
                self.update_buttons((x, y))
            elif "!" in game.read(x, y):
                game.play(x, y, "annerisci_ripetizioni")
                self.update_buttons((x, y))
            else:
                game.play(x, y, "flag")
                self.update_buttons((x, y))
        elif "h" in released:
            game.h()
            self.update_buttons()
            

    def update_buttons(self, last_move=None):
        cols, rows = self._game.cols(), self._game.rows()
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), (cols * W, rows * H + H))
        for y in range(rows):
            for x in range(cols):
                gray = 232 if (x, y) == last_move else 255
                text = self._game.read(x, y)
                _write(text, (x, y), bg=(gray, gray, gray))
        status = self._game.status()
        _write(status, (0, rows), cols)
        
def _write(text, pos, cols=1, bg=(255, 255, 255)):
    x, y = pos
    g2d.set_color(bg)
    g2d.draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
    
    chars = max(1, len(text))
    fsize = min(0.75 * H, 1.5 * cols * W // (chars))
    center = (x * W + cols * W/2, y * H + H/2)

    if "#" in text:
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
        g2d.set_color((0, 0, 0))
        text = text.replace("#", "")
        g2d.set_color((255, 255, 255))
        g2d.draw_text(text, center, fsize)

    elif "!" in text:
        text = text.replace("!", "")
        g2d.set_color((255, 255, 255))
        g2d.draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
        
        g2d.set_color((0, 0, 0))
        circle_center = (x * W + W / 2, y * H + H / 2)
        circle_radius = min(W, H) // 2 
        g2d.draw_circle(circle_center, circle_radius)

        g2d.set_color((255, 255, 255))
        g2d.draw_circle(circle_center, circle_radius - 3)

        g2d.set_color((0, 0, 0))
        g2d.draw_text(text, circle_center, fsize)

    else:
        g2d.set_color((0, 0, 0))
        g2d.draw_text(text, center, fsize)
        

def gui_play(game: BoardGame):

    g2d.init_canvas((game.cols() * W, game.rows() * H + H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
