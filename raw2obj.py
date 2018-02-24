import numpy as np
import scipy.misc
import mcubes
import argparse
import binvox
from sklearn.neighbors import NearestNeighbors


parser = argparse.ArgumentParser(description='Visualise the 3D volume')

parser.add_argument('--volume', dest='volume',
                    help="The volume to render")
parser.add_argument('--dim', dest='dim',
                    help="The dim of volume")
parser.add_argument('--obj', dest='obj',
                    help="The file path of the object")

args = parser.parse_args()


with open(args.volume, 'rb') as f:
    vol = binvox.read_as_coord_array(f).data
vol = binvox.sparse_to_dense(vol,int(args.dim))

vol = vol.astype(float)

vertices, triangles = mcubes.marching_cubes(vol, 0)
#vertices = vertices[:,(2,1,0)]
#vertices[:,2] *= 0.5 # scale the Z component correctly
vc = vertices


with open(args.obj, 'w') as f:
    for v in range(0,vc.shape[0]):
        f.write('v %0.2f %0.2f %0.2f\n' % (vc[v,0],vc[v,1],vc[v,2]))

    for t in range(0,triangles.shape[0]):
        f.write('f {} {} {}\n'.format(*triangles[t,:]+1))

print('Calculated the isosurface.')
