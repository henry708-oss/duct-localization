
#define a method for the centroid

#define the carver "Walk"
    #Bias toward straight

#Create a file

import sys
import numpy as np
import random
import matplotlib.pyplot as plt
import math
#import trimesh as tp

#----- BEARING -----
def GetNewBearing():
    newBearing = random.randint(1,6)
    return newBearing

#----- WALK -----
def Walk(position: list, canTurn: bool, shape:tuple):
    #bounds checks flags
    posX = False
    negX = False
    posY = False
    negY = False
    posZ = False
    negZ = False
    if (position[0]+3 < shape[0]-2):
        posX = True
    if (position[0]-3 > 1):
        negX = True
    if (position[1]+3 < shape[1]-2):
        posY = True
    if (position[1]-3 > 1):
        negY = True
    if (position[2]+3 < shape[2]-2):
        posZ = True
    if (position[2]-3 > 1):
        negZ = True

    moved = False
    if canTurn:
        position[3] = GetNewBearing()
    while(not moved):
        match position[3]:
            case 1: #pos x
                if posX:
                    position[0] +=3
                    moved = True
                else:
                    position[3] += 2 #swithc to posY
            case 2:# neg x
                if negX:
                    position[0] -= 3
                    moved = True
                else:
                    position[3] += 2 #switch to negY
            case 3:#pos y
                if posY:
                    position[1] += 3
                    moved = True
                else:
                    position[3] += 2 #switch to posZ
            case 4: #neg y
                if negY:
                    position[1] -= 3
                    moved = True
                else:
                    position[3] += 2 #swith to negZ
            case 5:#pos z
                if posZ:
                    position[2] += 3
                    moved = True
                else:
                    position[3] = 2 #switch to negX
            case 6:# neg z
                if negZ:
                    position[2] -=3
                    moved = True
                else:
                    position[3] = 1 #switch to posX

    
#----- BORE -----
def Bore(matrix, current_pos:list, shape: tuple, mode:int):
    matrix[current_pos[0],current_pos[1],current_pos[2]] = mode #sets self cube to hollow

    #sets flags for bounds checks
    negX = False
    negY = False
    negZ = False
    posX = False
    posY = False
    posZ = False
    if(current_pos[0]-1 >=0):
          negX = True
    if(current_pos[0]+1 < shape[0]):
          posX = True
    if(current_pos[1]-1 >=0):
          negY = True
    if(current_pos[1]+1 < shape[1]):
          posY = True 
    if(current_pos[2]-1 >=0):
          negZ = True
    if(current_pos[2]+1 < shape[2]):
          posZ = True 


    ## FIRST LAYER
    # 1: -x,-y,-z
    if negX and negY and negZ:
        matrix[current_pos[0]-1,current_pos[1]-1,current_pos[2]-1] = mode
    # 2: x,-y,-z
    if negY and negZ:
        matrix[current_pos[0],current_pos[1]-1,current_pos[2]-1] = mode
    # 3: +x,-y,-z
    if posX and negY and negZ:
        matrix[current_pos[0]+1,current_pos[1]-1,current_pos[2]-1] = mode
    # 4:-x,y,-z
    if negX and negZ:
        matrix[current_pos[0]-1,current_pos[1],current_pos[2]-1] = mode
    # 5: x,y,-z ## bottom middle
    if negZ:
        matrix[current_pos[0],current_pos[1],current_pos[2]-1] = mode
    # 6: +x,y,-z
    if posX and negZ:
        matrix[current_pos[0]+1,current_pos[1],current_pos[2]-1] = mode
    # 7: -x,+y,-z
    if negX and posY and negZ:
        matrix[current_pos[0]-1,current_pos[1]+1,current_pos[2]-1] = mode
    # 8: x, +y, -z
    if posY and negZ:
        matrix[current_pos[0],current_pos[1]+1,current_pos[2]-1] = mode
    # 9: +x, +y, -z
    if posX and posY and negZ:
        matrix[current_pos[0]+1,current_pos[1]+1,current_pos[2]-1] = mode

    ## SECOND LAYER
    # 10: -x,-y,z
    if negX and negY:
        matrix[current_pos[0]-1,current_pos[1]-1,current_pos[2]] = mode
    # 11: x,-y,z
    if  negY:
        matrix[current_pos[0],current_pos[1]-1,current_pos[2]] = mode
    # 12: +x,-y,z
    if posX and negY:
        matrix[current_pos[0]+1,current_pos[1]-1,current_pos[2]] = mode
    # 13: -x,y,z
    if negX:
        matrix[current_pos[0]-1,current_pos[1],current_pos[2]] = mode
    # 14: x,y,z --- SELF, SKIP
    # 15: +x,y,z
    if posX:
        matrix[current_pos[0]+1,current_pos[1],current_pos[2]] = mode
    # 16: -x,+y,z
    if negX and posY:
        matrix[current_pos[0]-1,current_pos[1]+1,current_pos[2]] = mode
    # 17: x,+y,z
    if posY:
        matrix[current_pos[0],current_pos[1]+1,current_pos[2]] = mode
    # 18: +x,+y,z
    if posX and posY:
        matrix[current_pos[0]+1,current_pos[1]+1,current_pos[2]] = mode

    ## THIRD LAYER
    # 19: -x,-y,+z
    if negX and negY and posZ:
        matrix[current_pos[0]-1,current_pos[1]-1,current_pos[2]+1] = mode
    # 20: x,-y,+z
    if negY and posZ:
        matrix[current_pos[0],current_pos[1]-1,current_pos[2]+1] = mode
    # 21: +x,-y,+z
    if posX and negY and posZ:
        matrix[current_pos[0]+1,current_pos[1]-1,current_pos[2]+1] = mode
    # 22: -x,y,+z
    if negX and posZ:
        matrix[current_pos[0]-1,current_pos[1],current_pos[2]+1] = mode
    # 23: x,y,+z
    if posZ:
        matrix[current_pos[0],current_pos[1],current_pos[2]+1] = mode
    # 24: +x,y,+z
    if posX and posZ:
        matrix[current_pos[0]+1,current_pos[1],current_pos[2]+1] = mode

    # 25: -x,+y,+z
    if negX and posY and posZ:
        matrix[current_pos[0]-1,current_pos[1]+1,current_pos[2]+1] = mode
    # 26: x,+y,+z
    if posY and posZ:
        matrix[current_pos[0],current_pos[1]+1,current_pos[2]+1] = mode
    # 27: +x,+y,+z
    if posX and posY and posZ:
        matrix[current_pos[0]+1,current_pos[1]+1,current_pos[2]+1] = mode


#----- VOXELS -----
#taken from an ai summary, might be bugged
def matrix_to_gazebo_sdf(matrix, voxel_size=0.1, model_name="matrix_solid"):
    """
    Converts a 3D binary numpy matrix into a Gazebo SDF file consisting of 
    discrete voxels (box primitives).
    """
    sdf_header = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="{model_name}">
    <static>true</static>
"""
    sdf_footer = """  </model>
</sdf>"""
    
    links = []
    # Find indices where matrix element is active (e.g., equals 1)
    z_indices, y_indices, x_indices = np.where(matrix > 0)
    
    for idx, (z, y, x) in enumerate(zip(z_indices, y_indices, x_indices)):
        # Calculate the physical spatial center for each block
        pos_x = x * voxel_size
        pos_y = y * voxel_size
        pos_z = z * voxel_size
        
        link_str = f"""
    <link name="voxel_{idx}">
      <pose>{pos_x} {pos_y} {pos_z} 0 0 0</pose>
      <collision name="collision_{idx}">
        <geometry>
          <box><size>{voxel_size} {voxel_size} {voxel_size}</size></box>
        </geometry>
      </collision>
      <visual name="visual_{idx}">
        <geometry>
          <box><size>{voxel_size} {voxel_size} {voxel_size}</size></box>
        </geometry>
        <material>
          <ambient>0.2 0.6 0.2 1</ambient>
          <diffuse>0.2 0.6 0.2 1</diffuse>
        </material>
      </visual>
    </link>"""
        links.append(link_str)
        
    full_sdf = sdf_header + "".join(links) + sdf_footer
    return full_sdf

#----- VISUALIZER -----
def Vis(matrix):
    ####### below taken from google ai summary. Creates a plot visualizer. Turn this into a "vis" func. 
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Render the matrix as solid voxels
    # 'edgecolor' outlines the individual blocks to give a true grid feeling
    # alpha controls transparency. 
    ax.voxels(matrix, edgecolor=None, facecolors='cyan', alpha=0.3)

    # Set labels and show
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Carver Demo')
    plt.show()  

#----- MAIN -----
#create a matrix using CL args
if (len(sys.argv)<4):
    print("To use, input: **python carver.py mat_dim_x mat_y mat_z mode")
    print("Example: python3 carver.py 30 30 30")
    print("x, y, z must be greater than 30")
    print("mode 0 for carver, mode 1 for extruder")
    sys.exit(1)

x = int(sys.argv[1])
y = int(sys.argv[2])
z = int(sys.argv[3])
mode = int(sys.argv[4]) #if 0, then output is a solid with chennels
                        #if 1, then output is the channels as solids; a "negative" of the map

if (x < 30) or (y < 30) or (z < 30):
    print("Matrix must be at least 30x30x30")
    sys.exit(1)

shape = (x,y,x)
if mode:
    matrix_solid = np.zeros(shape, dtype=bool)
else:
    matrix_solid = np.ones(shape, dtype=bool)

#create random starting point on the X,Z plane at least 6 voxels in to the solid
cur_x = random.randint(6, x-7)
cur_y = 4
cur_z = random.randint(6, z-7)


#bearing determines which way the "drill" moves. 1 = pos x, 2 neg x, 3 pos y, 4 neg y, 5 pos z, 6 neg z
#always starts drilling into the cube
cur_bearing = 3
cur_pos = [cur_x, cur_y, cur_z, cur_bearing]
set_pos = cur_pos
print(cur_pos)

for i in range(5):
    Bore(matrix_solid,set_pos,shape, mode)
    set_pos[1]-=1

running = True
canTurn = False
iters = math.floor(x**1.65) 
print(iters)
while(running):
    turnBias = random.randint(0,4) #about a %20 chance to fork path on each iteration
    match turnBias:                #creates a bias toward straight channels
        case 4:
            canTurn = True
            Walk(cur_pos, canTurn, shape)
            canTurn = False
        case _:
            Walk(cur_pos, canTurn, shape)
    Bore(matrix_solid, cur_pos, shape, mode)
    iters-=1
    if iters < 0:
        running = False


#voxelize and save to file
#vox_mat = matrix_to_gazebo_sdf(matrix_solid, voxel_size=.02)   
#with open("model.sdf", "w") as f:
#    f.write(vox_mat)
#print("SDF file generated successfully as 'model.sdf'!")

Vis(matrix_solid)
