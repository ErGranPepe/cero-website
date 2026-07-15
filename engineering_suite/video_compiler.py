#!/usr/bin/env python3
"""
==========================================================================
CERO MOTORSPORTS REAL VIDEO COMPILER
Parses engineering STL meshes, reads vehicle dynamics CSV telemetry logs,
and compiles a high-fidelity vertical Reel (1080x1920 @ 60 FPS) in MP4.
Uses OpenCV for graphics and Matplotlib for dynamic telemetry plots.
==========================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import os

def read_ascii_stl(filename):
    """Parses an ASCII STL mesh file and returns vertices and facet faces."""
    vertices = []
    print(f"[COMPILER] Leyendo malla STL: {filename}...")
    if not os.path.exists(filename):
        print(f"[COMPILER] ERROR: El archivo {filename} no existe.")
        return None, None
        
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("vertex"):
                parts = line.split()
                # Parse vertex coordinates
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                
    # Every 3 vertices form a triangle face
    faces = [[i, i+1, i+2] for i in range(0, len(vertices), 3)]
    print(f"[COMPILER] Malla cargada. {len(faces)} triángulos.")
    return np.array(vertices), faces

def read_telemetry(filename):
    """Loads CSV telemetry output from vehicle dynamics simulator."""
    time_data = []
    steer_data = []
    speed_data = []
    g_data = []
    x_data = []
    y_data = []
    
    if not os.path.exists(filename):
        print(f"[COMPILER] ERROR: Telemetría {filename} no encontrada.")
        return None
        
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # skip header
        for row in reader:
            time_data.append(float(row[0]))
            steer_data.append(float(row[1]))
            speed_data.append(float(row[2]))
            g_data.append(float(row[5])) # LatG
            x_data.append(float(row[6]))
            y_data.append(float(row[7]))
            
    return {
        'time': np.array(time_data),
        'steer': np.array(steer_data),
        'speed': np.array(speed_data),
        'g': np.array(g_data),
        'x': np.array(x_data),
        'y': np.array(y_data)
    }

def project_3d_points(points, cx, cy, scale, rotX, rotY, cam_dist=4.0):
    """Projects 3D points onto a 2D viewport using camera matrices."""
    # Rotate Y
    c_y, s_y = np.cos(rotY), np.sin(rotY)
    ry_mat = np.array([
        [c_y, 0, -s_y],
        [0, 1, 0],
        [s_y, 0, c_y]
    ])
    
    # Rotate X
    c_x, s_x = np.cos(rotX), np.sin(rotX)
    rx_mat = np.array([
        [1, 0, 0],
        [0, c_x, -s_x],
        [0, s_x, c_x]
    ])
    
    rotated = points @ ry_mat.T @ rx_mat.T
    
    # Perspective projection
    zs = rotated[:, 2] + cam_dist
    xs = rotated[:, 0] * scale / zs + cx
    ys = rotated[:, 1] * scale / zs + cy
    
    return np.column_stack((xs, ys)).astype(int)

def create_telemetry_plot(time_data, val_data, current_t, max_t, color_hex):
    """Renders a real telemetry plot using Matplotlib and converts it to OpenCV image."""
    fig, ax = plt.subplots(figsize=(4.0, 2.2), facecolor='#0c0e12')
    ax.set_facecolor('#0c0e12')
    
    # Filter data up to current time
    mask = time_data <= current_t
    ax.plot(time_data[mask], val_data[mask], color=color_hex, linewidth=2.0)
    
    ax.set_xlim(0, max_t)
    ax.set_ylim(np.min(val_data) - 0.2, np.max(val_data) + 0.2)
    
    # Styles
    ax.spines['bottom'].set_color('#27272a')
    ax.spines['left'].set_color('#27272a')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(colors='#a1a1aa', labelsize=8)
    ax.grid(color='#1e293b', linestyle=':', alpha=0.5)
    
    # Save chart to a numpy buffer
    fig.canvas.draw()
    # Get RGBA buffer as numpy array
    img = np.asarray(fig.canvas.buffer_rgba())
    # Slice to RGB and copy to avoid writeable flag issues
    img = img[:, :, :3].copy()
    # Convert RGB to BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.close(fig)
    return img

def compile_reel_video(stl_file, csv_file, output_file="output_cad/cero_reel.mp4"):
    print("[COMPILER] Iniciando compilación de Reel de Instagram...")
    
    # 1. Load engineering datasets
    vertices, faces = read_ascii_stl(stl_file)
    telemetry = read_telemetry(csv_file)
    
    if vertices is None or telemetry is None:
        print("[COMPILER] Fallo al cargar dependencias de archivos.")
        return
        
    # Scale STL vertices to fit viewport (-1.0 to 1.0 bounding scale approx)
    max_val = np.max(np.abs(vertices))
    if max_val > 0:
        vertices = vertices / max_val
        
    # Video properties: 1080x1920 (Vertical Reel), 60 FPS
    width, height = 1080, 1920
    fps = 60
    duration = 5.0 # seconds
    total_frames = int(duration * fps)
    
    # Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    print(f"[COMPILER] Grabadora inicializada. Procesando {total_frames} fotogramas...")

    neon_bgr = (255, 229, 0) # Neon blue in BGR
    neon_hex = '#00e5ff'
    
    # 2. Frame-by-frame loop
    for frame_idx in range(total_frames):
        t = (frame_idx / total_frames) * duration # time in seconds
        
        # Blank canvas
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (8, 5, 4) # Dark slate background (#040508 BGR)
        
        # A. Draw Neon Grid lines
        grid_spacing = 60
        y_offset = int((t * 120) % grid_spacing)
        for x in range(0, width, grid_spacing):
            cv2.line(frame, (x, 0), (x, height), (22, 16, 12), 1) # dark blue lines
        for y in range(y_offset, height, grid_spacing):
            cv2.line(frame, (0, y), (width, y), (22, 16, 12), 1)
            
        # B. Rotate and project 3D STL wireframe
        # Center of viewport: middle of screen height
        cy = int(height * 0.42)
        cx = int(width / 2)
        
        # Rotation angles over time
        rot_x = 0.5 + 0.1 * np.sin(t * 1.5)
        rot_y = t * 1.8
        
        # Project
        proj_pts = project_3d_points(vertices, cx, cy, scale=550, rotX=rot_x, rotY=rot_y, cam_dist=3.5)
        
        # Draw wireframe triangles (glow pass + white core pass)
        for face in faces:
            pt1 = tuple(proj_pts[face[0]])
            pt2 = tuple(proj_pts[face[1]])
            pt3 = tuple(proj_pts[face[2]])
            
            # Glow pass (thick neon line)
            cv2.line(frame, pt1, pt2, (150, 100, 0), 4, cv2.LINE_AA)
            cv2.line(frame, pt2, pt3, (150, 100, 0), 4, cv2.LINE_AA)
            cv2.line(frame, pt3, pt1, (150, 100, 0), 4, cv2.LINE_AA)
            
            # Core pass (thin bright cyan line)
            cv2.line(frame, pt1, pt2, neon_bgr, 1, cv2.LINE_AA)
            cv2.line(frame, pt2, pt3, neon_bgr, 1, cv2.LINE_AA)
            cv2.line(frame, pt3, pt1, neon_bgr, 1, cv2.LINE_AA)
            
        # C. Telemetry HUD Texts & Borders
        hud_top_y = int(height * 0.68)
        
        # Draw tech panel box borders
        cv2.rectangle(frame, (80, hud_top_y), (width - 80, height - 200), (32, 28, 22), -1) # fill panel dark
        cv2.rectangle(frame, (80, hud_top_y), (width - 80, height - 200), (60, 50, 40), 2) # border
        
        # Glowing neon corners
        cv2.line(frame, (80, hud_top_y + 40), (80, hud_top_y), neon_bgr, 3)
        cv2.line(frame, (80, hud_top_y), (140, hud_top_y), neon_bgr, 3)
        cv2.line(frame, (width - 80, hud_top_y + 40), (width - 80, hud_top_y), neon_bgr, 3)
        cv2.line(frame, (width - 80, hud_top_y), (width - 140, hud_top_y), neon_bgr, 3)

        # Get telemetry at current simulated time
        tel_idx = np.argmin(np.abs(telemetry['time'] - (t % 3.0))) # loop telemetry if t > 3s
        speed_val = telemetry['speed'][tel_idx]
        steer_val = telemetry['steer'][tel_idx]
        g_val = telemetry['g'][tel_idx]
        
        # Draw Tech Labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "CERO ENGINE LABS // TELEMETRY LINK", (120, hud_top_y + 50), font, 0.7, (200, 200, 200), 2, cv2.LINE_AA)
        
        # Title of part
        cv2.putText(frame, "CHASSIS SPACEFRAME ANALYSIS", (120, hud_top_y + 110), font, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
        
        # Specifications
        cv2.putText(frame, f"VELOCIDAD: {speed_val:.1f} KM/H", (120, hud_top_y + 180), font, 0.8, neon_bgr, 2, cv2.LINE_AA)
        cv2.putText(frame, f"ACEL. LATERAL: {g_val:.2f} G", (120, hud_top_y + 230), font, 0.8, neon_bgr, 2, cv2.LINE_AA)
        cv2.putText(frame, f"DIRECCION: {steer_val:.1f} DEG", (120, hud_top_y + 280), font, 0.8, neon_bgr, 2, cv2.LINE_AA)
        
        # D. Real-Time Telemetry Graph Overlay
        # Create rolling graph of G-forces up to current time
        graph_img = create_telemetry_plot(telemetry['time'], telemetry['g'], t % 3.0, 3.0, neon_hex)
        # Overlay graph image onto canvas bottom right
        g_h, g_w, _ = graph_img.shape
        gy, gx = height - 200 - g_h - 20, width - 80 - g_w - 20
        frame[gy:gy+g_h, gx:gx+g_w] = graph_img
        
        # E. Top branding and watermark
        cv2.putText(frame, "BUILDCERO.COM", (100, 100), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(frame, (width - 240, 70), (width - 100, 110), neon_bgr, -1)
        cv2.putText(frame, f"D|A {int(t*10 + 12)}", (width - 220, 100), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        # Write frame to video file
        out.write(frame)
        
        # Progress logging
        if (frame_idx + 1) % 60 == 0:
            print(f"[COMPILER] Procesados {frame_idx + 1}/{total_frames} fotogramas...")

    out.release()
    print(f"[COMPILER] ¡Reel compilado con éxito! Guardado en: {output_file}")

if __name__ == "__main__":
    stl_p = "output_cad/cero_chassis.stl"
    csv_p = "output_cad/telemetry.csv"
    compile_reel_video(stl_p, csv_p)
