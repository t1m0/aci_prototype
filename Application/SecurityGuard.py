from random import randrange
from Application.Cell import Cell

class SecurityGuard:

    restricted_fields = [3000, 25, 35, -10, -11]

    def __init__(self,map):
        
        start_cell = self.__get_random_cell(map)
        self.movement = [start_cell]
        
    def get_current_cell(self):
        return self.movement[-1]
    
    def move(self, map, diagonal_movement):
        row, col = self.get_current_cell().get_pos()
        
        new_cell = None
        
        while new_cell == None:
            if diagonal_movement:
                movement = randrange(3)
            else:
                movement = randrange(7)
            if(movement == 0 and row+1 < map.size):
                new_cell = map.get_cell(row+1,col)
            if(movement == 1 and row-1 >= 0):
                new_cell = map.get_cell(row-1,col)
            if(movement == 2 and col+1 < map.size):
                new_cell = map.get_cell(row,col+1)
            if(movement == 3 and col-1 >= 0):
                new_cell = map.get_cell(row,col-1)
            if((movement == 4)and(row+1 < map.size) and (col+1 < map.size) and diagonal_movement):
                new_cell = map.get_cell(row+1,col+1)
            if((movement == 5)and(row-1 >= 0) and (col-1 >=0) and diagonal_movement):
                new_cell = map.get_cell(row-1,col-1)
            if((movement == 6)and(row+1 < map.size) and (col-1 >=0) and diagonal_movement):
                new_cell = map.get_cell(row+1,col+1)
            if((movement == 7)and(row-1 >= 0) and (col+1 < map.size) and diagonal_movement):
                new_cell = map.get_cell(row-1,col+1)
            if new_cell != None and new_cell.weight in self.restricted_fields:
                new_cell = None

        if new_cell != None and not new_cell.weight in self.restricted_fields:
            self.movement.append(new_cell)

    def __get_random_cell(self,map):
        start_row,start_col = map.startpoint.get_pos()
        end_row,end_col = map.endpoint.get_pos()
        size = map.size

        random_cell = None
        while random_cell == None:
            row = self.__get_random_number(size,start_row,end_row)
            col = self.__get_random_number(size,start_col,end_col)
            random_cell = map.get_cell(row,col)
            if random_cell.weight in self.restricted_fields:
                random_cell = None
        return random_cell

    def __get_random_number(self,max,exclude_start,exclude_end):
        random_number = None
        while random_number == None:
            current_random_number = randrange(max)
            if current_random_number != exclude_start and current_random_number != exclude_end:
                random_number = current_random_number
        return random_number
