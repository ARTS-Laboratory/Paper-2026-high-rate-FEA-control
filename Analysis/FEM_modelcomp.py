# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 10:33:43 2025

@author: trott
"""

import pandas as pd
import matplotlib.pyplot as plt
import re
 
matlab_file = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Modeling\MATLAB\XY_MATLAB.txt"
abaqus_file = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Modeling\Abaqus\XYabaqus.rpt"
save_path = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Analysis\Figures\comparison_matlab_abaqus.png"

df_matlab = pd.read_csv(matlab_file, sep='\t', header=None, names=['Time', 'Displacement'])
df_matlab['Displacement_mm'] = df_matlab['Displacement'] * 1e3  # meters → mm

def load_abaqus_rpt(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            # Find numeric values (handles e.g. 250.005E-06)
            nums = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", line)
            if len(nums) == 2:
                t, u = map(float, nums)
                data.append([t, u])
    df = pd.DataFrame(data, columns=["Time", "Displacement"])
    
    # Clean: drop obvious bad rows (like if time = 2.0 s but only 0.05 s expected)
    df = df[df["Time"] <= 0.05].reset_index(drop=True)
    
    # Convert displacement to mm
    df["Displacement_mm"] = df["Displacement"] * 1e3
    return df

df_abaqus = load_abaqus_rpt(abaqus_file)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

plt.figure(figsize=(6,4))
plt.plot(df_matlab['Time']*1e3, df_matlab['Displacement_mm'], label="MATLAB Uncontrolled", linewidth=1)
plt.plot(df_abaqus['Time']*1e3, df_abaqus['Displacement_mm'], label="Abaqus", linewidth=1)

plt.xlabel("Time (ms)")
plt.ylabel("Displacement (mm)")
plt.title("Midpoint Displacement Comparison: MATLAB vs Abaqus")
plt.legend(facecolor="white", edgecolor="lightgray", framealpha=1, frameon=True)
plt.grid(True)
plt.tight_layout()

plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot saved to {save_path}")
