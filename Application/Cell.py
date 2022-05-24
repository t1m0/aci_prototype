class Cell:
    cost = 0
    def __init__(self,col,row,value,total_rows):
        self.row = row
        self.col = col
        self.weight = value
        self.total_rows = total_rows

    def get_pos(self):
        return (self.row,self.col)
    
    def get_weight(self):
        return (self.weight)
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Cell):
            return self.row == other.row and self.col == other.col and self.weight == other.weight
        return False
    
    def __hash__(self):
        return hash((self.row, self.col, self.weight))
         