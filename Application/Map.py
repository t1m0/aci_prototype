
import re
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
        self.__store_weights_for_security_guards()

    def move_security_guards(self,diagonal_movement=False):
        for security_guard in self.security_guards:
            security_guard.move(self, diagonal_movement)
        self.__store_weights_for_security_guards()
    
    def find_neighbors_in_radius(self, current_cell, radius=1):
        row,col = current_cell.get_pos()
        
        lower_row = self.__find_lowest(row,radius)
        lower_col = self.__find_lowest(col,radius)
        higher_row = self.__find_highest(row,radius)
        higher_col = self.__find_highest(col,radius)

        left_side = self.__walk_vertical_line(lower_col,higher_col,lower_row) 
        right_side = self.__walk_vertical_line(lower_col,higher_col,higher_row) 
        top_side = self.__walk_horizontal_line(lower_row,higher_row,higher_col)
        lower_side = self.__walk_horizontal_line(lower_row,higher_row,lower_col)

        neighbors = left_side + right_side + top_side + lower_side
        return neighbors
    
    def find_neighbors(self, current_cell):
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
        return neighbors

    def security_guard_in_close_proximity(self,cell):
        one_cell_radius = self.find_neighbors_in_radius(cell,radius=1)
        two_cell_radius = self.find_neighbors_in_radius(cell,radius=2)
        three_cell_radius = self.find_neighbors_in_radius(cell,radius=3)
        four_cell_radius = self.find_neighbors_in_radius(cell,radius=4)
        relevant_cells = one_cell_radius+two_cell_radius+three_cell_radius+four_cell_radius
        for relevant_cell in relevant_cells:
            if relevant_cell in self.security_guard_weights.keys() and self.security_guard_weights[relevant_cell] == 4000:
                return True
        return False
        
    def __find_lowest(self,current,radius):
        if current-radius > 0:
            return current-radius
        else:
            return 0
    
    def __find_highest(self,current,radius):
        if current+radius < self.size:
            return current+radius
        else:
            return self.size-1

    def __walk_vertical_line(self,start,end,stable):
        cells = []
        for i in range(start,end+1):
            cells.append(self.get_cell(stable,i))
        return cells

    def __walk_horizontal_line(self,start,end,stable):
        cells = []
        for i in range(start,end+1):
            cells.append(self.get_cell(i,stable))
        return cells

    def get_weight(self, in_cell):
        row, col = in_cell.get_pos()
        cell = self.cells[col][row]
        if cell in self.security_guard_weights.keys():
            return self.security_guard_weights[cell]
        return cell.weight

    def get_cell(self, row, col):
        try: 
            cell = self.cells[col][row]
            return cell
        except IndexError:
            print(f"Failed to lookup {col} | {row}")
            return None

    def __store_weights_for_security_guards(self):
        self.security_guard_weights = {}
        for security_guard in self.security_guards:
            sec_cell = security_guard.get_current_cell()
            self.security_guard_weights[sec_cell] = 4000
            self.__store_security_guard_neighbor_weights(sec_cell, radius=1, weight=3900)
            self.__store_security_guard_neighbor_weights(sec_cell, radius=2,weight=3800)
    
    def __store_security_guard_neighbor_weights(self,sec_cell,radius,weight):
        for neighbor in self.find_neighbors_in_radius(sec_cell, radius=radius):
                if not neighbor in self.security_guard_weights.keys():
                    self.security_guard_weights[neighbor] = weight
