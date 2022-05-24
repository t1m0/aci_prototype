import uuid
class PathFindingResult:
    uuid = None
    time_elapsed = None
    total_iteration = None
    total_cost = None
    path_length = None
    path = None
    heuristic = None
    map = None
    
    def __init__(self,map,heuristic,path,total_cost,total_iteration,time_elapsed):
        self.uuid = uuid.uuid1()
        self.map = map
        self.heuristic = heuristic
        self.path = path
        self.path_length = len(path)
        self.total_cost = total_cost
        self.total_iteration = total_iteration
        self.time_elapsed = time_elapsed