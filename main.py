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
        self.player:Player = player
        self.opponent:Player = opponent
        self.turn:Player = player # whose turn it is
        self.game_phase:str = "Setup"

        # create PhotoImages
        self.ocean = tk.PhotoImage(file="assets/ocean.png")
        self.radar = tk.PhotoImage(file="assets/radar.png")

        # constants
        self.PBOARD_X = 250
        self.PBOARD_Y = 450
        self.PBOARD_SPACE = 30 # width of one space on the board

        self.drawBackground()

        self.master.bind("<Key>", self.onKeyPress)
        self.bind("<Button-1>", self.onClick)


    
    ''' DRAWING FUNCTIONS '''
    # draw things that won't change
    def drawBackground(self):
        # component backgrounds
        self.create_image(200, 0, image=self.ocean, anchor="nw") # targeting and primary grid background
        self.create_rectangle(600, 0, 800, 400, fill="lightblue", width=0) # enemy ships
        self.create_rectangle(600, 400, 800, 800, fill="lightblue", width=0) # your ships

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

        # ship graveyard constants
        PAD_X = 25
        PAD_Y = 50

        # enemy ships
        self.create_text(700, 25, anchor="center", text="Enemy Ships", fill="black", font=("Helvetica", "16"))
        self.drawShip(600+PAD_X, 50, 5)
        self.drawShip(600+PAD_X, 50+PAD_Y, 4)
        self.drawShip(600+PAD_X, 50+2*PAD_Y, 3)
        self.drawShip(600+PAD_X, 50+3*PAD_Y, 3)
        self.drawShip(600+PAD_X, 50+4*PAD_Y, 2)

        # friendly ships
        self.create_text(700, 425, anchor="center", text="Your Ships", fill="black", font=("Helvetica", "16"))
        self.drawShip(600+PAD_X, 450, 5)
        self.drawShip(600+PAD_X, 450+PAD_Y, 4)
        self.drawShip(600+PAD_X, 450+2*PAD_Y, 3)
        self.drawShip(600+PAD_X, 450+3*PAD_Y, 3)
        self.drawShip(600+PAD_X, 450+4*PAD_Y, 2)

        self.sidebar = self.InfoSidebar(self)
        self.create_window(0, 0, width=200, height=800, anchor="nw", window=self.sidebar)
    
    def drawShip(self, x, y, length, vertical=False, color="gray", tags=None):
        """
        drawShip draws a ship consisting of 30px by 30px squares

        :param x: x location of NW corner of ship 
        :param y: y location of NW corner of ship
        :param length: length of ship in squares
        :param vertical: draw ship vertically if true, horizontally if false
        :param color: color of ship
        :param tags: tags to be included in all shapes used to draw the ship
        """

        if not vertical:
            # colored backdrop
            self.create_rectangle(x, y, x+30*length, y+30, fill=color, tags=tags)

            # border lines
            self.create_line(x, y, x+30*length, y, width=2, tags=tags)
            self.create_line(x, y+30, x+30*length, y+30, width=2, tags=tags)
            self.create_line(x, y, x, y+30, width=2, tags=tags)
            self.create_line(x+30*length, y, x+30*length, y+30, width=2, tags=tags)

            # inside lines
            for i in range(1, length):
                newX = x + 30 * i
                self.create_line(newX, y, newX, y+30, width=1, tags=tags)
        else:
            # colored backdrop
            self.create_rectangle(x, y, x+30, y+30*length, fill=color, tags=tags)

            # border lines
            self.create_line(x, y, x, y+30*length, width=2, tags=tags)
            self.create_line(x+30, y, x+30, y+30*length, width=2, tags=tags)
            self.create_line(x, y, x+30, y, width=2, tags=tags)
            self.create_line(x, y+30*length, x+30, y+30*length, width=2, tags=tags)

            # inside lines
            for i in range(1, length):
                newY = y + 30 * i
                self.create_line(x, newY, x+30, newY, width=1, tags=tags)
    
    def drawShipObject(self, ship:Ship, color="gray", tags=None):
        """
        drawShipObject draws a Ship object on the primary board consisting of 30px by 30px squares

        :param ship: the Ship object to be drawn
        :param color: color of ship
        :param tags: tags to be included in all shapes used to draw the ship
        """
        
        x = self.PBOARD_X + self.PBOARD_SPACE * ship.spaces[0][0]
        y = self.PBOARD_Y + self.PBOARD_SPACE * ship.spaces[0][1]
        vertical = ship.direction[0] == 0
        self.drawShip(x, y, ship.length, vertical, color=color, tags=tags)

    # inner frame classes
    class InfoSidebar(tk.Frame):
        def __init__(self, master):
            super().__init__(bg="lightblue")
            self.master = master
            self.labels:dict[str, tk.Label] = {}

            self.labels["turninfo"] = tk.Label(self, text="Your Turn", bg="lightblue", font=("Helvetica", "16"))
            self.labels["instructions"] = tk.Label(self, text="Place Your Ships\nUse arrow keys to move the ship\nPress Space to rotate\nPress Enter to confirm", bg="lightblue")
            self.labels["lobbyinfoheader"] = tk.Label(self, text="Lobby Info:", bg="lightblue", font=("Helvetica", "16"))
            self.labels["lobbyinfo"] = tk.Label(self, text="Game Type: Local", bg="lightblue")
            self.labels["opponentinfo"] = tk.Label(self, text="Opponent: CPU", bg="lightblue")

            for lb in self.labels.values():
                lb.pack()
        
        # change the turn info label to display newTxt
        def changeLabel(self, labelname, newTxt):
            self.labels[labelname].configure(text=newTxt)
            self.labels[labelname].update()
    
    ''' SETUP PHASE '''
    def initializeSetupPhase(self):
        self.shipToPlace = Ship([0, 0], 5, [1, 0])
        self.drawShipObject(self.shipToPlace, "lightgray", "shipToPlace")
    
    # TODO: add out of bounds checking/ ship in the way checking
    def moveSetupShip(self, transVector):
        self.shipToPlace.translate(transVector)
        self.delete("shipToPlace")
        self.drawShipObject(self.shipToPlace, "lightgray", "shipToPlace")
            
    
    ''' INPUT HANDLING FUNCTIONS '''
    def onKeyPress(self, event):
        if self.turn != self.player: return # ignore input during opponent's turn

        if self.game_phase == "Setup":
            if event.keysym == "Up": self.moveSetupShip([0, -1])
            elif event.keysym == "Down": self.moveSetupShip([0, 1])
            elif event.keysym == "Left": self.moveSetupShip([-1, 0])
            elif event.keysym == "Right": self.moveSetupShip([1, 0])
            elif event.keysym == "space":
                pass
            elif event.keysym == "Return":
                pass
            print(event)

    def onClick(self, event):
        if self.turn != self.player: return # ignore input during opponent's turn

        print(event.x)
        
        

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