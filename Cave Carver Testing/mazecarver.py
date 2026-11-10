#Fork of carver.py that lets it be used as a module
#
# Authored by Zach Strahan
#
#

import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import trimesh as tri
from skimage import measure


#----- BEARING -----
def _GetNewBearing():
    newBearing = random.randint(1,6)
    return newBearing

#----- WALK -----
def _Walk(position: list, canTurn: bool, shape:tuple):
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
        position[3] = _GetNewBearing()
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
def _Bore(matrix, current_pos:list, shape: tuple, mode:int):
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

#----- CARVE -----
#The main carver function called from main. 
#Uses, Bore, Walk, and GetNewBearing internally
#Args:
# matrix: A 3d Numpy Array of at least size 30x30x30
# mode: Int value to set mat to. Can be 1 or 0. Should by opposite value of mat.
# Returns the carved matrix on success, None on error.
def Carve(matrix, mode:int):
    shape = np.shape(matrix) # shape[0]=x,[1] = y,[2] = z
    if shape[0] < 30 or shape[1] < 30 or shape[2] < 30:
        return None

    if mode != 0 or mode != 1:
        return None
    #create random starting point on the X,Z plane at least 6 voxels in to the solid
    cur_x = random.randint(6, shape[0]-7)
    cur_y = 4
    cur_z = random.randint(6, shape[2]-7)

    #bearing determines which way the "drill" moves. 1 = pos x, 2 neg x, 3 pos y, 4 neg y, 5 pos z, 6 neg z
    #always starts drilling into the cube
    cur_bearing = 3
    cur_pos = [cur_x, cur_y, cur_z, cur_bearing]
    set_pos = cur_pos
    #print(cur_pos)

    for i in range(5):
        _Bore(matrix,set_pos,shape, mode)
        set_pos[1]-=1

    running = True
    canTurn = False
    iters = math.floor(min(shape)**1.65)
    print(iters)
    while(running):
        turnBias = random.randint(0,4) #about a %20 chance to fork path on each iteration
        match turnBias:                #creates a bias toward straight channels
            case 4:
                canTurn = True
                _Walk(cur_pos, canTurn, shape)
                canTurn = False
            case _:
                _Walk(cur_pos, canTurn, shape)
        _Bore(matrix, cur_pos, shape, mode)
        iters-=1
        if iters < 0:
            running = False
    return matrix

#----- MESH -----
#adapted from an ai summary, might be buggy
def CreateMesh(matrix, model_name: str):
    # Extract surface mesh using Marching Cubes
    verts, faces, normals, values = measure.marching_cubes(matrix, level=0.5)

    # Create a Trimesh object
    mesh = tri.Trimesh(vertices=verts, faces=faces, vertex_normals=normals)

    # Export to STL or OBJ (Gazebo supports STL, OBJ, and DAE)
    outputfile = model_name + ".stl"
    mesh.export(outputfile)

#----- VISUALIZER -----
def Vis(matrix, name, flag):
    #implementation adapted from a google AI summary
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Render the matrix as solid voxels
    # 'edgecolor': if none, does not render. if 'k' renders grid lines
    # alpha controls transparency. 
    ax.voxels(matrix, edgecolor=None, facecolors='cyan', alpha=0.3)

    # Set labels and show
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Carver: Test" + name + "Demo")
    plt.savefig("Test "+name+".png")
    if flag:
        plt.show() 
