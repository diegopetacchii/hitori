from boardgame import BoardGame
from boardgamegui import gui_play


class RotationGame(BoardGame):
    def __init__(self, w,  h):
        self._w=w
        self._h=h
        self._bd=[1]*(w*h)
        self._n=max(w, h)+1


    def play(self, x: int, y: int, action: str):
        if 0 <= x < self._w and 0 <= y < self._h:
            v = self._bd[x + y * self._w]
            if v == self._n - 1:  
                self._bd[x + y * self._w] = 1
            else:
                self._bd[x + y * self._w] = v + 1
    
    def read(self, x: int, y: int):
        if 0<=x<self._w and 0<=y<self._h:
            v=self._bd[x+y*self._w]
            
            return str(v)
        else:
            return ' '
        
    def cols(self) -> int:
        return self._h
    
    def rows(self) -> int:
        return self._w

    def finished(self) -> bool:
        

        for y in range(self._h):
            row=[]
            for x in range(self._w):
                row.append(self._bd[x+y*self._w])
            if self.has_repetittion(row):
                return False

        for x in range(self._w):
            cols=[]
            for y in range(self._h):
                cols.append(self._bd[x+y*self._w])
            if self.has_repetittion(cols):
                return False
            

        if all(self._bd):
            return True
        else:
            return False
    
    def has_repetittion(self, list):
        seen=set()
        for v in list:
            if v in seen:
                return True
            seen.add(v)
        return False


    def status(self) -> str:
        return 'Game over!'
    
gui_play(RotationGame(4, 4))