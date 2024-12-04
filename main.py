from boardgame import BoardGame
from boardgamegui import gui_play


CLEAR=1
BLACK=2


class Hitori(BoardGame):
    def __init__(self, filename):
        
        self._bd = []
        self._h=0
        self._w=0

        with open(filename, "r") as f:
            row=[]
            for x in f:
                x=x.strip()
                row=x.split(',')

                int_values = [int(value) for value in row]
                self._bd.extend(int_values)

                self._w+=1
                if self._h == 0:  
                    self._h = len(int_values)

        self._annot=[0]*(self._h*self._w)
        print(self._annot)

    def play(self, x: int, y: int, action: str):
        if action == "black":
            self.black(x, y)
        elif action == "flag":
            self.circle(x, y)
        """elif action == "cerchia_adiacenti" and "#" in self._bd[x + y * self._w]:
            self.cerchia_adiacenti(x, y)"""

    def black(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            v = self._bd[x + y * self._w]
            if "#" in str(v):
                v = int(v.replace("#", ""))
                self._bd[x + y * self._w] = str(v)
                self._annot[x + y * self._w] = 0
            elif "!" not in str(v):
                self._bd[x + y * self._w] = str(v)+"#"
                self._annot[x + y * self._w] = 2
    
    def circle(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            v = self._bd[x + y * self._w]
            if "!" in str(v):
                v = int(v.replace("!", ""))
                self._bd[x + y * self._w] = str(v)
            elif "#" not in str(v):
                self._bd[x + y * self._w] = str(v)+"!"


    def read(self, x: int, y: int):
        if 0<=x<self._w and 0<=y<self._h:
            v=self._bd[x+y*self._w]
            #if self.adiacenzaCella(x, y)==True:
                #return str(v)+"!"
            return str(v)
        else:
            return ' '
        
    def cols(self) -> int:
        return self._h
    
    def rows(self) -> int:
        return self._w

    """def finished(self) -> bool:

        if self.adiacenze()==True:
            print("presenti adicenze")
            return False
        
        self._annot = [0] * (self._h * self._w)
        for y in range(self._h): 
            for x in range(self._w): 
                if self._annot[x + y * self._w] == 0 and "#" not in str(self._bd[x + y * self._w]): 
                   self.fill(x, y) 
                   break 
            if 1 in self._annot: 
                break

        

        for y in range(self._h): 
            for x in range(self._w): 
                if self._annot[x + y * self._w] == 0 and "#" not in str(self._bd[x + y * self._w]): 
                    print("celle non collegate")
                    return False        


        for y in range(self._h):
            row=[]
            for x in range(self._w):
                if not("#" in str(self._bd[x+y*self._w])):
                    row.append(self._bd[x+y*self._w])
            if self.has_repetittion(row):
                print("ripetizioni su righe")
                return False



        for x in range(self._w):
            cols=[]
            for y in range(self._h):
                if not("#" in str(self._bd[x+y*self._w])):
                    cols.append(self._bd[x+y*self._w])
            if self.has_repetittion(cols):
                print("ripetizioni su colonne")
                return False
            
        return True"""
    
    def finished(self) -> bool:

        if self.adiacenze()==True:
            print("presenti adicenze")
            return False
        
        self._annot = [0] * (self._h * self._w)
        self.fill(0, 0) 
        if all(self._annot)==False:
            print("non tutte collegate")
            return False
        else:

            for y in range(self._h):
                row=[]
                for x in range(self._w):
                    if not("#" in str(self._bd[x+y*self._w])):
                        row.append(self._bd[x+y*self._w])
                if self.has_repetittion(row):
                    print("ripetizioni su righe")
                    return False

            for x in range(self._w):
                cols=[]
                for y in range(self._h):
                    if not("#" in str(self._bd[x+y*self._w])):
                        cols.append(self._bd[x+y*self._w])
                if self.has_repetittion(cols):
                    print("ripetizioni su colonne")
                    return False
                                
            return True
            

    def fill(self, x, y):
        bd, w, h = self._annot, self._w, self._h
        if 0 <= x < w and 0 <= y < h and bd[x + y * w] == 0:
            bd[x + y * w] = 1
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                if 0 <= x + dx < w and 0 <= y + dy < h and "#" not in str(self._bd[(x + dx) + (y + dy) * w]):
                    self.fill(x + dx, y + dy)
    
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
                    return True
        return False

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
    
    """def cerchia_adiacenti(self, x, y):
        if 0 <= x < self._w and 0 <= y < self._h:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._w and 0 <= ny < self._h:
                    self.circle(nx, ny)"""


    def status(self) -> str:
        if self.finished():
            return 'You win'
        else:
            return 'Playing...'

gui_play(Hitori("5-easy.csv"))
