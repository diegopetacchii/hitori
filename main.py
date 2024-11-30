from boardgame import BoardGame
from boardgamegui import gui_play

bdTable=[3,1,3,4,4,5,4,2,3,3,3,2,4,2,1,3,3,1,5,3,1,2,4,3,5]

class RotationGame(BoardGame):
    def __init__(self, w,  h):
        self._w=w
        self._h=h
        self._bd=bdTable   #[1]*(w*h)
        self._n=max(w, h)+1


    def play(self, x: int, y: int, action: str):
        if 0 <= x < self._w and 0 <= y < self._h:
            v = self._bd[x + y * self._w]
            if "#" in str(v):
                v = int(v.replace("#", ""))
                self._bd[x + y * self._w] = str(v)
            else:
                self._bd[x + y * self._w] = str(v)+"#"
    
    def read(self, x: int, y: int):
        if 0<=x<self._w and 0<=y<self._h:
            v=self._bd[x+y*self._w]
            if self.adiacenzaCella(x, y)==True:
                return str(v)+"!"
            return str(v)
        else:
            return ' '
        
    def cols(self) -> int:
        return self._h
    
    def rows(self) -> int:
        return self._w

    def finished(self) -> bool:
        
        if self.adiacenze()==True:
            for y in range(self._h):
                row=[]
                for x in range(self._w):
                    if not("#" in str(self._bd[x+y*self._w])):
                        row.append(self._bd[x+y*self._w])
                if self.has_repetittion(row):
                    return False

            for x in range(self._w):
                cols=[]
                for y in range(self._h):
                    if not("#" in str(self._bd[x+y*self._w])):
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

    def adiacenze(self):
        for y in range(self._h):
            for x in range(self._w):
                if self.adiacenzaCella(x, y)==True:
                    return False
        return True

    def adiacenzaCella(self, x, y):
        idx = x + y * self._w  
        if "#" in str(self._bd[idx]):
            if x + 1 < self._w and "#" in str(self._bd[idx + 1]):
                return True
            if x - 1 >= 0 and "#" in str(self._bd[idx - 1]):
                return True
            if y + 1 < self._h and "#" in str(self._bd[idx + self._w]):
                return True
            if y - 1 >= 0 and "#" in str(self._bd[idx - self._w]):
                return True
        return False

    def status(self) -> str:
        if self.finished():
            return 'You win'
        else:
            return 'Playing...'
    
gui_play(RotationGame(5, 5))