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
        self.master.next_screen = GameScreen(self.master, LocalPlayer(), ComputerPlayer())
        self.master.display_next()
    
    def host_screen(self):
        self.master.next_screen = HostScreen(self.master)
        self.master.display_next()
    
    def join_screen(self):
        pass #TODO: complete this

class HostScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

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
        pass #TODO: complete this
    
    def back(self):
        self.master.next_screen = TitleScreen(self.master)
        self.master.display_next()

class JoinScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

# container representing the main interactive area (primary grid and targeting grid)
class GameScreen(tk.Canvas):
    def __init__(self, master, player, opponent):
        super().__init__(master, width=800, height=800, bd=0, highlightthickness=0, relief='ridge')
        self.master = master
        self.player = player
        self.opponent = opponent

        # create PhotoImages
        self.ocean = tk.PhotoImage(file="assets/ocean.png")
        self.radar = tk.PhotoImage(file="assets/radar.png")

        self.drawBackground()
    
    # draw things that won't change
    def drawBackground(self):
        # component backgrounds
        self.create_rectangle(0, 0, 200, 800, fill="lightgray", width=0) # info sidebar
        self.create_image(200, 0, image=self.ocean, anchor="nw") # targeting and primary grid background
        self.create_rectangle(600, 0, 800, 400, fill="lightgray", width=0) # enemy ships
        self.create_rectangle(600, 400, 800, 800, fill="lightgray", width=0) # your ships

        # lines separating components
        self.create_line(200, 0, 200, 800, width=2)
        self.create_line(600, 400, 800, 400, width=2)
        self.create_line(600, 0, 600, 800, width=2)

        # targeting grid
        self.create_text(400, 25, anchor="center", text="Targeting Grid", fill="lightgreen", font=("Helvetica", "16"))
        self.create_image(250, 50, image=self.radar, anchor="nw")
        self.create_line(250, 50, 550, 50, fill="green", width=1)
        self.create_line(550, 50, 550, 350, fill="green", width=1)
        self.create_line(550, 350, 250, 350, fill="green", width=1)
        self.create_line(250, 350, 250, 50, fill="green", width=1)

        # primary grid
        self.create_text(400, 425, anchor="center", text="Primary Grid", fill="lightgreen", font=("Helvetica", "16"))
        self.create_image(250, 450, image=self.radar, anchor="nw")
        self.create_line(250, 450, 550, 450, fill="green", width=1)
        self.create_line(550, 450, 550, 750, fill="green", width=1)
        self.create_line(550, 750, 250, 750, fill="green", width=1)
        self.create_line(250, 750, 250, 450, fill="green", width=1)
    
    # draw a 10x10 grid with the NW corner at (x, y) of size x size using lines of color and thickness
    '''def drawGrid(self, x, y, size, color, thickness):
        # vert
        for i in range(0, 11):
            realx = x + int(size * (i/10))
            self.create_line(realx, y, realx, y+size, fill=color, width=thickness)
        # horiz
        for i in range(0, 11):
            realy = y + int(size * (i/10))
            self.create_line(x, realy, x+size, realy, fill=color, width=thickness)'''
    
    # draw functions
    def drawSidebar(self):
        pass

    def drawTargetingGrid(self):
        pass

    def drawPrimaryGrid(self):
        pass

    def drawEnemyShips(self):
        pass

    def drawMyShips(self):
        pass

    # inner frame classes
    '''class InfoSidebar(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="gray")
            self.master = master

    class TargetingGrid(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="red")
            self.master = master
            self.player = master.player

    class PrimaryGrid(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="blue")
            self.master = master

    class EnemyShips(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="gray")
            self.master = master

    class MyShips(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="lightgray")
            self.master = master'''
        

# main game object
class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Battleship")

        self.current_screen = None # current frame being displayed
        self.next_screen = TitleScreen(self) # next frame to be displayed
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
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = self.next_screen
        self.current_screen.pack()
        self.next_screen = None



if __name__ == "__main__":
    #game = Game()
    #game.mainloop()
    root = tk.Tk()
    game = GameScreen(root, LocalPlayer(), ComputerPlayer())
    game.pack()
    root.mainloop()