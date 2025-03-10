import tkinter as tk
import pygame

# container representing the main interactive area (primary grid and targeting grid)
class GameScreen():
    def __init__(self, master):
        self.master = master

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Battleship")

        self.title_screen()

    # display the title screen
    def title_screen(self):
        PAD = 10
        BUTTONWIDTH = 40
        BUTTONHEIGHT = 7

        root = tk.Tk()
        root.geometry("500x500")
        root.title("Battleship Title Screen")
        frame = tk.Frame(root)
        
        label = tk.Label(frame, text="Battleship", font=('Arial', 18))
        hostbutton = tk.Button(frame, command=self.host_screen, text="Host Game", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        joinbutton = tk.Button(frame, text="Join Game", width=BUTTONWIDTH, height=BUTTONHEIGHT)
        exitbutton = tk.Button(frame, text="Quit", width=BUTTONWIDTH, height=BUTTONHEIGHT)

        label.pack(pady=PAD)
        hostbutton.pack(pady=PAD)
        joinbutton.pack(pady=PAD)
        exitbutton.pack(pady=PAD)

        frame.pack()
    
    def host_screen(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.mainloop()