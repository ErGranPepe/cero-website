#!/usr/bin/env python3
"""
==========================================================================
CERO MOTORSPORTS VEHICLE DYNAMICS SIMULATOR
2-DOF Bicycle Model with yaw rate, lateral slip, and load transfer.
Simulates a high-speed steering maneuver and exports CSV telemetry.
Plots vehicle path and lateral G forces.
==========================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Physical parameters of CERO racing car
MASS = 230.0         # kg (with driver)
WHEELBASE = 1.6      # meters (L)
A_DIST = 0.72        # meters (CoG to front axle - 45% bias)
B_DIST = 0.88        # meters (CoG to rear axle - 55% bias)
IZ = 120.0           # kg*m^2 (Yaw moment of inertia)
C_FRONT = 15000.0    # N/rad (Front tyre cornering stiffness)
C_REAR = 18000.0     # N/rad (Rear tyre cornering stiffness)
GRAVITY = 9.81       # m/s^2

def run_simulation(velocity_kmh=60.0, steering_deg=6.0):
    print(f"[DYNAMICS] Iniciando simulación de maniobra a {velocity_kmh} km/h con {steering_deg}° de dirección...")
    
    # Constants
    V = velocity_kmh / 3.6  # convert to m/s
    delta = np.radians(steering_deg)
    
    # Simulation settings
    t_end = 3.0 # seconds
    dt = 0.01   # time step
    steps = int(t_end / dt)
    
    # States
    beta = 0.0  # side slip angle (rad)
    omega = 0.0 # yaw rate (rad/s)
    psi = 0.0   # heading angle (rad)
    X = 0.0     # Global coordinates
    Y = 0.0
    
    # History logs for telemetry
    time_log = []
    beta_log = []
    omega_log = []
    ay_log = []
    x_log = []
    y_log = []
    steering_log = []
    speed_log = []

    # Run Euler integration
    for step in range(steps):
        t = step * dt
        
        # Steering input: step input after 0.5s
        if t < 0.5:
            delta_input = 0.0
        elif t < 0.8:
            # Smooth steering turn-in ramp
            delta_input = delta * (t - 0.5) / 0.3
        else:
            delta_input = delta
            
        # Slip angles:
        alpha_f = delta_input - beta - (A_DIST * omega / V)
        alpha_r = -beta + (B_DIST * omega / V)
        
        # Lateral Tyre Forces (linear regime)
        Fyf = C_FRONT * alpha_f
        Fyr = C_REAR * alpha_r
        
        # Equations of Motion state derivatives:
        # beta_dot = (Fyf + Fyr)/(m*V) - omega
        # omega_dot = (a*Fyf - b*Fyr)/Iz
        beta_dot = (Fyf + Fyr) / (MASS * V) - omega
        omega_dot = (A_DIST * Fyf - B_DIST * Fyr) / IZ
        
        # Integrate states
        beta += beta_dot * dt
        omega += omega_dot * dt
        psi += omega * dt
        
        # Lateral Acceleration (G forces)
        ay = V * (beta_dot + omega) # m/s^2
        ay_g = ay / GRAVITY
        
        # Integrate global trajectory position
        X += V * np.cos(psi + beta) * dt
        Y += V * np.sin(psi + beta) * dt
        
        # Logging
        time_log.append(t)
        beta_log.append(np.degrees(beta))
        omega_log.append(np.degrees(omega))
        ay_log.append(ay_g)
        x_log.append(X)
        y_log.append(Y)
        steering_log.append(np.degrees(delta_input))
        speed_log.append(velocity_kmh)

    # Convert to arrays
    time_arr = np.array(time_log)
    x_arr = np.array(x_log)
    y_arr = np.array(y_log)
    ay_arr = np.array(ay_log)
    
    # 1. Save Telemetry CSV
    os.makedirs("output_cad", exist_ok=True)
    telemetry_data = np.column_stack((time_log, steering_log, speed_log, omega_log, beta_log, ay_log, x_log, y_log))
    header = "Time(s),Steer(deg),Speed(km/h),YawRate(deg/s),Sideslip(deg),LatG,PosX(m),PosY(m)"
    np.savetxt("output_cad/telemetry.csv", telemetry_data, delimiter=",", header=header, comments="", fmt="%.5f")
    print(f"[DYNAMICS] Telemetría guardada: output_cad/telemetry.csv ({len(time_log)} registros)")

    # 2. Render & Save plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0c0e12')
    
    # Trajectory Plot
    ax1.set_facecolor('#0c0e12')
    ax1.plot(y_arr, x_arr, color='#00e5ff', linewidth=2.5, label='Trayectoria Monoplaza')
    ax1.scatter(y_arr[0], x_arr[0], color='#39ff14', s=40, label='Salida')
    ax1.scatter(y_arr[-1], x_arr[-1], color='#ff007f', s=40, label='Meta')
    ax1.set_title("Trazado en Pista (Trayectoria XY)", color='#ffffff', fontsize=12, fontweight='bold')
    ax1.set_xlabel("Lateral Y (m)", color='#a1a1aa')
    ax1.set_ylabel("Longitudinal X (m)", color='#a1a1aa')
    ax1.tick_params(colors='#a1a1aa')
    ax1.grid(color='#1e293b', linestyle='--')
    ax1.legend(facecolor='#131720', edgecolor='#1e293b', labelcolor='#ffffff')
    ax1.axis('equal')

    # Lateral G Plot
    ax2.set_facecolor('#0c0e12')
    ax2.plot(time_arr, ay_arr, color='#ff007f', linewidth=2.0)
    ax2.set_title("Aceleración Lateral (G forces)", color='#ffffff', fontsize=12, fontweight='bold')
    ax2.set_xlabel("Tiempo (s)", color='#a1a1aa')
    ax2.set_ylabel("Fuerza Lateral (G)", color='#a1a1aa')
    ax2.tick_params(colors='#a1a1aa')
    ax2.grid(color='#1e293b', linestyle='--')

    plt.savefig("output_cad/dynamics_plot.png", dpi=150, bbox_inches='tight', facecolor='#0c0e12')
    plt.close()
    print("[DYNAMICS] Gráfico de física guardado en output_cad/dynamics_plot.png")

if __name__ == "__main__":
    run_simulation()
