
from Application.Cell import Cell
from Application.SecurityGuard import SecurityGuard

class Map:

    def __init__(self, name, map_data, num_security_guards=3):
        self.name = name
        self.map_data = map_data
        self.cells = self.__make_cells(map_data)
        self.startpoint, self.endpoint = self.__find_start_and_end(self.cells)
        height, width = map_data.shape
        self.node_count = (height * width -2)
        self.size = height
        self.num_security_guards = num_security_guards
        self.security_guards = []
        self.place_security_guards()

    '''create for each element in the map a cell object'''
    def __make_cells(self, map_data):
        rows, cols = map_data.shape
        return [[Cell(i, j, int(map_data[i][j]), rows) for j in range(rows)] for i in range(cols)]

    def __find_start_and_end(self, cells):
        for row in cells:
            for cell in row:
                if cell.weight == -10:
                    startpoint = cell
                if cell.weight == -11:
                    endpoint = cell
        return startpoint, endpoint

    def place_security_guards(self):
        self.security_guards.clear()
        for i in range(self.num_security_guards):
            self.security_guards.append(SecurityGuard(self))

    def move_security_guards(self,diagonal_movement=False):
        for security_guard in self.security_guards:
            security_guard.move(self, diagonal_movement)

    def find_neighbors(self, current_cell, diagonal_movement=False):
        row,col = current_cell.get_pos()
        neighbors = []
        if(row+1 < self.size):
            neighbors.append(self.get_cell(row+1,col))
        if(row-1 >= 0):
            neighbors.append(self.get_cell(row-1,col))
        if(col+1 < self.size):
            neighbors.append(self.get_cell(row,col+1))
        if(col-1 >= 0):
            neighbors.append(self.get_cell(row,col-1))
        if((row+1 < self.size) and (col+1 < self.size) and diagonal_movement):
            neighbors.append(self.get_cell(row+1,col+1))
        if((row-1 >= 0) and (col-1 >=0) and diagonal_movement):
            neighbors.append(self.get_cell(row-1,col-1))
        if((row+1 < self.size) and (col-1 >=0) and diagonal_movement):
            neighbors.append(self.get_cell(row+1,col+1))
        if((row-1 >= 0) and (col+1 < self.size) and diagonal_movement):
            neighbors.append(self.get_cell(row-1,col+1))
        return neighbors

    def get_weight(self, in_cell):
        row, col = in_cell.get_pos()
        cell = self.cells[col][row]
        for security_guard in self.security_guards:
            if security_guard.get_current_cell() == cell:
                return 3000
        return cell.weight

    def get_cell(self, row, col):
        cell = self.cells[col][row]
        return cell
