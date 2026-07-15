#!/usr/bin/env python3
"""
==========================================================================
CERO MOTORSPORTS ENGINEERING SUITE PIPELINE RUNNER
Runs CAD generation, Structural FEA, Vehicle Dynamics, and Video Compilation
in sequence using the active virtual environment.
==========================================================================
"""

import sys
import os
import subprocess

def run_script(script_name, cwd):
    print(f"\n==========================================================================")
    print(f"[PIPELINE] Ejecutando: {script_name}...")
    print(f"==========================================================================")
    
    # Run using the current virtual environment python executable
    python_exe = sys.executable
    script_path = os.path.join(cwd, "engineering_suite", script_name)
    
    result = subprocess.run([python_exe, script_path], cwd=cwd)
    if result.returncode != 0:
        print(f"[PIPELINE] ERROR: {script_name} terminó con código de error {result.returncode}")
        sys.exit(result.returncode)
    print(f"[PIPELINE] COMPLETADO: {script_name}")

if __name__ == "__main__":
    # Get current project root path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"[PIPELINE] Directorio raíz del proyecto: {project_root}")
    
    # Run modules sequentially
    run_script("cad_generator.py", project_root)
    run_script("chassis_fea.py", project_root)
    run_script("vehicle_dynamics.py", project_root)
    run_script("video_compiler.py", project_root)
    
    print("\n==========================================================================")
    print("[PIPELINE] PIPELINE DE INGENIERÍA COMPLETADO CON ÉXITO")
    print("Mallas 3D, cálculos FEA, telemetría de dinámica y Reel final compilados.")
    print("Archivos disponibles en la carpeta: output_cad/")
    print("==========================================================================")
