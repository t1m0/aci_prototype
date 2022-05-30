import glob
import imageio
import os
def generate_gifs(base_file_names):
    for base_file_name in [base_file_names[0]]:
        files = [f for f in glob.glob('Visualization/'+base_file_name+"*.png", recursive=False)]
        files.sort(key=os.path.getmtime)
        export_name='Visualization/'+base_file_name+".gif"
        frames = []
        for file in files:
            image = imageio.imread(file)
            frames.append(image)
            os.remove(file)
        kargs = { 'duration': 0.05 }
        print(f"Saving {export_name}")
        imageio.mimsave(export_name, frames, 'GIF', **kargs)
