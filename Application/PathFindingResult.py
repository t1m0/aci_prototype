import uuid
class PathFindingResult:
    
    def __init__(self,name,map,heuristic,path,a_star_executions,total_iteration,time_elapsed):
        self.name = name
        self.map = map
        self.heuristic = heuristic
        self.path = path
        self.path_length = len(path)
        self.a_star_executions = a_star_executions
        self.total_iteration = total_iteration
        self.time_elapsed = time_elapsed
        self.total_cost = 0
        for cell in path:
            self.total_cost += cell.weight
