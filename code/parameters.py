import numpy as np
from scipy.fft import fftn, ifftn
from scipy.fft import rfftn, irfftn

###############################
############ USAGE ############
###############################

# Choose your parameters in this file, and then run 'python BxC.py' in a terminal from the main folder, namely the one containing BxC.py.

##########################################
############ INPUT PARAMETERS ############
##########################################

N = 256 # Resolution
dx = 1/N

B0_model = 'none'  #either 'none', 'arcade', 'braided', or 'GH'

# Seed, mean and standard deviation of the white noise
seed_wn, mean_seed_wn, std_seed_wn = 130, 0., [1., 1., 1.]

# Parameters of the (modified) Biot-Savart law for the FGF field:
L_r = [0.15, 0.15, 0.15] # L basically controls the size of the 'eddies'. L is in box size, which is = 1. So 0 < L < 0.5
h_r = 0.1 # Hurst parameter: Small --> FGF is smooth, large --> FGF is rough 
eta_r = 0.003 # expessed in box size 

# Parameters of the (modified) Biot-Savart law for the magnetic field:
L_B = [0.1, 0.1, 0.1] # L_B is in box size, which is = 1. So 0 < L_B < 0.5
h_B = 2.0 # Hurst parameter
eta_B = 0.003  # expessed in box size -- use eta >= 3dx to ensure divergence-free property