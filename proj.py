import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm#for color selection
import itertools

#######################################################################################################
#function to project onto the plane
#takes normal vector of the plane, a point on the plane and vertices to be projected as argument
#returns the position vector of the projected point on the plane
#######################################################################################################
def planeprojection(normalvector,centroid,vertices):
    shape = vertices.shape#shape of vertex array, can be one vertex or multiple vertices to project
    if len(shape)==1:#meaning there is only one vertex
        vertex = vertices
        #dot product of position vector to the vertex from plane and normal vector
        dotscalar = np.dot(np.subtract(vertex,centroid),normalvector)
        #now returning the position vector of the projection onto the plane
        return np.subtract(vertex,dotscalar*normalvector)
    else:
        #array to store projectedvectors
        projectedvectors = np.zeros((shape[0],shape[1]))
        #now projecting onto plane, one by one
        for counter in range(shape[0]):
            vertex = vertices[counter,:]
            print (vertex)
            dotscalar = np.dot(vertex - centroid,normalvector)
            print (dotscalar)
            #now returning the position vector of the projection onto the plane
            projectedvectors[counter,:] = np.subtract(vertex,dotscalar*normalvector)
        #now returning the vectors projected
        return projectedvectors
#######################################################################################################
###normalising function
#######################################################################################################
def normalise(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm
##############################################################################################################
##########points to project####################
##############################################################################################################
xcod = float(input("X coordinate:"))
ycod = float(input("Y coordinate:"))
zcod = float(input("Z coordinate:"))
# xcod = np.array([1,2,1,3,-1,1])
# ycod = np.array([2,1,4.5,5.,6,2])
# zcod = np.array([1,-2,0,2,3,1])
num = 1
# num = len(xcod)-1
#centroid of the cell
# centroid = np.array([np.mean(xcod[0:num]),np.mean(ycod[0:num]),np.mean(zcod[0:num])])
#getting tuples of x,y,z
verts = [[xcod,ycod,zcod]]
#numpy array of vertices
vertices =np.array(verts)
centroid = np.array([[0,0,0]])
print("vertices",vertices)
#normal to the plane
averagenormal = np.array([ 1, 0 ,  0 ])
#Projecting the vertices now
projectedvertices = planeprojection(averagenormal,centroid,vertices)
#changing the format to tuple for plotting polyhedron surface
projectedverts = [projectedvertices]
print("projectedvert",projectedverts)
################################################################################
######plotting #################################################################
################################################################################
#also defining the plot in 3d for start plotting
fig = plt.figure()
ax = fig.add_subplot(111,projection = '3d')
#plotting all the points
ax.plot([xcod],[ycod],[zcod],'x-')
#plotting polyhedron surface
ax.add_collection3d(Poly3DCollection(projectedverts, color="g"))
#adding labels for vertice
# for i in range(num):
    # ax.text(xcod[i],ycod[i],zcod[i],'%d(%.2f,%.2f,%.2f)'%(i,xcod[i],ycod[i],zcod[i]))
ax.text(xcod,ycod,zcod,'(%.2f,%.2f,%.2f)'%(xcod,ycod,zcod))

#plotting averagenormal vector point
# ax.scatter(averagenormal[0],averagenormal[1],averagenormal[2],marker = 'o',color="g")
#plotting centroid 
# ax.scatter(centroid[0],centroid[1],centroid[2],marker = 'o',color="g")
#plotting averagenormal vector point from centroid
# ax.scatter(averagenormal[0]+centroid[0],averagenormal[1]+centroid[1],averagenormal[2]+centroid[2],marker = 'o',color="g")#plot show
ax.set_xlim([-1,5])
ax.set_ylim([-1,6])
ax.set_zlim([-5,6])
plt.show()
