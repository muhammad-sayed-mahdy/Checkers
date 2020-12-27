import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Checkers import Checkers, Positions

window = tk.Tk()
window.title("Checkers")
IMG_SIZE = 75
black_man = ImageTk.PhotoImage(Image.open('assets/black_man.png').resize((IMG_SIZE, IMG_SIZE)))
black_king = ImageTk.PhotoImage(Image.open('assets/black_king.png').resize((IMG_SIZE, IMG_SIZE)))
white_man = ImageTk.PhotoImage(Image.open('assets/white_man.png').resize((IMG_SIZE, IMG_SIZE)))
white_king = ImageTk.PhotoImage(Image.open('assets/white_king.png').resize((IMG_SIZE, IMG_SIZE)))
blank_white = ImageTk.PhotoImage(Image.open('assets/blank_white.png').resize((IMG_SIZE, IMG_SIZE)))
blank_black = ImageTk.PhotoImage(Image.open('assets/blank_black.png').resize((IMG_SIZE, IMG_SIZE)))

MAX_DEPTH = 5

class GUI:
    
    def __init__(self) -> None:
        super().__init__()
        self.game = Checkers()
        
        self.player = Checkers.BLACK
        if self.player == Checkers.WHITE:
            self.game.minimaxPlay(1-self.player, maxDepth=MAX_DEPTH, evaluate=Checkers.evaluate2, enablePrint=False)
        
        self.lastX = None
        self.lastY = None
        self.willCapture = False
        self.cnt = 0
        self.btn = [[None]*self.game.size for _ in range(self.game.size)]
        for i in range(self.game.size):
            window.columnconfigure(i, weight=1, minsize=IMG_SIZE)
            window.rowconfigure(i, weight=1, minsize=IMG_SIZE)

            for j in range(self.game.size):
                frame = tk.Frame(master=window)
                frame.grid(row=i, column=j, sticky="nsew")

                self.btn[i][j] = tk.Button(master=frame, width=IMG_SIZE, height=IMG_SIZE)
                self.btn[i][j].bind("<Button-1>", self.click)
                self.btn[i][j].pack(expand=True)
                
        self.update()
        nextPositions = [move[0] for move in self.game.nextMoves(self.player)]
        self.highlight(nextPositions)
        totalSize = IMG_SIZE*self.game.size
        window.geometry(f"{totalSize}x{totalSize}")
        window.mainloop()

    def update(self):
        for i in range(self.game.size):
            f = i % 2 == 1
            for j in range(self.game.size):

                if f:
                    img = blank_black
                else:
                    img = blank_white
                if self.game.board[i][j] == Checkers.BLACK_MAN:
                    img = black_man
                elif self.game.board[i][j] == Checkers.BLACK_KING:
                    img = black_king
                elif self.game.board[i][j] == Checkers.WHITE_MAN:
                    img = white_man
                elif self.game.board[i][j] == Checkers.WHITE_KING:
                    img = white_king

                self.btn[i][j]["image"] = img
                
                f = not f
    
    def highlight(self, positions: Positions):
        defaultbg = window.cget('bg')
        for x in range(self.game.size):
            for y in range(self.game.size):
                self.btn[x][y].master.config(highlightbackground=defaultbg, highlightthickness=3)

        for position in positions:
            x, y = position
            self.btn[x][y].master.config(highlightbackground="yellow", highlightthickness=3)

    def click(self, event):
        info = event.widget.master.grid_info()
        x, y = info["row"], info["column"]
        if self.lastX == None or self.lastY == None:
            moves = self.game.nextMoves(self.player)
            found = (x, y) in [move[0] for move in moves]
            
            if found:
                self.lastX = x
                self.lastY = y
                normal, capture = self.game.nextPositions(x, y)
                positions = normal if len(capture) == 0 else capture
                self.highlight(positions)
            else:
                print("Invalid position")
            return

        normalPositions, capturePositions = self.game.nextPositions(self.lastX, self.lastY)
        positions = normalPositions if (len(capturePositions) == 0) else capturePositions
        if (x,y) not in positions:
            print("invalid move")
            if not self.willCapture:
                self.lastX = None
                self.lastY = None
                nextPositions = [move[0] for move in self.game.nextMoves(self.player)]
                self.highlight(nextPositions)
            return

        canCapture, removed, _ = self.game.playMove(self.lastX, self.lastY, x, y)
        self.update()
        self.cnt += 1
        self.lastX = None
        self.lastY = None
        self.willCapture = False

        if removed != 0:
            self.cnt = 0
        if canCapture:
            _, nextCaptures = self.game.nextPositions(x, y)
            if len(nextCaptures) != 0:
                self.willCapture = True
                self.lastX = x
                self.lastY = y
                self.highlight(nextCaptures)
                return
        evaluate = Checkers.evaluate2
        if self.cnt > 25:
            evaluate = Checkers.sumDistances
        cont, reset = self.game.minimaxPlay(1-self.player, maxDepth=MAX_DEPTH, evaluate=evaluate, enablePrint=False)
        self.cnt += 1
        if not cont:
            messagebox.showinfo(message="You Won!", title="Checkers")
            window.destroy()
            return
        self.update()
        if reset:
            self.cnt = 0
        if self.cnt == 100:
            messagebox.showinfo(message="Draw!", title="Checkers")
            window.destroy()
            return
        
        nextPositions = [move[0] for move in self.game.nextMoves(self.player)]
        self.highlight(nextPositions)
        if len(nextPositions) == 0:
            messagebox.showinfo(message="You lost!", title="Checkers")
            window.destroy()

GUI()