from Application.Map import Map
import numpy as np
import matplotlib.pyplot as plt

weight_to_color_map = {
    -1 : [255,153,255], # path
    -10 : [255,255,0], # start node
    -11 : [255,128,0], # end node
    3000 : [51,0,102], # obstacle
    4000 : [255, 95, 31], # security_guard
    1 : [210,210,210], # house
    5 : [70,70,70], # road
    7 : [128,128,128], # gravel road
    9 : [112,215,0], # gras
    15 : [173,132,86], # stone garden
    25 : [0,0,255], # water shallow
    35 : [0,0,128],  # water deep
    50 : [116, 14, 5], # camera center
    40 : [136, 17, 6], # camera center
    30 : [155, 19, 6], # camera center
    20 : [175, 22, 7], # camera center
    10 : [194, 24, 8], # camera center
    100 : [0,128,0], # tree
}

'''create a 3d version of the original 2d map and colorize all the different elements in the map'''
def plot_map(map:Map, path):
    testmap = map.map_data.to_numpy()
    height, width = testmap.shape
    map_image = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            current_weight = testmap[i][j]
            if current_weight in weight_to_color_map.keys():
                map_image[i][j] = weight_to_color_map[current_weight]
            else:
                print(f"Weight {current_weight} not found!")
                map_image[i][j] = [0,0,0]
    for cell in path:
        if cell != map.startpoint and cell != map.endpoint:
            row, col = cell.get_pos()
            map_image[row][col] = weight_to_color_map[-1]
    for security_guard in map.security_guards:
        for cell in security_guard.movement:
            row, col = cell.get_pos()
            map_image[row][col] = weight_to_color_map[4000]
    plt.figure(figsize = (10,10))
    plt.imshow(map_image)
    ax = plt.gca()
    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, height, 1))
    ax.set_xticklabels(np.arange(0, width, 1))
    ax.set_yticklabels(np.arange(0, height, 1))
    ax.xaxis.tick_top()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.grid(color=[0.8,0.8,0.8], linestyle='-', linewidth=0.5)
    plt.show()
