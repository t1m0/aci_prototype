class Paparazi:
    
    def __init__(self,startpoint):
        self.path = [startpoint]
    
    def get_current_cell(self):
        return self.path[-1]

    def move(self,startpoint):
        self.path.append(startpoint)