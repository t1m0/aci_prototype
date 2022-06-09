import glob
from Application.Map import Map
import time
from Application.Astar import A_Star
from Application.Paparazi import Paparazi
from Application.PathFindingResult import PathFindingResult
from Application.plot_map import plot_map
from Application.generate_gif import generate_gifs
import pathlib

import pandas as pd

class PaparaziGame:

    heuristics = [None, "Manhattan", "Euclidean", "Chebyshev"]
    diagonal_movement_options = [True, False]
    
    def play(self, map_root_dir, num_security_guards=1, iterations=1, selected_map_sizes=[],selected_heuristics=[],smart_path_finding=True):
        maps = self.__load_maps(map_root_dir, num_security_guards, selected_map_sizes)
        if not selected_heuristics:
            selected_heuristics = self.heuristics
        results = []
        for map in maps:
            plot_map(map,[],only_plot_current_position=True)
            for diagonal_movement in self.diagonal_movement_options:
                diagonal_label = 'diagonal' if diagonal_movement else 'no_diagonal' 
                for heuristic in selected_heuristics:
                    print(f"Started {map.name} with {heuristic} heuristic")
                    for iteration in range(iterations):
                        print(f"Iteration {iteration} of {iterations}")
                        start_time = time.time()
                        paparazi = Paparazi(map.startpoint)
                        total_iteration = 0
                        time_elapsed = 0
                        intermediate_info_count = 0
                        iteration_name = time.strftime("%d%m%Y")+"_"+map.name + "_" + diagonal_label + "_" + str(heuristic) + "_" + str(iteration)
                        path = []
                        a_star_executions = 0
                        while(self.__is_not_finished(paparazi,map)):
                            path, a_star_executions = self.__update_path_if_required(paparazi,map,heuristic,path,a_star_executions,smart_path_finding,diagonal_movement)
                            next_cell = self.__find_next_move(paparazi.get_current_cell(), path)
                            paparazi.move(next_cell)
                            map.move_security_guards()
                            total_iteration += 1
                            time_elapsed = self.__time_elapsed(start_time)
                            intermediate_info_count = self.__plot_current_state(map, paparazi, iteration_name, time_elapsed, total_iteration, intermediate_info_count)
                        print(f"Finished {map.name} ({diagonal_label}) with {heuristic} heuristic in {total_iteration} iterations and {time_elapsed}min with {a_star_executions} A* executions")
                        plot_map(map,paparazi.path)
                        result = PathFindingResult(iteration_name, map.name, str(heuristic), paparazi.path, a_star_executions, total_iteration, time_elapsed, diagonal_movement, num_security_guards, smart_path_finding)
                        results.append(result)
                        map.place_security_guards()
                        generate_gifs([iteration_name])
        return results
        
    def __load_maps(self, map_root_dir, num_security_guards, selected_map_sizes):
        maps = []
        files = [f for f in glob.glob(map_root_dir+"**/*.csv", recursive=True)]
        for file in files:
            pure_path = pathlib.PurePath(file)
            map_data = pd.read_csv(file, header=None)
            map_name = pure_path.name.replace(".csv","")
            print(map_name)
            map = Map(map_name, map_data,num_security_guards)
            if not selected_map_sizes:
                maps.append(map)
            elif map.size in selected_map_sizes:
                maps.append(map)
            else:
                print(f"Skipping map of size {map.size}")
        return maps
    
    def __update_path_if_required(self,paparazi, map, heuristic, path, a_star_executions, smart_path_finding,diagonal_movement):
        if not path or map.security_guard_in_close_proximity(paparazi.get_current_cell()) or not smart_path_finding:
            path, total_cost, a_star_iterations = A_Star(map, paparazi.get_current_cell(), heuristic, diagonal_movement)
            a_star_executions += 1
        return path, a_star_executions


    def __find_next_move(self,current, path):
        current_index = path.index(current)
        current_index += 1
        return path[current_index]

    def __time_elapsed(self,start_time):
        time_elapsed = 1000 * (time.time() - start_time) # time in ms
        return round((time_elapsed/60000),2) # time in min    
    
    def __is_not_finished(self, paparazi:Paparazi, map:Map):
        return paparazi.get_current_cell() != map.endpoint
    
    def __plot_current_state(self, map, paparazi, iteration_name, time_elapsed, total_iteration, intermediate_info_count):
        plot_name = iteration_name + "_" + str(total_iteration) + ".png"
        plot_map(map, paparazi.path, save_image=True, plot_name=plot_name, only_plot_current_position=True)
        if (time_elapsed > 15) and (not self.__is_not_finished(paparazi,map)):
            print(f"Running longer than 15min currently at iteration {total_iteration} and {time_elapsed}min")
            plot_map(map, paparazi.path)
            intermediate_info_count += 1
        return intermediate_info_count