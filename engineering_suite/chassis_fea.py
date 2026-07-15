#!/usr/bin/env python3
"""
==========================================================================
CERO MOTORSPORTS STRUCTURAL FEA SOLVER
3D Spaceframe Truss Finite Element Analysis Solver (Direct Stiffness Method).
Solves for displacements, internal member stresses, and safety factors.
Plots and saves the deformed chassis stress map.
==========================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Physical properties of Steel 4130 Chromoly
E_STEEL = 205000.0  # MPa (N/mm^2)
YIELD_STEEL = 460.0  # MPa (N/mm^2)
OD_TUBE = 25.4      # mm
T_TUBE = 2.4        # mm

def run_fea_analysis():
    print("[FEA] Iniciando resolvedor por Elementos Finitos 3D del chasis...")
    
    # 1. Geometry: Node coords (X, Y, Z) in mm
    nodes = np.array([
        [400, 180, 250],   # Node 0: f_bulk_tl
        [400, -180, 250],  # Node 1: f_bulk_tr
        [400, 180, 50],    # Node 2: f_bulk_bl
        [400, -180, 50],   # Node 3: f_bulk_br
        
        [800, 220, 480],   # Node 4: f_hoop_tl
        [800, -220, 480],  # Node 5: f_hoop_tr
        [800, 250, 50],    # Node 6: f_hoop_bl
        [800, -250, 50],   # Node 7: f_hoop_br
        
        [1450, 0, 950],    # Node 8: m_hoop_t
        [1450, 260, 580],  # Node 9: m_hoop_ml
        [1450, -260, 580], # Node 10: m_hoop_mr
        [1450, 280, 50],   # Node 11: m_hoop_bl
        [1450, -280, 50],  # Node 12: m_hoop_br
        
        [2100, 150, 350],  # Node 13: r_bulk_tl
        [2100, -150, 350], # Node 14: r_bulk_tr
        [2100, 150, 80],   # Node 15: r_bulk_bl
        [2100, -150, 80]   # Node 16: r_bulk_br
    ], dtype=float)

    # 2. Connectivity: (node_i, node_j)
    elements = np.array([
        [0, 1], [1, 3], [3, 2], [2, 0],  # Front bulkhead ring
        [4, 5], [5, 7], [7, 6], [6, 4],  # Front hoop ring
        [11, 9], [9, 8], [8, 10], [10, 12], [12, 11],  # Main hoop ring
        [13, 14], [14, 16], [16, 15], [15, 13],  # Rear bulkhead ring
        [0, 4], [1, 5], [2, 6], [3, 7],  # Front bulkhead to hoop
        [4, 9], [5, 10], [6, 11], [7, 12],  # Front hoop to main hoop
        [9, 13], [10, 14], [11, 15], [12, 16],   # Main hoop to rear
        
        # Side panel diagonals
        [0, 6], [2, 4],  # Left side front
        [1, 7], [3, 5],  # Right side front
        [4, 11], [6, 9], # Left side mid
        [5, 12], [7, 10],# Right side mid
        [9, 15], [11, 13],# Left side rear
        [10, 16], [12, 14],# Right side rear
        
        # Top/Bottom diagonals
        [0, 5], [1, 4],  # Top front
        [2, 7], [3, 6],  # Bottom front
        [4, 10], [5, 9], # Top mid
        [6, 12], [7, 11],# Bottom mid
        [9, 14], [10, 13],# Top rear
        [11, 16], [12, 15],# Bottom rear
        
        # Bulkhead cross braces and rear roll hoop braces
        [0, 3], [4, 7], [13, 16], # Bulkhead cross braces
        [8, 13], [8, 14] # Main hoop rear bracing elements (essential for longitudinal stability)
    ])

    num_nodes = len(nodes)
    num_elements = len(elements)
    num_dof = num_nodes * 3

    # Tube cross-section area: A = pi * (ro^2 - ri^2)
    ro = OD_TUBE / 2.0
    ri = ro - T_TUBE
    A = np.pi * (ro**2 - ri**2)

    # 3. Global Stiffness Matrix K Assembly
    K = np.zeros((num_dof, num_dof))
    lengths = np.zeros(num_elements)
    cosines = np.zeros((num_elements, 3)) # direction cosines: l, m, n

    for e in range(num_elements):
        n1, n2 = elements[e]
        p1, p2 = nodes[n1], nodes[n2]
        
        dx = p2 - p1
        L = np.linalg.norm(dx)
        lengths[e] = L
        
        # Direction cosines
        l, m, n = dx / L
        cosines[e] = [l, m, n]
        
        # Local stiffness matrix factors
        k_const = (A * E_STEEL) / L
        
        # Global element stiffness matrix terms
        ke_truss = np.array([
            [l*l, l*m, l*n, -l*l, -l*m, -l*n],
            [l*m, m*m, m*n, -l*m, -m*m, -m*n],
            [l*n, m*n, n*n, -l*n, -m*n, -n*n],
            [-l*l, -l*m, -l*n, l*l, l*m, l*n],
            [-l*m, -m*m, -m*n, l*m, m*m, m*n],
            [-l*n, -m*n, -n*n, l*n, m*n, n*n]
        ])
        
        ke = k_const * ke_truss
        
        # Map element DOFs to global K matrix DOFs
        dofs = [n1*3, n1*3+1, n1*3+2, n2*3, n2*3+1, n2*3+2]
        for i in range(6):
            for j in range(6):
                K[dofs[i], dofs[j]] += ke[i, j]

    # 4. Forces Vector (F) Assembly
    # Simulate a frontal impact (5G test). Vehicle Mass = 230 kg
    # F_impact = 230 * 9.81 * 5 = 11281 N. Distribute equally on front bulkhead nodes (0, 1, 2, 3) in -X direction.
    F = np.zeros(num_dof)
    force_per_node = -11281.5 / 4.0
    for node in [0, 1, 2, 3]:
        F[node * 3] = force_per_node # force applied in X direction

    # 5. Boundary Conditions (Constrain rear bulkhead nodes as fixed)
    # Rear bulkhead nodes (13, 14, 15, 16) are anchored to the ground/engine mount fixture
    fixed_nodes = [13, 14, 15, 16]
    fixed_dofs = []
    for node in fixed_nodes:
        fixed_dofs.extend([node*3, node*3+1, node*3+2])

    free_dofs = np.delete(np.arange(num_dof), fixed_dofs)

    # 6. Solve the linear system for free DOFs: K_free * U_free = F_free
    K_free = K[np.ix_(free_dofs, free_dofs)]
    F_free = F[free_dofs]
    U_free = np.linalg.solve(K_free, F_free)

    # Global displacements vector U
    U = np.zeros(num_dof)
    U[free_dofs] = U_free

    # 7. Stress Calculation for each structural member
    # sigma_e = E/L * [-l, -m, -n, l, m, n] . U_e
    stresses = np.zeros(num_elements)
    for e in range(num_elements):
        n1, n2 = elements[e]
        L = lengths[e]
        l, m, n = cosines[e]
        
        u_elem = np.array([
            U[n1*3], U[n1*3+1], U[n1*3+2],
            U[n2*3], U[n2*3+1], U[n2*3+2]
        ])
        
        stress_mat = np.array([-l, -m, -n, l, m, n])
        stresses[e] = (E_STEEL / L) * np.dot(stress_mat, u_elem)

    # Safety factor calculations
    max_stress = np.max(np.abs(stresses))
    min_safety_factor = YIELD_STEEL / max_stress if max_stress > 0 else float('inf')

    print(f"[FEA] Análisis completo.")
    print(f"[FEA] Deflexión máxima: {np.max(np.abs(U)):.4f} mm")
    print(f"[FEA] Tensión interna máxima: {max_stress:.2f} MPa")
    print(f"[FEA] Factor de Seguridad estructural mínimo: {min_safety_factor:.2f}")
    if min_safety_factor >= 1.5:
        print("[FEA] DISEÑO VALIDADADO: Cumple con el factor de seguridad regulatorio de 1.5.")
    else:
        print("[FEA] ALERTA DE HOMOLOGACIÓN: Tensión crítica por encima de la admisible. Rediseñe tubos.")

    # 8. Render & Save 3D FEA Stress Map Plot
    fig = plt.figure(figsize=(10, 8), facecolor='#0c0e12')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0c0e12')
    
    # Grid and axis colors
    ax.xaxis.set_pane_color((0.08, 0.09, 0.12, 1.0))
    ax.yaxis.set_pane_color((0.08, 0.09, 0.12, 1.0))
    ax.zaxis.set_pane_color((0.08, 0.09, 0.12, 1.0))
    ax.grid(True)
    
    # Scale displacement up for visual effect
    scale_factor = 50.0 # amplify deflection by 50x to see deformation clearly
    deformed_nodes = nodes + U.reshape(-1, 3) * scale_factor

    # Normalize stresses for colormap coloring
    norm_stresses = np.abs(stresses)
    max_abs_s = np.max(norm_stresses) if np.max(norm_stresses) > 0 else 1.0
    
    # Draw elements
    for e in range(num_elements):
        n1, n2 = elements[e]
        p1 = deformed_nodes[n1]
        p2 = deformed_nodes[n2]
        
        # Color element based on stress intensity (Blue=Low, Yellow=Mid, Red=Critical)
        s_val = norm_stresses[e]
        color_val = s_val / YIELD_STEEL
        color = plt.cm.jet(min(1.0, color_val)) # colormap JET
        
        # Plot deformed line
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                color=color, linewidth=2.5, solid_capstyle='round')

    # Draw Nodes as scatter points
    ax.scatter(deformed_nodes[:, 0], deformed_nodes[:, 1], deformed_nodes[:, 2], 
               color='#ffffff', s=15, depthshade=True)

    # Plot Settings
    ax.set_title("CERO CHASSIS FEA - STRESS MAP (MPa)", color='#ffffff', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Longitudinal X (mm)", color='#a1a1aa')
    ax.set_ylabel("Lateral Y (mm)", color='#a1a1aa')
    ax.set_zlabel("Height Z (mm)", color='#a1a1aa')
    ax.tick_params(colors='#a1a1aa', labelsize=8)

    # Add Colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.jet, norm=plt.Normalize(0, YIELD_STEEL))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=12, pad=0.08)
    cbar.set_label("Stress (MPa)", color='#ffffff', labelpad=10)
    cbar.ax.yaxis.set_tick_params(color='#ffffff', labelcolor='#ffffff')

    os.makedirs("output_cad", exist_ok=True)
    plt.savefig("output_cad/chassis_fea.png", dpi=150, bbox_inches='tight', facecolor='#0c0e12')
    plt.close()
    print("[FEA] Gráfico 3D guardado en output_cad/chassis_fea.png")
    
    return max_stress, min_safety_factor

if __name__ == "__main__":
    run_fea_analysis()
