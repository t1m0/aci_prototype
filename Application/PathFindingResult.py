import uuid
class PathFindingResult:
    
    def __init__(self,name,map,heuristic,path,a_star_executions,total_iteration,time_elapsed,diagonal_movement,num_security_guards,smart_path_finding):
        self.name = name
        self.map = map
        self.heuristic = heuristic
        self.path = path
        self.path_length = len(path)
        self.a_star_executions = a_star_executions
        self.total_iteration = total_iteration
        self.time_elapsed = time_elapsed
        self.total_cost = 0
        self.diagonal_movement = diagonal_movement
        self.num_security_guards = num_security_guards
        self.smart_path_finding = smart_path_finding
        for cell in path:
            self.total_cost += cell.weight
