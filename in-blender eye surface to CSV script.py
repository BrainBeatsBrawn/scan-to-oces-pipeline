import bpy
import bmesh
import mathutils
import csv
import math
import os.path
from functools import reduce

def distance(vector1, vector2) -> float: 
    return (vector1 - vector2).length

def converVectorToGlobal(vector_to_transform, global_transform):
    return mathutils.Matrix(global_transform) @ mathutils.Vector(vector_to_transform).to_4d()


def converNormalToGlobal(vector_to_transform, global_transform):
    return global_transform.to_3x3().inverted().transposed() @ vector_to_transform

def getAverageRadius(face_verts, face_center):
    #find radius of each vector from mid point
    all_radius = 0
    for v in face_verts:
        all_radius += distance(v, face_center)
    return all_radius/len(face_verts)

def averageIOAngle(face) -> float:
    #get neighbouring faces and calculate the angle between them
    neighbour_faces = [fa for e in face.edges for fa in e.link_faces if fa is not face]
    
    #check current face normal isn't 0,0,0
    if face.normal == mathutils.Vector((0,0,0)):
        raise ValueError("Error: Normal of face is 0,0,0")
    
    #check current face has a neighboring face
    if len(neighbour_faces) == 0:
        raise ValueError("Error: Face is not connected to any other faces.")
        
    #get angle between neighbouring face
    neighbour_faces_all_angles = 0
    for nf in neighbour_faces:
        #check neighbour face vector isn't 0,0,0
        if nf.normal == mathutils.Vector((0,0,0)):
            raise ValueError("Error: Normal of neighbouring face is 0,0,0")
                
        neighbour_faces_all_angles += normal.angle(nf.normal)
        
    return neighbour_faces_all_angles/ len(neighbour_faces)


FILE_SCALE = 1 # 1mm is '1' (the value here) in this file
TARGET_SCALE = 0.001 # 1mm is '0.001' in the target file.

scale_factor = TARGET_SCALE/FILE_SCALE

save_path = bpy.path.abspath("//")

data = []

object = bpy.context.selected_objects[0]
mesh = object.data

world_transform = mathutils.Matrix(object.matrix_world)
#world_transform.invert()
print("\tworld_vec")
print(world_transform)

b_mesh = bmesh.new()
b_mesh.from_mesh(mesh)

#bmesh.new().from_mesh(bpy.data.meshes['Plane'])

for f in b_mesh.faces:
    normal = f.normal
    center_median = mathutils.Vector(f.calc_center_median())
    #print(f.normal)
    #print(mathutils.Vector(f.calc_center_median()))
    
    global_verts = []
    for v in f.verts:
        global_verts.append(converVectorToGlobal(mathutils.Vector(v.co), world_transform))
    
    #Convert vectors to global, normalize normals just in case
    global_center = converVectorToGlobal(center_median,world_transform)*scale_factor
    global_norm = converNormalToGlobal(normal,world_transform)
    global_norm.normalize()
    
    avg_radius = getAverageRadius(global_verts, global_center)*scale_factor
    avg_io_angle = averageIOAngle(f)
    
    #cacluclate distance back from the lens
    # k = R/tan(IO/2))
    
    focal_point_offset = avg_radius/ math.tan(avg_io_angle/2)
        
        
    #add data to object and convert vectors to global
    data_packet = {
            "center": global_center, 
#            "normal": converVectorToGlobal(normal,world_transform.Rotation), 
            "normal": global_norm, 
            "radius": avg_radius, 
            "interommatidial_angle":avg_io_angle,
            "focal_point_offset": focal_point_offset
        }
    print("Normalized:", data_packet["normal"])
    data.append(data_packet)
    
    #print("Face with:")
    #print("\tNormal:", normal)
    #print("\tCenter Median:", center_median)
    #print("\tVertices:", vertices)  
    #print("\tAverage Radius:", avg_radius)
    #print("\tNeighbourface:", neighbour_faces)
    #print("\t Average Angle neighbours:",avg_io_angle)
    
eyewide_avg_io_angle = reduce(lambda n,m:n+m, [d["interommatidial_angle"] for d in data], 0)/len(data)
print("Eye-wide average interommatidial angle:", eyewide_avg_io_angle)
print("Eye-wide average interommatidial angle (degrees):", math.degrees(eyewide_avg_io_angle))

with open(os.path.join(save_path,"eye_data.csv"), "w", newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(
        ["center_x", "center_y", "center_z",
         "normal_x", "normal_y", "normal_z",
         "interommatidial_angle",
         "focal_point_offset",
         "radius", 
         ])
    
    for d in data:
        file_writer.writerow(
            [
             d["center"][0], d["center"][1], d["center"][2],
             d["normal"][0], d["normal"][1], d["normal"][2],
             d["interommatidial_angle"],
             d["focal_point_offset"],
             d["radius"]
            ])
        

#bpy.data.texts[0].as_module()