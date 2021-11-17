"""
base class for Game of life
"""

class GoL():
    """ Class containing one instance of a game of life board
Methods
 init  initialise game and rules
    """

    def __init__(self, cell_list={}, stay_alive={2, 3}, get_born={3}):
        """
        create initialise board, , and rules for when a cell is to be born
        or survive depending on the number of its neighbours
        """
        self.universe = set(cell_list)
        self.neighbours = {}
        self.stay_alive = stay_alive
        self.get_born = get_born

    def toggle(self, x, y):
        """ toggle a cell with row x and column y
        """
        if (x, y) in self.universe:
            self.universe = self.universe - {(x, y)}
            return False
        else:
            self.universe = self.universe | {(x, y)}
            return True

    def countNeighbours(self):
        """ for each cell in universe count up the neighbors"""
        self.neighbours = {}  # a sparse dictionary
        for cell in self.universe:  # only for cells set in universe
            (row, col) = cell
            for rR in range(row - 1, row + 2):
                for rC in range(col - 1, col + 2):  # 9 field square surrounding the cell
                    try:
                        self.neighbours[(rR, rC)] += 1
                    except:
                        self.neighbours[(rR, rC)] = 1
            self.neighbours[cell] -= 1  # you are not your own neighbour
        return self.neighbours

    def step(self):
        """
        generate the next generation of cells
        """
        new_universe = set([])  # new universe initially empty
        neighbours = self.countNeighbours()
#     print(neighbours)
        for cell in neighbours:
            if cell in self.universe:
                if neighbours[cell] in self.stay_alive:
                    new_universe = new_universe | {cell}
#                  print(str(cell) + "survived")
            elif neighbours[cell] in self.get_born:
                new_universe = new_universe | {cell}
#              print(str(cell) + "born")
        self.universe = new_universe
