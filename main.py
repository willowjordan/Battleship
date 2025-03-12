import tkinter as tk
from battleshiplib import *

class TitleScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        PAD = 10
        BUTTONWIDTH = 40
        BUTTONHEIGHT = 7

        self.label = tk.Label(self, text="Battleship", font=('Arial', 18))
        self.localbutton = tk.Button(self, command=self.local_game, text="Play VS Computer", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        self.hostbutton = tk.Button(self, command=self.host_screen, text="Host Game", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        self.joinbutton = tk.Button(self, command=self.join_screen, text="Join Game", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        self.exitbutton = tk.Button(self, command=self.master.destroy, text="Quit", width=BUTTONWIDTH, height=BUTTONHEIGHT)

        self.label.pack(pady=PAD)
        self.localbutton.pack(pady=PAD)
        self.hostbutton.pack(pady=PAD)
        self.joinbutton.pack(pady=PAD)
        self.exitbutton.pack(pady=PAD)
    
    def local_game(self):
        self.master.player = LocalPlayer()
        self.master.opponent = ComputerPlayer()
        self.master.next_frame = GameScreen(self.master)
        self.master.display_next()
    
    def host_screen(self):
        self.master.next_frame = HostScreen(self.master)
        self.master.display_next()
    
    def join_screen(self):
        pass

class HostScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        PAD = 10
        BUTTONWIDTH = 40
        BUTTONHEIGHT = 7

        self.label = tk.Label(self, text="Host a Game...", font=('Arial', 18))
        self.lobbynamelabel = tk.Label(self, text="Lobby Name: ")
        self.lobbyname = tk.Text(self, height=3, bg="white", fg="black")
        self.displaynamelabel = tk.Label(self, text="Display Name: ")
        self.displayname = tk.Text(self, height=3, bg="white", fg="black")
        self.startbutton = tk.Button(self, command=self.createLobby, text="Start Lobby", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        self.backbutton = tk.Button(self, command=self.back, text="Back", width=BUTTONWIDTH, height=BUTTONHEIGHT)

        self.label.grid(row=1, column=1, columnspan=2)
        self.lobbynamelabel.grid(row=2, column=1)
        self.lobbyname.grid(row=2, column=2)
        self.displaynamelabel.grid(row=3, column=1)
        self.displayname.grid(row=3, column=2)
        self.startbutton.grid(row=4, column=1, columnspan=2)
        self.backbutton.grid(row=5, column=1, columnspan=2)
    
    def createLobby(self):
        pass
    
    def back(self):
        self.master.next_frame = TitleScreen(self.master)
        self.master.display_next()

class JoinScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

# container representing the main interactive area (primary grid and targeting grid)
class GameScreen(tk.Canvas):
    def __init__(self, master):
        super().__init__(height=800, width=800)
        self.master = master
        
        # create frames
        self.info_frame = tk.Frame(self, bg="gray")
        self.create_window(0, 0, window=self.info_frame, anchor="nw", width=200, height=800)
        self.targeting_frame = tk.Frame(self, bg="red")
        self.create_window(200, 0, window=self.targeting_frame, anchor="nw", width=400, height=400)
        self.primary_frame = tk.Frame(self, bg="blue")
        self.create_window(200, 400, window=self.primary_frame, anchor="nw", width=400, height=400)
        self.enemyships_frame = tk.Frame(self, bg="gray")
        self.create_window(600, 0, window=self.enemyships_frame, anchor="nw", width=200, height=400)
        self.myships_frame = tk.Frame(self, bg="lightgray")
        self.create_window(600, 400, window=self.myships_frame, anchor="nw", width=200, height=400)
        
        # TODO: add elements to specific frames
        
        


# main game object
class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Battleship")

        self.current_frame = None # current frame being displayed
        self.next_frame = TitleScreen(self) # next frame to be displayed
        self.display_next()

    def title_screen(self):
        ts = TitleScreen(self)
        ts.pack()

    def host_screen(self):
        hs = HostScreen(self)
        hs.pack()

    def join_screen(self):
        js = JoinScreen(self)
        js.pack()

    # destroy current frame and display next
    def display_next(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = self.next_frame
        self.current_frame.pack()
        self.next_frame = None



if __name__ == "__main__":
    game = Game()
    game.mainloop()