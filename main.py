"""
User interface for manipulation of Conways Game of life
"""

import sys
import tkinter
from tkinter import filedialog as fd

# sys.path.append(".")
from GoLOO import GoL

gol = GoL()
colors = ["#FFFFFF", "#FFFF80", "#FFFF00", "#FF8000",
          "#FF0020", "#800040", "#400060", "#000040",
          "#200010", "#000000"]


def updateCanvas(C):
    global rect
    global refreshLabel
    global refreshScreen
    global CellCounterLabel
    global gol
    global stay_alive_vars
    global get_born_vars
    gol.countNeighbours()
    refreshLabel.configure(text="Gernerations: " + str(refreshScreen))
    CellCounterLabel.configure(text="Living Cells:  " + str(len(gol.universe)))
    C.itemconfigure(tagOrId="all", fill="lightblue", width=0)
    for (row, column) in gol.neighbours:
        if (row, column) in rect:
            color = colors[gol.neighbours[(row, column)]]
            width = 0
            if (row, column) in gol.universe:
                width = 1
            #           tag = str(row) + ":" + str(column)
            C.itemconfigure(tagOrId=rect[(row, column)], fill=color, width=width)
    for i in range(9):
        if i in gol.get_born:
            get_born_vars[i].set(1)
        else:
            get_born_vars[i].set(0)
        if i in gol.stay_alive:
            stay_alive_vars[i].set(1)
        else:
            stay_alive_vars[i].set(0)


#
# Interface routines for Tk
#
cellSize = 15


def toggle(e):
    """
    Calll back function for taggling cell, calculates screen coordinates in universum coordinate
    :param e: klick point
    :return:
    """
    col = e.y // cellSize
    row = e.x // cellSize
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
    switch into keepRunning mode and launch timer step generation
    """
    global keepRunning
    global loopButton
    loopButton.config(text="Stop", command=stopb)  # Change Button to Stop
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
    if refreshScreen % 7 == 0:  # Update screen only ever ith step for speed up
        updateCanvas(C)
    if (keepRunning):  # chekc whether stop button was pressedn
        top.after(1, loopb)   # schedule again


def stopb():
    """ switch of background task
    """
    global keepRunning
    keepRunning = False
    loopButton.config(text="Loop", command=loopbFirst)


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


def loadfile():
    """" Read in a file containing the set cells and the limits for survinving and new to be born cells
        file format is in Python set format, separated by semicolons
    """
    global C
    global gol
    with tkinter.filedialog.askopenfile(mode='r') as f:
        s = f.read()
    #   print (s)
    (u, stay, get) = s.split(";", -1)
    gol = GoL(eval(u), eval(stay), eval(get))
    updateCanvas(C)


def savefile():
    """" Write current universe to  a file containing the set cells and the limits for surviving and new to be born cells
         file format is in Python set format, separated by semicolons
     """
    with tkinter.filedialog.asksaveasfile(mode='w') as f:
        f.write(str(gol.universe) +
                ";" +
                str(gol.stay_alive) +
                ";" +
                str(gol.get_born))


def updateRules():
    """ read the rules for cell survival and creation from the GUI Control check boxes
    and transfer them into the attribult of the GoL class object"""
    global stay_alive_vars  # list of Tk Vars connected to check boxes
    global get_born_vars
    global gol

    for i in range(9):                    # from 0 to 8 possible neigbours
        if stay_alive_vars[i].get() != 0: # if check box set
            gol.stay_alive |= {i}         # set the corresponding element in the Gol class attribute
        else:
            gol.stay_alive -= {i}         # otherwise clear
        if get_born_vars[i].get() != 0:   # mutatis mutandis for newly born cells
            gol.get_born |= {i}
        else:
            gol.get_born -= {i}
    pass

def GoLGUI():
    """ Start the GUI interface for the Game of Life"""
    global C  # make the canvas widget accessible to the updateCanvas function
    global top  # make the top window available to the background tasks and to whoever needs it
    global refreshScreen  # make the generation counter acccessible to whoever needs it
    global loopButton
    global stay_alive_vars
    global get_born_vars

    global rect
    rect = {}

    refreshScreen = 0
    #
    # General window set up
    #
    top = tkinter.Tk()
    top.title("Game of Life")
    l = tkinter.Label(top, text="Game of Life")
    l.config(font=("Arial", 14))
    l.pack()
    #
    #   Check boxes determining Game of life rules in terms of number of neighbours
    #
    rulesframe = tkinter.Frame(top)
    rulesframe.pack(side=tkinter.TOP, expand=True)
    stay_alive_label = tkinter.Label(rulesframe,
                                     text="Alive cell survives on neighbors",
                                     font=("Arial", 12))
    stay_alive_label.pack(side=tkinter.LEFT)

    stay_alive_vars = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        stay_alive_vars[i] = tkinter.IntVar()
        cn = tkinter.Checkbutton(rulesframe, text=str(i), variable=stay_alive_vars[i], onvalue=1, offvalue=0,
                                 command=updateRules)
        if i in gol.stay_alive:
            stay_alive_vars[i].set(1)
        else:
            stay_alive_vars[i].set(0)
        cn.pack(side=tkinter.LEFT)

    get_born_label = tkinter.Label(rulesframe,
                                   text="New cells gets born on neighbours",
                                   font=("Arial", 12))
    get_born_label.pack(side=tkinter.LEFT)
    get_born_vars = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        get_born_vars[i] = tkinter.IntVar()
        cn = tkinter.Checkbutton(rulesframe, text=str(i), variable=get_born_vars[i], onvalue=1, offvalue=0,
                                 command=updateRules)
        if i in gol.get_born:
            get_born_vars[i].set(1)
        else:
            get_born_vars[i].set(0)
        cn.pack(side=tkinter.LEFT)

    #
    #   Create canvas for cell display
    #
    C = tkinter.Canvas(top, bg="white", width=cellSize * 80, height=cellSize * 50)

    # prepare the GUI Window with all cells predrawn, to be configured later
    for row in range(80):
        for column in range(50):
            rect[(row, column)] = C.create_rectangle(row * cellSize, column * cellSize, row * cellSize + cellSize - 1,
                                                     column * cellSize + cellSize - 1,
                                                     tag=str(row) + ":" + str(column))
    #       C.tag_bind(rect[(row, column)], "<ButtonPress-1>", toggle)
    C.bind("<ButtonPress-1>", toggle)
    C.pack()
    #
    # Command buttons and labels for interaction
    #
    buttonframe = tkinter.Frame(top)
    buttonframe.pack(side=tkinter.TOP, expand=True)
    nextButton = tkinter.Button(buttonframe, text='Next', width=15, command=stepb)
    nextButton.config(font=("Arial", 14))
    nextButton.pack(side=tkinter.LEFT)
    loopButton = tkinter.Button(buttonframe, text='Loop', width=15, command=loopbFirst)
    loopButton.pack(side=tkinter.LEFT)
    clearButton = tkinter.Button(buttonframe, text="Clear", width=15, command=clearb)
    clearButton.pack(side=tkinter.LEFT)


    labelframe = tkinter.Frame(top)
    labelframe.pack(side=tkinter.TOP)
    global refreshLabel
    refreshLabel = tkinter.Label(labelframe, text=str(refreshScreen), width=25)
    refreshLabel.pack(side=tkinter.LEFT)
    global CellCounterLabel

    CellCounterLabel = tkinter.Label(labelframe, text=str(len(gol.universe)), width=25)
    CellCounterLabel.pack(side=tkinter.LEFT)


    #
    # Menubar or saving and loading of files and quiting
    #
    menubar = tkinter.Menu(top, font=("Arial", 20))
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.configure(font=("Arial", 14, "bold"))
    #
    filemenu.add_command(label="Open", command=loadfile, accelerator="Ctrl+O")
    filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S")
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.quit, accelerator="Ctrl+Q")
    mm = menubar.add_cascade(label="File", font=("Verdana", 14), menu=filemenu)
    # accelerator tag above is not enough
    # need to intercept key events to the top level window
    top.bind_all("<Control-q>", lambda event: top.quit())
    top.bind_all("<Control-o>", lambda event: loadfile())
    top.bind_all("<Control-s>", lambda event: savefile())
    top.config(menu=menubar)
    #
    # refresh canvas
    #
    updateCanvas(C)
    #
    # main gui loop
    #
    top.mainloop()


GoLGUI()
