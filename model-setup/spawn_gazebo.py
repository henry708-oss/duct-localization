'''
Generate gazebo from mazecarver and maze.stl  
'''
import sys
import random
import math
import numpy as np
# import matplotlib.pyplot as plt
# import trimesh as tri
# from skimage import measure
from pathlib import Path

# import carver as cv
import os
# modelname/ meshes / model.stl
# modelname / model_config / model.sdf
#root directory
proj_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root / "Cave Carver Testing"))

import mazecarver as mz

def generate_maze(model_name):
    mode = 1
    shape = (100,100,100)
    matrix = np.zeros(shape, dtype=bool)
    carve_matrix = mz.Carve(matrix, mode)
  
# Returns the carved matrix on success, None on error.
    if carve_matrix is None:
        raise RuntimeError("Maze generation failed")
    

    #<model name>
	#<meshes>
	#	model.stl
	#model.config
	#model.sdf
#From root directory to model name, meshes, and handles making directory    
    model_dir = proj_root / "model-setup" / model_name
    meshes_dir = model_dir / "meshes"
    config_dir = proj_root / "model-setup" / "my_stl_model" / "model.config"
    sdf_dir = proj_root / "model-setup" / "my_stl_model" / "model.sdf"
    os.makedirs(meshes_dir,exist_ok = True)
    mz.CreateMesh(carve_matrix, str(meshes_dir / "model"))

    config = config_dir.read_text().replace("my_stl_model", model_name)
    config_output = model_dir / "model.config"
    config_output.write_text(config)
    
    sdf = sdf_dir.read_text().replace("my_stl_model", model_name)
    sdf_output = model_dir / "model.sdf"
    sdf_output.write_text(sdf)
    #(model_dir / "model.sdf").write_text(sdf)

if __name__ == "__main__":
    generate_maze("cave1")
