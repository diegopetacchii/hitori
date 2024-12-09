from boardgame import BoardGame
from boardgamegui import gui_play
import g2d

CLAER=0
CIRCLED=1
BLACKED=2


class Hitori(BoardGame):

    #costruttore del gioco, valorizza varibili fondamentali dell oggetto
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

    #funzione per scorrere i livelli di gioco
    def level(self, level):
        l=["6-medium.csv", "8-hard.csv", 
        "9-veryhard.csv", "12-superhard.csv", "15-imppossible.csv"]
        
        gui_play(Hitori(l[level]))

        g2d.close_canvas()

    #funzione per gestire funzioni in base all'iput ricevuto
    def play(self, x: int, y: int, action: str):
        if action == "black":
            self.black(x, y)
        elif action == "flag":
            self.circle(x, y)
        elif action == "cerchia_adiacenti":
            self.cerchia_adiacenti(x, y)
        elif action == "annerisci_ripetizioni":
            self.annerisci_ripetizioni(x, y)

    #funzione per annerire i valori della lista
    def black(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            if self._annot[x + y * self._w] == 2:
                self._annot[x + y * self._w] = 0
            else:
                self._annot[x + y * self._w] = 2
    
    #funzione per cerhiare i valori della lista
    def circle(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            if self._annot[x + y * self._w] ==1:
                self._annot[x + y * self._w] = 0
            else:
                self._annot[x + y * self._w] = 1

    #legge i valori della lista e li passa a una funzione per la loro scrittura a schermo
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
    
    #ritorna il numero di righe della matrice
    def cols(self) -> int:
        return self._h
    
    #ritorna il numero di righe della tabella
    def rows(self) -> int:
        return self._w
    
    #controllo perhe tutte le regole siano rispettate per la vittoria 
    def finished(self) -> bool:

        if self.adiacenze()==True:
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
                    return False

        
        for y in range(self._h):
            row=[]
            for x in range(self._w):
                if self._annot[x+y*self._w]!=BLACKED:
                    row.append(self._bd[x+y*self._w])
            if self.has_repetition(row):
                return False

        for x in range(self._w):
            cols=[]
            for y in range(self._h):
                if self._annot[x+y*self._w]!=BLACKED:
                   cols.append(self._bd[x+y*self._w])
            if self.has_repetition(cols):
                return False

        #tutte le regole sono rispettate               
        return True
            
    #funzione per controllare se tutte le celle sono sollegate tra loro
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
    
    #controllo per le ripetizioni sia su riga che per colonna
    def has_repetition(self, list):
        seen=set()
        for v in list:
            if v in seen:
                return True
            seen.add(v)
        return False

    #scorre tutte le celle della lista per verificare adiacenze tra celle nere
    def adiacenze(self):
        for y in range(self._h):
            for x in range(self._w):
                if self.adiacenzaCella(x, y)==True:
                    return True
        return False

    #controlla se una cella e adiacente ad un altra cella nera in una delle 4 direzioni 
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
    
    #funzione per gestire automatismo cerchia celle adiacenti a una cella nera
    def cerchia_adiacenti(self, x, y):
        if 0 <= x < self._w and 0 <= y < self._h:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self._w and 0 <= ny < self._h:
                    self.auto_circle(nx, ny)

    #cerchia una cella
    def auto_circle(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            self._annot[x + y * self._w] = 1       
    
    #controlla se in una riga o colonna ci sono ripetizioni e in caso le annerisce
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

    #annerisce una singla cella 
    def auto_black(self, x: int, y: int):
        if 0 <= x < self._w and 0 <= y < self._h:
            self._annot[x + y * self._w] = 2

    #funzione per gestire tutti gli automatismi insieme su tutta la lista
    def h(self):
        initial_temp = list(self._annot)
        temp = self._annot
        
        for y in range(self._h):
            for x in range(self._w):
                if initial_temp[x + y * self._w] in {BLACKED, CIRCLED}:
                    if temp[x + y * self._w] == BLACKED:
                        self.cerchia_adiacenti(x, y)
                    elif temp[x + y * self._w] == CIRCLED:
                        self.annerisci_ripetizioni(x, y)

    #ritorna lo stato del gioco
    def status(self) -> str:
        if self.finished():
            return 'You win'
        else:
            return self.wrong()
    
    #funzione per controllare che errori impediscono la vittoria
    def wrong(self):

        if self.adiacenze()==True:
            return "Sono presenti adicenze"
            
        
        visited = [0] * (self._h * self._w)

        for y in range(self._h):
            for x in range(self._w):
                if self._annot[x + y * self._w] != BLACKED: 
                    self.fill(x, y, visited)
                    break

        for y in range(self._h):
            for x in range(self._w):
                idx = x + y * self._w
                if self._annot[idx] != BLACKED and visited[idx] == 0:
                    return ("non tutte le celle sono collegate")

        
        for y in range(self._h):
            row=[]
            for x in range(self._w):
                if self._annot[x+y*self._w]!=BLACKED:
                    row.append(self._bd[x+y*self._w])
            if self.has_repetition(row):
                return ("Sono presenti ripetizioni sulle righe")

        for x in range(self._w):
            cols=[]
            for y in range(self._h):
                if self._annot[x+y*self._w]!=BLACKED:
                   cols.append(self._bd[x+y*self._w])
            if self.has_repetition(cols):
                return("Sono presenti ripetizioni sulle colonne")
                                
        return ""

#funzione principale per avviare il gioco
def main():
    l="5-easy.csv"

    gui_play(Hitori(l))

    n=input()


if __name__ == '__main__':
    main()
