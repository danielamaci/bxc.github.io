"""
The script generates turbulent magnetic field and current density field
It distinguishes between purely turbulent and structured magnetic field

Choose the parameters in the parameters.py file before rnning the script 
"""
from parameters import *
from fields_functions import *

if B0_model == 'none':  ## Build the purely turbulent magnetic and current density field
    alpha = 1  # == no filtering
    
    r, FGF = build_r() #FGF is the vector fields, r is the norm
    S = build_S(r)
    
    B = build_B(S, FGF, alpha)
    B = B/(np.amax(np.sqrt(B[0]**2 + B[1]**2 + B[2]**2)))
    
    j = build_j(B) # Already normalized inside the function build_j
else: ## Build turbulent magnetic field with background structure
    B0 = build_B0(B0_model)
    B0 = B0/(np.amax(np.sqrt(B0[0]**2 + B0[1]**2 + B0[2]**2)))
    
    alpha = np.sqrt(B0[0]**2 + B0[1]**2 + B0[2]**2)
    
    r, FGF = build_r() #FGF is the vector fields, r is the norm
    S = build_S(r)

    Bturb = build_B(S, FGF, alpha)
    Bturb = Bturb/(np.amax(np.sqrt(Bturb[0]**2 + Bturb[1]**2 + Bturb[2]**2)))
    
    ## At this point, these fields could be deleted to save memory
    # del(r, FGF, S)
    
    jturb = build_j(Bturb) #comment if not needed
    
    gamma = 0.3 #constant filtering 
    
    B = B0 + gamma*Bturb
    
    ## At this point, this field could be deleted to save memory
    # del(Bturb) 
    
    j = build_j(B)    