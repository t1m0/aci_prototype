from random import randrange
from Application.Cell import Cell

class SecurityGuard:
    def __init__(self,map):
        start_row,start_col = map.startpoint.get_pos()
        end_row,end_col = map.endpoint.get_pos()
        size = map.size
        row = self.__get_random_number(size,start_row,end_row)
        col = self.__get_random_number(size,start_col,end_col)
        start_cell = map.get_cell(row,col)
        self.movement = [start_cell]
        
    def get_current_cell(self):
        return self.movement[-1]
    
    def move(self, map, diagonal_movement):
        row, col = self.get_current_cell().get_pos()
        if diagonal_movement:
            movement = randrange(3)
        else:
            movement = randrange(7)

        if(movement == 0 and row+1 < map.size):
            self.movement.append(map.get_cell(row+1,col))
        if(movement == 1 and row-1 >= 0):
            self.movement.append(map.get_cell(row-1,col))
        if(movement == 2 and col+1 < map.size):
            self.movement.append(map.get_cell(row,col+1))
        if(movement == 3 and col-1 >= 0):
            self.movement.append(map.get_cell(row,col-1))
        if((movement == 4)and(row+1 < map.size) and (col+1 < map.size) and diagonal_movement):
            self.movement.append(map.get_cell(row+1,col+1))
        if((movement == 5)and(row-1 >= 0) and (col-1 >=0) and diagonal_movement):
            self.movement.append(map.get_cell(row-1,col-1))
        if((movement == 6)and(row+1 < map.size) and (col-1 >=0) and diagonal_movement):
            self.movement.append(map.get_cell(row+1,col+1))
        if((movement == 7)and(row-1 >= 0) and (col+1 < map.size) and diagonal_movement):
            self.movement.append(map.get_cell(row-1,col+1))
        return self.movement

    def __get_random_number(self,max,exclude_start,exclude_end):
        random_number = None
        while random_number == None:
            current_random_number = randrange(max)
            if(current_random_number != exclude_start and current_random_number != exclude_end):
                random_number = current_random_number
        return random_number
