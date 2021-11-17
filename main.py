import sys

sys.path.append(".")
from GoLOO import GoL
import tkinter

gol = GoL()

colors = ["#FFFFFF", "#FFFF80", "#FFFF00", "#FF8000", "#FF4000", "#FF2000", "#FF0000", "#c00000", "#800000", "#000000"]


def updateCanvas(C):
    global rect
    global refreshLabel
    global refreshScreen
    global CellCounterLabel
    gol.countNeighbours()
    refreshLabel.configure(text="Gernerations: " + str(refreshScreen))
    CellCounterLabel.configure(text="Living Cells:  " + str(len(gol.universe)))
    C.itemconfigure(tagOrId="all", fill="lightblue", width=0)
    for (row, column) in gol.neighbours:
        color = colors[gol.neighbours[(row, column)]]
        width = 1
        if (row, column) in gol.universe:
            width = 5
        tag = str(row) + ":" + str(column)
        C.itemconfigure(tagOrId=str(row) + ":" + str(column), fill=color, width=width)


#
# Interface routines for Tk
#
cellSize=15
def toggle(e):
    """
    Calll back function for taggling cell, calculates screen coordinates in universum coordinate
    :param e: klick point
    :return:
    """
    col = e.y //cellSize
    row = e.x //cellSize
    gol.toggle(row, col)
    updateCanvas(C)

def stepb():
    """
     Button function for a single step ,
     """
    gol.step()
    updateCanvas(C)


refreshScreen = 0


def loopbFirst():
    """
    start single stepping in background for the first time,
    switch into keepRunning mode and lauch timer step generation
    """
    global keepRunning
    keepRunning = True
    loopb()


def loopb():
    """ background tasks called every millisecond """
    global refreshScreen
    global top
    global keepRunning
    global gol
    gol.step()
    refreshScreen += 1
    if refreshScreen % 5 == 0:  # Update screen only ever 10th step for speed up
        updateCanvas(C)
    if (keepRunning):  # chekc whether stop button was pressedn
        top.after(1, loopb)


def stopb():
    """ switch of background task
    """
    global keepRunning
    keepRunning = False


def clearb():
    """
    Clear the universe and update display
    """
    global C
    global gol
    gol = GoL()
    gol.countNeighbours()
    updateCanvas(C)
    print("cleared...")


def GoLGUI():
    """ Start the GUI interface for the Game of Life"""
    global C  # make the canvas widget accessible to the updateCanvas function
    global top  # make the top window available to the background tasks and to whoever needs it
    global refreshScreen  # make the generation counter acccessible to whoever needs it
    refreshScreen = 0
    top = tkinter.Tk()
    top.title("Game of Life")
    l = tkinter.Label(top, text="Game of Life")
    l.config(font=("Arial", 44))
    l.pack()
    C = tkinter.Canvas(top, bg="white", width=1000, height=800)
    rect = {}
    # prepare the GUI Window with all cells predrawn, to be configured later
    for row in range(80):
        for column in range(50):
            rect[(row, column)] = C.create_oval(row * cellSize, column * cellSize, row * cellSize + cellSize-1, column * cellSize + cellSize-1,
                                                tag=str(row) + ":" + str(column))
            C.tag_bind(rect[(row, column)], "<ButtonPress-1>", toggle)
    C.pack()
    #
    # Command buttons and labels for interaction
    #
    buttonframe = tkinter.Frame(top)
    buttonframe.pack(expand=True)
    nextButton = tkinter.Button(buttonframe, text='Next', width=15, command=stepb)
    nextButton.config(font=("Arial", 14))
    nextButton.pack(side=tkinter.LEFT)
    loopButton = tkinter.Button(buttonframe, text='Loop', width=15, command=loopbFirst)
    loopButton.pack(side=tkinter.LEFT)
    stopButton = tkinter.Button(buttonframe, text='Stop', width=15, command=stopb)
    stopButton.pack(side=tkinter.LEFT)
    global refreshLabel
    refreshLabel = tkinter.Label(buttonframe, text=str(refreshScreen), width=25)
    refreshLabel.pack(side=tkinter.LEFT)
    global CellCounterLabel
    CellCounterLabel = tkinter.Label(buttonframe, text=str(len(gol.universe)), width=25)
    CellCounterLabel.pack(side=tkinter.LEFT)

    clearButton = tkinter.Button(buttonframe, text="Clear", width=15, command=clearb)
    clearButton.pack(side=tkinter.LEFT)

    updateCanvas(C)
    top.mainloop()


GoLGUI()
