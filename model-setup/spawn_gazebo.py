'''
Generate gazebo from mazecarver and maze.stl  
'''
import sys
import random
import math
import numpy as np
import subprocess
import time
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

models_path = proj_root.parent / "mrs_uav_gazebo_simulator" / "models"

os.environ["GZ_SIM_RESOURCE_PATH"] = (
    str(models_path) + os.pathsep
    + str(proj_root / "model-setup") + os.pathsep
    + os.environ.get("GZ_SIM_RESOURCE_PATH", "")
)

def generate_maze(model_name):
    mode = 1
    shape = (100,100,100)
    matrix = np.zeros(shape, dtype=bool)
    carve_matrix = mz.Carve(matrix, mode)
  
# Returns the carved matrix on success, None on error.
    if carve_matrix is None:
        raise RuntimeError("Maze generation failed")
    
    spawn_position = random_spawn(carve_matrix)
    print("Drone spawn position:", spawn_position)
    
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
    #Taken from AI
    subprocess.Popen(["gz", "sim", "-r", "empty.sdf"])
    time.sleep(5)
    for name, path, position in [
        (model_name, sdf_output, (0, 0, 0)),
        ("x500", proj_root.parent / "x500.sdf", spawn_position)
    ]:
        x, y, z = position
        request = (
            f'sdf_filename: "{path}", name: "{name}", '
            f'pose: {{position: {{x: {x}, y: {y}, z: {z}}}}}'
        )

        subprocess.run([
            "gz", "service",
            "-s", "/world/empty/create",
            "--reqtype", "gz.msgs.EntityFactory",
            "--reptype", "gz.msgs.Boolean",
            "--timeout", "5000",
            "--req", request
        ], check=True)
    (model_dir / "model.sdf").write_text(sdf)

# to be implemented
def random_spawn(matrix):
    random_point = np.argwhere(matrix)
    position = random.choice(random_point.tolist())
    return position

if __name__ == "__main__":
    generate_maze("cave1")
