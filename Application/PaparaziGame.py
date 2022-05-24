import glob
from Application.Map import Map
import time
from Application.Astar import A_Star
from Application.PathFindingResult import PathFindingResult
import pathlib

import pandas as pd

class PaparaziGame:

    heuristics = [None, "Manhattan", "Euclidean", "Chebyshev"]
    
    def play(self, map_root_dir, num_of_repetition = 10):
        maps = self.__load_maps(map_root_dir)
        results = []
        for map in maps:
            for heuristic in self.heuristics:
                for i in range(num_of_repetition): # repeat each pathfinding for a certain number and store the results
                    starttime = time.time()
                    path, total_cost, total_iteration = A_Star(map, heuristic)
                    time_elapsed = 1000 * (time.time() - starttime) # time in ms
                    result = PathFindingResult(map, str(heuristic), path, total_cost, total_iteration, time_elapsed)
                    results.append(result)
        return results
        
    def __load_maps(self, map_root_dir):
        maps = []
        files = [f for f in glob.glob(map_root_dir+"**/*.csv", recursive=True)]
        for file in files:
            pure_path = pathlib.PurePath(file)
            map_data = pd.read_csv(file, header=None)
            map_name = pure_path.name.replace(".csv","")
            print(map_name)
            maps.append(Map(map_name, map_data))
        return maps

    
    
    