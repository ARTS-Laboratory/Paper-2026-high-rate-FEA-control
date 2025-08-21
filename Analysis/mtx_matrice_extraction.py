# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 13:05:17 2025

@author: trott
"""

import re
import numpy as np
from scipy.sparse import coo_matrix
import pandas as pd
import os

# --------- Step 1: Custom parser for your .mtx files ---------
def parse_custom_mtx(file_path):
    rows, cols, values = [], [], []
    max_row, max_col = 0, 0
    
    with open(file_path, "r") as f:
        for line in f:
            parts = re.split(r"[,\s]+", line.strip())
            if len(parts) >= 5:
                i, _, j, _, val = parts[:5]
                i, j, val = int(i), int(j), float(val)
                rows.append(i-1)  # convert to 0-based indexing
                cols.append(j-1)
                values.append(val)
                max_row = max(max_row, i)
                max_col = max(max_col, j)
    
    return coo_matrix((values, (rows, cols)), shape=(max_row, max_col)).toarray()

# --------- Step 2: Input file paths ---------
mass_file = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Modeling\Abaqus\mtx\Job-2_MASS2.mtx"
stiff_file = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Modeling\Abaqus\mtx\Job-2_STIF2.mtx"

# --------- Step 3: Output folder ---------
out_dir = r"C:\Users\trott\Documents\Paper-2026-high-rate-FEA-control\Analysis\kmc_matrices"
os.makedirs(out_dir, exist_ok=True)

# --------- Step 4: Load matrices ---------
mass_matrix = parse_custom_mtx(mass_file)
stiffness_matrix = parse_custom_mtx(stiff_file)

print("Mass matrix shape:", mass_matrix.shape)
print("Stiffness matrix shape:", stiffness_matrix.shape)

# --------- Step 5: Compute damping matrix ---------
alpha = 65.53
beta = 3.95e-6
damping_matrix = alpha * mass_matrix + beta * stiffness_matrix

print("Damping matrix shape:", damping_matrix.shape)

# --------- Step 6: Save all matrices as CSV ---------
pd.DataFrame(mass_matrix).to_csv(os.path.join(out_dir, "Mass_Matrix.csv"), index=False)
pd.DataFrame(stiffness_matrix).to_csv(os.path.join(out_dir, "Stiffness_Matrix.csv"), index=False)
pd.DataFrame(damping_matrix).to_csv(os.path.join(out_dir, "Damping_Matrix.csv"), index=False)

print(f"✅ All matrices saved to {out_dir}")
