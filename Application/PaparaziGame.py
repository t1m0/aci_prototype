import glob
from Application.Map import Map
import time
from Application.Astar import A_Star
from Application.Paparazi import Paparazi
from Application.PathFindingResult import PathFindingResult
from Application.plot_map import plot_map
import pathlib

import pandas as pd

class PaparaziGame:

    heuristics = [None, "Manhattan", "Euclidean", "Chebyshev"]
    
    def play(self, map_root_dir, num_security_guards=3):
        maps = self.__load_maps(map_root_dir, num_security_guards)
        results = []
        for map in maps:
            for heuristic in self.heuristics:
                print(f"Started {map.name} with {heuristic} heuristic")
                starttime = time.time()
                paparazi = Paparazi(map.startpoint)
                total_iteration = 0
                time_elapsed = 0
                intermediate_info_count = 0
                while(paparazi.get_current_cell() != map.endpoint):
                    path, total_cost, iterations = A_Star(map, paparazi.get_current_cell(), heuristic)
                    next_cell = self.__find_next_move(paparazi.get_current_cell(), path)
                    paparazi.move(next_cell)
                    map.move_security_guards()
                    total_iteration += 1
                    time_elapsed = 1000 * (time.time() - starttime)
                    if ((time_elapsed / 60000) - intermediate_info_count*60000) > 15:
                        print(f"Running longer than 15min currently at iteration {total_iteration}")
                        plot_map(map, paparazi.path)
                        intermediate_info_count += 1
                time_elapsed = 1000 * (time.time() - starttime) # time in ms
                print(f"Finished {map.name} with {heuristic} heuristic in {total_iteration} iterations and {round(time_elapsed,2)}ms")
                plot_map(map,paparazi.path)
                result = PathFindingResult(map, str(heuristic), paparazi.path, total_iteration, time_elapsed)
                results.append(result)
                map.place_security_guards()
        return results
        
    def __load_maps(self, map_root_dir, num_security_guards):
        maps = []
        files = [f for f in glob.glob(map_root_dir+"**/*.csv", recursive=True)]
        for file in files:
            pure_path = pathlib.PurePath(file)
            map_data = pd.read_csv(file, header=None)
            map_name = pure_path.name.replace(".csv","")
            print(map_name)
            maps.append(Map(map_name, map_data,num_security_guards))
        return maps
    
    def __find_next_move(self,current, path):
        current_index = path.index(current)
        current_index += 1
        return path[current_index]

    
    
    