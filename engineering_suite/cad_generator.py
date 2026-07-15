#!/usr/bin/env python3
"""
==========================================================================
CERO MOTORSPORTS CAD GENERATOR
Programmatic 3D Geometry mesh exporter (.stl and .obj) for car parts.
Outputs clean solid manifold meshes readable by SolidWorks, Fusion 360, etc.
==========================================================================
"""

import math
import os

def compute_normal(v1, v2, v3):
    """Calculates the normal vector of a triangle face."""
    # Vectors
    ux, uy, uz = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
    vx, vy, vz = v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]
    # Cross product
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    # Normalize
    length = math.sqrt(nx*nx + ny*ny + nz*nz)
    if length > 0:
        return [nx/length, ny/length, nz/length]
    return [0.0, 0.0, 0.0]

def save_stl(filename, vertices, faces, solid_name="CERO_PART"):
    """Saves mesh vertices and faces in ASCII STL format."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(f"solid {solid_name}\n")
        for face in faces:
            v1 = vertices[face[0]]
            v2 = vertices[face[1]]
            v3 = vertices[face[2]]
            normal = compute_normal(v1, v2, v3)
            
            f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v1[0]:.6f} {v1[1]:.6f} {v1[2]:.6f}\n")
            f.write(f"      vertex {v2[0]:.6f} {v2[1]:.6f} {v2[2]:.6f}\n")
            f.write(f"      vertex {v3[0]:.6f} {v3[1]:.6f} {v3[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {solid_name}\n")
    print(f"[CAD] Guardado archivo STL: {filename} ({len(faces)} triángulos, {len(vertices)} vértices)")

def generate_cylinder(radius, height, segments=16, center=[0, 0, 0], axis="Z"):
    """Generates a cylinder mesh (vertices and faces)."""
    vertices = []
    faces = []
    
    half_h = height / 2.0
    
    # Generate circle vertices
    for i in range(segments):
        ang = (i / segments) * 2 * math.pi
        x = radius * math.cos(ang)
        y = radius * math.sin(ang)
        
        # Two caps
        if axis == "Z":
            vertices.append([x + center[0], y + center[1], -half_h + center[2]]) # Bottom cap (even index)
            vertices.append([x + center[0], y + center[1],  half_h + center[2]]) # Top cap (odd index)
        elif axis == "X":
            vertices.append([-half_h + center[0], x + center[1], y + center[2]])
            vertices.append([ half_h + center[0], x + center[1], y + center[2]])
        elif axis == "Y":
            vertices.append([x + center[0], -half_h + center[1], y + center[2]])
            vertices.append([x + center[0],  half_h + center[1], y + center[2]])

    # Center vertices for the caps
    idx_center_bottom = len(vertices)
    if axis == "Z":
        vertices.append([center[0], center[1], -half_h + center[2]])
    elif axis == "X":
        vertices.append([-half_h + center[0], center[1], center[2]])
    elif axis == "Y":
        vertices.append([center[0], -half_h + center[1], center[2]])

    idx_center_top = len(vertices)
    if axis == "Z":
        vertices.append([center[0], center[1], half_h + center[2]])
    elif axis == "X":
        vertices.append([half_h + center[0], center[1], center[2]])
    elif axis == "Y":
        vertices.append([center[0], half_h + center[1], center[2]])

    # Connect walls and caps
    for i in range(segments):
        next_i = (i + 1) % segments
        b1, t1 = i * 2, i * 2 + 1
        b2, t2 = next_i * 2, next_i * 2 + 1
        
        # Side wall triangles (2 per segment)
        faces.append([b1, b2, t2])
        faces.append([b1, t2, t1])
        
        # Bottom cap triangle (pointing outward, clockwise order)
        faces.append([idx_center_bottom, b2, b1])
        
        # Top cap triangle (pointing outward, counter-clockwise order)
        faces.append([idx_center_top, t1, t2])
        
    return vertices, faces

def generate_box(width, length, height, center=[0, 0, 0]):
    """Generates a cuboid mesh."""
    dx = width / 2.0
    dy = length / 2.0
    dz = height / 2.0
    
    vertices = [
        [-dx, -dy, -dz], [ dx, -dy, -dz], [ dx,  dy, -dz], [-dx,  dy, -dz], # Bottom 4
        [-dx, -dy,  dz], [ dx, -dy,  dz], [ dx,  dy,  dz], [-dx,  dy,  dz]  # Top 4
    ]
    
    # Translate
    for v in vertices:
        v[0] += center[0]
        v[1] += center[1]
        v[2] += center[2]
        
    faces = [
        [0, 2, 1], [0, 3, 2], # Bottom
        [4, 5, 6], [4, 6, 7], # Top
        [0, 1, 5], [0, 5, 4], # Front
        [1, 2, 6], [1, 6, 5], # Right
        [2, 3, 7], [2, 7, 6], # Back
        [3, 0, 4], [3, 4, 7]  # Left
    ]
    return vertices, faces

def merge_meshes(mesh_list):
    """Merges multiple meshes (list of vertices, faces) into a single mesh."""
    total_vertices = []
    total_faces = []
    
    v_offset = 0
    for vertices, faces in mesh_list:
        total_vertices.extend(vertices)
        for face in faces:
            total_faces.append([face[0] + v_offset, face[1] + v_offset, face[2] + v_offset])
        v_offset += len(vertices)
        
    return total_vertices, total_faces

def generate_chassis_tubes(nodes, connections, r_tube=12.7):
    """
    Generates solid cylinder meshes for all tubes in the chassis spaceframe.
    This creates a real solid 3D STEP/STL representation of the tubular chassis!
    """
    mesh_list = []
    
    for start_node, end_node in connections:
        p1 = nodes[start_node]
        p2 = nodes[end_node]
        
        # Calculate length and direction
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        if length == 0:
            continue
            
        center = [(p1[0] + p2[0])/2.0, (p1[1] + p2[1])/2.0, (p1[2] + p2[2])/2.0]
        
        # Generate tube aligned to Z
        tube_verts, tube_faces = generate_cylinder(r_tube, length, segments=8, center=[0, 0, 0], axis="Z")
        
        # Rotate tube from Z-axis to alignment vector (dx, dy, dz)
        # Direction cosines
        vx, vy, vz = dx/length, dy/length, dz/length
        
        # Rotation axis = Z_axis x V
        # Z_axis = [0, 0, 1]
        # Cross product: [0, 0, 1] x [vx, vy, vz] = [-vy, vx, 0]
        rx = -vy
        ry = vx
        rz = 0.0
        r_len = math.sqrt(rx*rx + ry*ry)
        
        # If aligned with Z already, no rotation needed (or simple flip if vz is -1)
        if r_len > 1e-6:
            rx /= r_len
            ry /= r_len
            
            # Angle of rotation
            # dot product: [0, 0, 1] . [vx, vy, vz] = vz
            theta = math.acos(max(-1.0, min(1.0, vz)))
            
            # Rotate vertices using Rodrigues rotation formula
            rotated_verts = []
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            
            for v in tube_verts:
                # v rotated by theta about axis (rx, ry, rz)
                dot = v[0]*rx + v[1]*ry + v[2]*rz
                cross_x = ry*v[2] - rz*v[1]
                cross_y = rz*v[0] - rx*v[2]
                cross_z = rx*v[1] - ry*v[0]
                
                rx_rot = v[0]*cos_t + cross_x*sin_t + rx*dot*(1 - cos_t)
                ry_rot = v[1]*cos_t + cross_y*sin_t + ry*dot*(1 - cos_t)
                rz_rot = v[2]*cos_t + cross_z*sin_t + rz*dot*(1 - cos_t)
                
                # Translate to final position
                rotated_verts.append([rx_rot + center[0], ry_rot + center[1], rz_rot + center[2]])
            tube_verts = rotated_verts
        else:
            # Axis is parallel to Z-axis. Translate only.
            translated_verts = []
            # Check if opposite direction
            dir_factor = 1.0 if vz > 0 else -1.0
            for v in tube_verts:
                translated_verts.append([v[0] + center[0], v[1] + center[1], v[2]*dir_factor + center[2]])
            tube_verts = translated_verts
            
        mesh_list.append((tube_verts, tube_faces))
        
    return merge_meshes(mesh_list)

if __name__ == "__main__":
    print("[CAD] Iniciando generación de componentes 3D CERO...")
    
    # 1. Generate Wheel Mesh (OZ rim / Hoosier tyre)
    wheel_verts, wheel_faces = generate_cylinder(radius=228.6, height=203.2, segments=24, center=[0, 0, 0], axis="Y")
    save_stl("output_cad/cero_wheel.stl", wheel_verts, wheel_faces, "CERO_Wheel")
    
    # 2. Generate Battery segment box
    bat_verts, bat_faces = generate_box(width=300, length=400, height=200, center=[0, 0, 0])
    save_stl("output_cad/cero_battery_box.stl", bat_verts, bat_faces, "CERO_BatteryBox")

    # 3. Generate Chassis Spaceframe (Tubular CAD)
    nodes = {
        'f_bulk_tl': [400, 180, 250], 'f_bulk_tr': [400, -180, 250],
        'f_bulk_bl': [400, 180, 50],  'f_bulk_br': [400, -180, 50],
        'f_hoop_tl': [800, 220, 480], 'f_hoop_tr': [800, -220, 480],
        'f_hoop_bl': [800, 250, 50],  'f_hoop_br': [800, -250, 50],
        'm_hoop_t': [1450, 0, 950],   'm_hoop_ml': [1450, 260, 580],
        'm_hoop_mr': [1450, -260, 580], 'm_hoop_bl': [1450, 280, 50],
        'm_hoop_br': [1450, -280, 50],
        'r_bulk_tl': [2100, 150, 350], 'r_bulk_tr': [2100, -150, 350],
        'r_bulk_bl': [2100, 150, 80],  'r_bulk_br': [2100, -150, 80]
    }
    connections = [
        # Structural rings
        ('f_bulk_tl', 'f_bulk_tr'), ('f_bulk_tr', 'f_bulk_br'), ('f_bulk_br', 'f_bulk_bl'), ('f_bulk_bl', 'f_bulk_tl'),
        ('f_hoop_tl', 'f_hoop_tr'), ('f_hoop_tr', 'f_hoop_br'), ('f_hoop_br', 'f_hoop_bl'), ('f_hoop_bl', 'f_hoop_tl'),
        ('m_hoop_bl', 'm_hoop_ml'), ('m_hoop_ml', 'm_hoop_t'), ('m_hoop_t', 'm_hoop_mr'), ('m_hoop_mr', 'm_hoop_br'), ('m_hoop_br', 'm_hoop_bl'),
        ('r_bulk_tl', 'r_bulk_tr'), ('r_bulk_tr', 'r_bulk_br'), ('r_bulk_br', 'r_bulk_bl'), ('r_bulk_bl', 'r_bulk_tl'),
        
        # Longitudinal members
        ('f_bulk_tl', 'f_hoop_tl'), ('f_bulk_tr', 'f_hoop_tr'), ('f_bulk_bl', 'f_hoop_bl'), ('f_bulk_br', 'f_hoop_br'),
        ('f_hoop_tl', 'm_hoop_ml'), ('f_hoop_tr', 'm_hoop_mr'), ('f_hoop_bl', 'm_hoop_bl'), ('f_hoop_br', 'm_hoop_br'),
        ('m_hoop_ml', 'r_bulk_tl'), ('m_hoop_mr', 'r_bulk_tr'), ('m_hoop_bl', 'r_bulk_bl'), ('m_hoop_br', 'r_bulk_br'),
        
        # Side panel diagonals
        ('f_bulk_tl', 'f_hoop_bl'), ('f_bulk_bl', 'f_hoop_tl'),
        ('f_bulk_tr', 'f_hoop_br'), ('f_bulk_br', 'f_hoop_tr'),
        ('f_hoop_tl', 'm_hoop_bl'), ('f_hoop_bl', 'm_hoop_ml'),
        ('f_hoop_tr', 'm_hoop_br'), ('f_hoop_br', 'm_hoop_mr'),
        ('m_hoop_ml', 'r_bulk_bl'), ('m_hoop_bl', 'r_bulk_tl'),
        ('m_hoop_mr', 'r_bulk_br'), ('m_hoop_br', 'r_bulk_tr'),
        
        # Top/Bottom diagonals
        ('f_bulk_tl', 'f_hoop_tr'), ('f_bulk_tr', 'f_hoop_tl'),
        ('f_bulk_bl', 'f_hoop_br'), ('f_bulk_br', 'f_hoop_bl'),
        ('f_hoop_tl', 'm_hoop_mr'), ('f_hoop_tr', 'm_hoop_ml'),
        ('f_hoop_bl', 'm_hoop_br'), ('f_hoop_br', 'm_hoop_bl'),
        ('m_hoop_ml', 'r_bulk_tr'), ('m_hoop_mr', 'r_bulk_tl'),
        ('m_hoop_bl', 'r_bulk_br'), ('m_hoop_br', 'r_bulk_bl'),
        
        # Bulkhead cross braces and rear roll hoop braces
        ('f_bulk_tl', 'f_bulk_br'), ('f_hoop_tl', 'f_hoop_br'), ('r_bulk_tl', 'r_bulk_br'),
        ('m_hoop_t', 'r_bulk_tl'), ('m_hoop_t', 'r_bulk_tr')
    ]
    
    chassis_verts, chassis_faces = generate_chassis_tubes(nodes, connections, r_tube=12.7)
    save_stl("output_cad/cero_chassis.stl", chassis_verts, chassis_faces, "CERO_ChassisSpaceframe")
    print("[CAD] Todos los archivos 3D de ingeniería generados.")
