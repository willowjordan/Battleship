"""
BUGS:
    - clicking during opponent's turn "buffers" a click (may be unfixable, but could maybe use threading)
    - with slow CPU, last player ship placement lags until response from CPU is received
FEATURES TO ADD:
    - implement intermediate and advanced CPUs
    - implement multiplayer
"""

import tkinter as tk
import copy

from player import * # includes Player, CPU, Board, Ship, etc

# UI CONSTANTS
BG_COLOR = "lightblue"
BUTTON_WIDTH = 40
BUTTON_HEIGHT = 7
PAD = 10
UI_FONT = ('Arial', 18)
GAME_FONT = ('Helvetica', 16)

class TitleScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(background = BG_COLOR)
        self.master = master

        self.label = tk.Label(self, text="Battleship", font=UI_FONT, background=BG_COLOR)
        self.localbutton = tk.Button(self, command=self.local_game, text="Play VS Computer", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.hostbutton = tk.Button(self, command=self.host_screen, text="Host Game", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.joinbutton = tk.Button(self, command=self.join_screen, text="Join Game", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.exitbutton = tk.Button(self, command=self.master.destroy, text="Quit", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.label.pack(pady=PAD)
        self.localbutton.pack(pady=PAD)
        self.hostbutton.pack(pady=PAD)
        self.joinbutton.pack(pady=PAD)
        self.exitbutton.pack(pady=PAD)
    
    def local_game(self):
        self.master.display(CPUPregameScreen(self.master))
    
    def host_screen(self):
        self.master.display(HostScreen(self.master))
    
    def join_screen(self):
        self.master.display(JoinScreen(self.master))

class CPUPregameScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(background=BG_COLOR)
        self.master = master

        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.d_selection = tk.StringVar()
        self.speed_options = ["Slow", "Fast"]
        self.s_selection = tk.StringVar()

        self.label = tk.Label(self, text="CPU Settings", font=UI_FONT, background = BG_COLOR)
        self.difficultylabel = tk.Label(self, text="Difficulty: ", background = BG_COLOR)
        self.difficulty = tk.OptionMenu(self, self.d_selection, *self.difficulty_options)
        self.speedlabel = tk.Label(self, text="Speed: ", background = BG_COLOR)
        self.speed = tk.OptionMenu(self, self.s_selection, *self.speed_options)
        self.startbutton = tk.Button(self, command=self.start, text="Start Game", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.backbutton = tk.Button(self, command=self.back, text="Back", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.label.grid(row=1, column=1, columnspan=2, pady=PAD)
        self.difficultylabel.grid(row=2, column=1, pady=PAD)
        self.difficulty.grid(row=2, column=2, pady=PAD)
        self.speedlabel.grid(row=3, column=1, pady=PAD)
        self.speed.grid(row=3, column=2, pady=PAD)
        self.startbutton.grid(row=5, column=1, columnspan=2, pady=PAD)
        self.backbutton.grid(row=6, column=1, columnspan=2, pady=PAD)
    
    def start(self):
        errormsg = ""

        s = self.s_selection.get()
        if s == "Slow": slow = True
        elif s == "Fast": slow = False
        else: errormsg += "Please select a speed value.\n"; slow = None

        d = self.d_selection.get()
        if d == "Easy": cpu = RandomCPU(slow)
        elif d == "Medium": cpu = IntermediateCPU(slow)
        elif d == "Hard": cpu = AdvancedCPU(slow)
        else: errormsg += "Please select a difficulty value.\n"

        if errormsg == "": # no errors
            self.master.display(GameScreen(self.master, ComputerPlayer(cpu)))
        else:
            if hasattr(self, 'errorlabel'):
                self.errorlabel.configure(text=errormsg)
            else:
                self.errorlabel = tk.Label(self, text=errormsg, font=UI_FONT, background = BG_COLOR, foreground="red")
                self.errorlabel.grid(row=4, column=1, columnspan=2)

    def back(self):
        self.master.display(TitleScreen(self.master))

class HostScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(background=BG_COLOR)
        self.master = master

        self.label = tk.Label(self, text="Host a Game...", font=UI_FONT, background = BG_COLOR)
        self.lobbynamelabel = tk.Label(self, text="Lobby Name: ", background = BG_COLOR)
        self.lobbyname = tk.Text(self, height=3, bg="white", fg="black")
        self.displaynamelabel = tk.Label(self, text="Display Name: ", background = BG_COLOR)
        self.displayname = tk.Text(self, height=3, bg="white", fg="black")
        self.startbutton = tk.Button(self, command=self.createLobby, text="Start Lobby", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.backbutton = tk.Button(self, command=self.back, text="Back", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.label.grid(row=1, column=1, columnspan=2)
        self.lobbynamelabel.grid(row=2, column=1)
        self.lobbyname.grid(row=2, column=2)
        self.displaynamelabel.grid(row=3, column=1)
        self.displayname.grid(row=3, column=2)
        self.startbutton.grid(row=4, column=1, columnspan=2)
        self.backbutton.grid(row=5, column=1, columnspan=2)
    
    def createLobby(self):
        self.master.display(LobbyScreen(self.master))
    
    def back(self):
        self.master.display(TitleScreen(self.master))

# TODO: implement
class LobbyScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        raise NotImplementedError("Lobby screen is not implemented yet")

# TODO: implement
class JoinScreen(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        raise NotImplementedError("Join screen is not implemented yet")

class GameScreen(tk.Canvas):
    """Container representing the main interactive area (primary grid and targeting grid)"""
    def __init__(self, master, opponent):
        super().__init__(master, width=800, height=800, bd=0, highlightthickness=0, relief='ridge')
        self.master = master
        self.board = Board() # local player's board
        self.opponent:Player = opponent
        self.myturn:bool = True # true if local player's turn, false otherwise
        self.game_phase:str = "Setup"

        # create PhotoImages
        self.ocean = tk.PhotoImage(file="assets/ocean.png")
        self.radar = tk.PhotoImage(file="assets/radar.png")

        # primary board constants
        self.PBOARD_X = 250
        self.PBOARD_Y = 450
        self.PBOARD_SPACE = 30 #width/height of one space
        # targeting board constants
        self.TBOARD_X = 250
        self.TBOARD_Y = 50
        self.TBOARD_SPACE = 30 #width/height of one space

        self.drawBackground()

        self.master.bind("<Key>", self.onKeyPress)
        self.bind("<Button-1>", self.onClick)

        self.initializeSetupPhase()
    
    ### DRAWING FUNCTIONS ###
    def drawBackground(self):
        """Draw things that won't change"""
        # component backgrounds
        self.create_image(200, 0, image=self.ocean, anchor="nw") # targeting and primary grid background
        self.create_rectangle(600, 0, 800, 400, fill=BG_COLOR, width=0) # enemy ships
        self.create_rectangle(600, 400, 800, 800, fill=BG_COLOR, width=0) # your ships

        # lines separating components
        self.create_line(200, 0, 200, 800, width=2)
        self.create_line(600, 400, 800, 400, width=2)
        self.create_line(600, 0, 600, 800, width=2)

        # targeting grid
        self.create_text(400, 25, anchor="center", text="Targeting Grid", fill="lightgreen", font=GAME_FONT)
        self.create_image(250, 50, image=self.radar, anchor="nw")
        self.create_line(250, 50, 550, 50, fill="green", width=1)
        self.create_line(550, 50, 550, 350, fill="green", width=1)
        self.create_line(550, 350, 250, 350, fill="green", width=1)
        self.create_line(250, 350, 250, 50, fill="green", width=1)

        # primary grid
        self.create_text(400, 425, anchor="center", text="Primary Grid", fill="lightgreen", font=GAME_FONT)
        self.create_image(250, 450, image=self.radar, anchor="nw")
        self.create_line(250, 450, 550, 450, fill="green", width=1)
        self.create_line(550, 450, 550, 750, fill="green", width=1)
        self.create_line(550, 750, 250, 750, fill="green", width=1)
        self.create_line(250, 750, 250, 450, fill="green", width=1)

        # ship graveyard constants
        PAD_X = 25
        PAD_Y = 50

        # enemy ships
        self.create_text(700, 25, anchor="center", text="Enemy Ships", fill="black", font=GAME_FONT)
        self.drawShip(600+PAD_X, 50, 5)
        self.drawShip(600+PAD_X, 50+PAD_Y, 4)
        self.drawShip(600+PAD_X, 50+2*PAD_Y, 3)
        self.drawShip(600+PAD_X, 50+3*PAD_Y, 3)
        self.drawShip(600+PAD_X, 50+4*PAD_Y, 2)

        # friendly ships
        self.create_text(700, 425, anchor="center", text="Your Ships", fill="black", font=GAME_FONT)
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
        
        x = self.PBOARD_X + self.PBOARD_SPACE * (ship.spaces[0][0] - 1)
        y = self.PBOARD_Y + self.PBOARD_SPACE * (ship.spaces[0][1] - 1)
        vertical = ship.direction[0] == 0
        self.drawShip(x, y, ship.length, vertical, color=color, tags=tags)
    
    def drawShot(self, opponent:bool, pos, result):
        """
        Draw a shot on the applicable board.

        :param opponent: true if shot is by opponent (primary board), false if by player (targeting board)
        :param pos: tuple(int, int) position of the shot in board coordinates (1-10, 1-10)
        :param result: result of the shot (will determine color)
        """
        if result == Result.MISS: clr = "white"
        else: clr = "red"
        if opponent:
            x = self.PBOARD_X + self.PBOARD_SPACE * (pos[0] - 1)
            y = self.PBOARD_Y + self.PBOARD_SPACE * (pos[1] - 1)
            self.create_oval(x, y, x+self.PBOARD_SPACE, y+self.PBOARD_SPACE, fill=clr, width=0)
        else:
            x = self.TBOARD_X + self.TBOARD_SPACE * (pos[0] - 1)
            y = self.TBOARD_Y + self.TBOARD_SPACE * (pos[1] - 1)
            self.create_oval(x, y, x+self.TBOARD_SPACE, y+self.TBOARD_SPACE, fill=clr, width=0)

    def drawSunk(self, opponent:bool, shipName):
        """
        Draw a strikethrough for the applicable sunk ship in the ship display panel

        :param opponent: true if opponent's ship, false if player's
        :param shipName: name of ship to draw strikethrough through
        """
        x = 625
        shippad = 10
        if opponent: y = 65
        else: y = 465
        
        if shipName == "Carrier": length = 5*30; y += 0
        elif shipName == "Battleship": length = 4*30; y += 50
        elif shipName == "Destroyer": length = 3*30; y += 100
        elif shipName == "Submarine": length = 3*30; y += 150
        elif shipName == "Patrol Boat": length = 2*30; y += 200
        else: raise ValueError(f"Unknown ship name \"{shipName}\"")

        self.create_line(x-shippad, y, x+length+shippad, y, fill="red", width=3)

    class InfoSidebar(tk.Frame):
        def __init__(self, master):
            super().__init__(bg=BG_COLOR)
            self.master = master
            self.labels:dict[str, tk.Label] = {}

            self.labels["turninfo"] = tk.Label(self, text="Setup Phase", bg=BG_COLOR, font=GAME_FONT)
            self.labels["instructions"] = tk.Label(self, text="Place Your Ships\nUse arrow keys to move the ship\nPress Space to rotate\nPress Enter to confirm", bg=BG_COLOR)
            self.labels["lobbyinfoheader"] = tk.Label(self, text="Lobby Info:", bg=BG_COLOR, font=GAME_FONT)
            self.labels["lobbyinfo"] = tk.Label(self, text="Game Type: Local", bg=BG_COLOR)
            self.labels["opponentinfo"] = tk.Label(self, text="Opponent: CPU", bg=BG_COLOR)

            for lb in self.labels.values():
                lb.pack()
            
            self.quitbutton = tk.Button(self, text="Quit", command=self.quit, width=15, height=2)
            self.quitbutton.pack(side="bottom", pady=20)
        
        def changeLabel(self, labelname, newTxt):
            """Change the text of label with labelname to display newTxt"""
            self.labels[labelname].configure(text=newTxt)
            self.labels[labelname].update()
        
        def getLabelText(self, labelname):
            return self.labels[labelname].cget("text")
        
        def quit(self):
            self.master.master.display(TitleScreen(self.master.master))
    
    ### SETUP PHASE ###
    def initializeSetupPhase(self):
        self.shipsToPlace = [Ship((0, 0), 5, (1, 0), "Carrier"), Ship((0, 0), 4, (1, 0), "Battleship"), Ship((0, 0), 3, (1, 0), "Destroyer"), Ship((0, 0), 3, (1, 0), "Submarine"), Ship((0, 0), 2, (1, 0), "Patrol Boat")]
        self.getNextShip()
    
    def getNextShip(self):
        # if list is empty, this will raise an exception we can handle elsewhere
        self.nextShip = self.shipsToPlace[0]
        self.shipsToPlace.pop(0)

        #TODO: maybe optimize this?
        # find an empty space to place the ship in (to start)
        valid = self.board.isShipValid(self.nextShip)
        while valid != 0:
            if valid == 2: # advance horizontally
                self.nextShip.translate((1, 0))
            else: # out of bounds, reset horizontal and advance vertically
                self.nextShip.translate((1-self.nextShip.pos[0], 1))
            valid = self.board.isShipValid(self.nextShip)
        
        self.drawShipObject(self.nextShip, "lightgray", "shipToPlace")
    
    def moveSetupShip(self, transVector):
        """
        moveSetupShip moves the setup ship by the specified amount. If a ship is in the way, it moves the setup ship through the ship to the next open space in that direction.
        If there's no open space in that direction, it doesn't make the move.

        :param transVector: The vector by which to move the ship - [dx, dy]
        """
        # check if translation is valid
        translated = copy.deepcopy(self.nextShip)
        translated.translate(transVector)
        valid = self.board.isShipValid(translated)
        while valid != 0:
            if valid == 1: return # now out of bounds, don't move ship
            translated.translate(transVector) # if inside another ship, move further and try again
            valid = self.board.isShipValid(translated)
        self.nextShip = translated
        self.delete("shipToPlace")
        self.drawShipObject(self.nextShip, "lightgray", "shipToPlace")

    def rotateSetupShip(self):
        """ 
        Attempt to rotate the startup ship 90 degrees clockwise.
        If there's something in the way or the rotation would place the ship out of bounds, don't rotate.
        """
        rotated = copy.deepcopy(self.nextShip)
        rotated.rotate()
        if self.board.isShipValid(rotated) != 0: return
        self.nextShip = rotated
        self.delete("shipToPlace")
        self.drawShipObject(self.nextShip, "lightgray", "shipToPlace")
    
    def confirmSetupShip(self):
        """Place setup ship on board and either queue next ship or start game"""
        self.delete("shipToPlace")
        self.board.addShip(self.nextShip)
        self.drawShipObject(self.nextShip, tags=self.nextShip.name)
        try:
            self.getNextShip()
        except: # out of ships to place, so start the game
            self.startGame()
    
    ### MAIN GAME FUNCTIONS ###
    def startGame(self):
        self.opponent.sendConfirmation()
        self.opponent.getConfirmation() # wait for other player to be ready
        self.game_phase = "Main"
        self.myturn = bool(random.getrandbits(1)) #TODO: change this if we implement online multiplayer
        self.changeTurns()
        
    def changeTurns(self):
        self.myturn = not self.myturn
        if self.myturn:
            self.sidebar.changeLabel("turninfo", "Your Turn")
            self.sidebar.changeLabel("instructions", "Click on a space on your\ntargeting board to fire a shot")
        else:
            self.sidebar.changeLabel("turninfo", "Opponent's Turn")
            self.sidebar.changeLabel("instructions", "Opponent is thinking...")
            self.handleOpponentMove()
    
    def handlePlayerMove(self, move):
        try:
            result = self.opponent.sendMove(move)
            self.board.addMyShot(move, result)
            self.drawShot(False, move, result)
            if result == Result.SUNK:
                self.drawSunk(True, self.opponent.board.lastShipSunk().name)
                if self.checkVictory() == 1: return
            self.changeTurns()
        except DuplicateShotError: pass # do nothing if player tries to click the same spot twice
    
    def handleOpponentMove(self):
        """Get move from opponent and update information accordingly, then do end of turn checks."""
        move = self.opponent.getMove()
        result = self.board.addEnemyShot(move)
        self.drawShot(True, move, result) # add peg for move
        self.opponent.sendMoveResult(move, result)
        if result == Result.SUNK:
            self.drawSunk(False, self.opponent.board.lastShipSunk().name)
            if self.checkVictory() == 1: return
        self.changeTurns()
    
    def checkVictory(self):
        """Check to see if either player has won. If so, go to victory screen and return 1. Otherwise, return 0."""
        if len(self.board.aliveShips) == 0:
            self.master.display(VictoryScreen(self.master, "Opponent"))
            return 1
        if len(self.opponent.board.aliveShips) == 0:
            self.master.display(VictoryScreen(self.master, "Player"))
            return 1
        return 0
    
    ### INPUT HANDLING FUNCTIONS ###
    def onKeyPress(self, event):
        if not self.myturn: return # ignore input during opponent's turn

        if self.game_phase == "Setup":
            if event.keysym == "Up": self.moveSetupShip((0, -1))
            elif event.keysym == "Down": self.moveSetupShip((0, 1))
            elif event.keysym == "Left": self.moveSetupShip((-1, 0))
            elif event.keysym == "Right": self.moveSetupShip((1, 0))
            elif event.keysym == "space": self.rotateSetupShip()
            elif event.keysym == "Return": self.confirmSetupShip()

    def onClick(self, event:tk.Event):
        if not self.myturn: return # ignore input during opponent's turn

        if self.game_phase == "Main":
            # ignore if click was outside the targeting board
            if event.x < self.TBOARD_X: return
            if event.x > self.TBOARD_X + 10 * self.TBOARD_SPACE: return
            if event.y < self.TBOARD_Y: return
            if event.y > self.TBOARD_Y + 10 * self.TBOARD_SPACE: return

            x = (event.x - self.TBOARD_X - 1) // self.TBOARD_SPACE + 1
            y = (event.y - self.TBOARD_Y - 1) // self.TBOARD_SPACE + 1
            self.handlePlayerMove((x, y))

class VictoryScreen(tk.Frame):
    def __init__(self, master, winner:str):
        super().__init__(background = BG_COLOR)
        self.master = master

        self.label = tk.Label(self, text=f"{winner} Won!", font=UI_FONT, bg=BG_COLOR)
        self.rematchbutton = tk.Button(self, command=self.rematch, text="Rematch", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.titlebutton = tk.Button(self, command=self.title, text="Title Screen", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.exitbutton = tk.Button(self, command=self.master.destroy, text="Quit", width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.label.pack(pady=PAD)
        self.rematchbutton.pack(pady=PAD)
        self.titlebutton.pack(pady=PAD)
        self.exitbutton.pack(pady=PAD)
    
    def rematch(self):
        raise NotImplementedError("Rematch function is not implemented yet")

    def title(self):
        self.master.display(TitleScreen(self.master))
        

# main game object
class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Battleship")
        self.configure(background=BG_COLOR)

        self.current_screen = None # current frame being displayed
        self.display(TitleScreen(self))

    def title_screen(self):
        ts = TitleScreen(self)
        ts.pack()

    def host_screen(self):
        hs = HostScreen(self)
        hs.pack()

    def join_screen(self):
        js = JoinScreen(self)
        js.pack()

    def display(self, screen):
        """Destroy current screen and display passed screen."""
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = screen
        self.current_screen.pack()

if __name__ == "__main__":
    game = Game()
    game.display(GameScreen(game, ComputerPlayer(IntermediateCPU(False))))
    game.mainloop()
    '''root = tk.Tk()
    game = GameScreen(root, ComputerPlayer())
    game.pack()
    root.mainloop()'''