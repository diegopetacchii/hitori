from boardgame import BoardGame
from boardgamegui import gui_play

CLAER=0
CIRCLED=1
BLACKED=2


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

                self._h+=1
                if self._w == 0:  
                    self._w = len(int_values)

        self._annot=[0]*(self._h*self._w)
        #print(self._annot)

    def play(self, x: int, y: int, action: str):
        if action == "black":
            self.black(x, y)
        elif action == "flag":
            self.circle(x, y)
        elif action == "cerchia_adiacenti":
            self.cerchia_adiacenti(x, y)
        elif action == "annerisci_ripetizioni":
            self.annerisci_ripetizioni(x, y)

        
    def black(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            if self._annot[x + y * self._w] == 2:
                self._annot[x + y * self._w] = 0
            else:
                self._annot[x + y * self._w] = 2
        #print(self._annot)
    
    def circle(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            if self._annot[x + y * self._w] ==1:
                self._annot[x + y * self._w] = 0
            else:
                self._annot[x + y * self._w] = 1
        #print(self._annot)

    def read(self, x: int, y: int):
        if 0<=x<self._w and 0<=y<self._h:
            v=self._bd[x+y*self._w]
            if self._annot[x+y*self._w]==CIRCLED:
                return str(v) + "!"
            elif self._annot[x+y*self._w]==BLACKED:
                return str(v) + "#"
            return str(v)
        else:
            return ' '
        
    def cols(self) -> int:
        return self._h
    
    def rows(self) -> int:
        return self._w
    
    def finished(self) -> bool:

        if self.adiacenze()==True:
            #print("presenti adicenze")
            return False
        
        visited = [0] * (self._h * self._w)

        # Trova una cella iniziale non annerita
        for y in range(self._h):
            for x in range(self._w):
                if self._annot[x + y * self._w] != BLACKED: 
                    self.fill(x, y, visited)
                    break

        # Verifica che tutte le celle non annerite siano state visitate
        for y in range(self._h):
            for x in range(self._w):
                idx = x + y * self._w
                if self._annot[idx] != BLACKED and visited[idx] == 0:
                    # Cella non annerita non visitata -> non tutte le celle sono collegate
                    #print("non tutte le celle sono collegate")
                    return False

        
        for y in range(self._h):
            row=[]
            for x in range(self._w):
                if self._annot[x+y*self._w]!=BLACKED:
                    row.append(self._bd[x+y*self._w])
            if self.has_repetittion(row):
                #print("ripetizioni su righe")
                return False

        for x in range(self._w):
            cols=[]
            for y in range(self._h):
                if self._annot[x+y*self._w]!=BLACKED:
                   cols.append(self._bd[x+y*self._w])
            if self.has_repetittion(cols):
                #print("ripetizioni su colonne")
                return False
                                
        return True
            

    def fill(self, x, y, visited):
        w, h = self._w, self._h
        idx = x + y * w
        if not (0 <= x < w and 0 <= y < h):
            return
        if visited[idx] == 1 or self._annot[idx] == BLACKED:
            return

        visited[idx] = 1

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            self.fill(x + dx, y + dy, visited)
    
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
        if self._annot[idx] == 2:
            if x + 1 < self._w and  self._annot[idx + 1] == 2:
                return True
            if x - 1 >= 0 and self._annot[idx - 1] == 2:
                return True
            if y + 1 < self._h and self._annot[idx + self._w] == 2:
                return True
            if y - 1 >= 0 and self._annot[idx - self._w] == 2:
                return True
        return False
    
    def cerchia_adiacenti(self, x, y):
        if 0 <= x < self._w and 0 <= y < self._h:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._w and 0 <= ny < self._h:
                    self.auto_circle(nx, ny)

    def auto_circle(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            self._annot[x + y * self._w] = 1       
    
    def annerisci_ripetizioni(self, x, y):
        seen = set()
        y_index = y * self._w
        for x1 in range(self._w): 
            index = y_index + x1
            if self._annot[index]!= BLACKED:
                val = self._bd[index]
                if val in seen:
                    self.auto_black(x1, y)
                else:
                    seen.add(val)
        
        seen = set()
        for y1 in range(self._h): 
            index = y1 * self._w + x
            if self._annot[index]!=BLACKED:
                val = self._bd[index]
                if val in seen:
                    self.auto_black(x, y1)
                else:
                    seen.add(val)

    def auto_black(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            self._annot[x + y * self._w] = 2
        #print(self._annot)

    def status(self) -> str:
        if self.finished():
            return 'You win'
        else:
            return 'Playing...'

def main():
    l=["5-easy.csv", "6-medium.csv", "7-hard.csv", "8-hard.csv", 
       "9-veryhard.csv", "12-superhard.csv", "15-imppossible.csv",]

    for x in l:
        gui_play(Hitori(x))


if __name__ == '__main__':
    main()