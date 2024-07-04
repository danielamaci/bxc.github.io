"""
The script generates turbulent magnetic field and current density field
It distinguishes between purely turbulent and structured magnetic field

Choose the parameters in the parameters.py file before running the script 
"""
from parameters import *
from fields_functions import *

print('Generating B field at resolution ' + str(N) + ' and background topology: ' + str(B0_model) )

if B0_model == 'none':  ## Build the purely turbulent magnetic and current density field
    alpha = 1  # == no filtering
    
    r, FGF = build_r() #FGF is the vector fields, r is the norm
    S = build_S(r)
    
    B = build_B(S, FGF, alpha)
    B = B/(np.amax(np.sqrt(B[0]**2 + B[1]**2 + B[2]**2)))
    
    del(r, FGF, S) ## comment this line if you want to see intermediate steps
    # j = build_j(B) # Uncomment if you also need the current density field
else: ## Build turbulent magnetic field with background structure
    B0 = build_B0(B0_model)
    B0 = B0/(np.amax(np.sqrt(B0[0]**2 + B0[1]**2 + B0[2]**2)))
    
    alpha = np.sqrt(B0[0]**2 + B0[1]**2 + B0[2]**2)
    
    r, FGF = build_r() #FGF is the vector fields, r is the norm
    S = build_S(r)

    Bturb = build_B(S, FGF, alpha)
    Bturb = Bturb/(np.amax(np.sqrt(Bturb[0]**2 + Bturb[1]**2 + Bturb[2]**2)))
    
    ## At this point, these fields could be deleted to save memory
    del(r, FGF, S) ## comment this line if you want to see intermediate steps
    
    # jturb = build_j(Bturb) # Uncomment if you also need the current density field of the purely turbulent field
    
    gamma = 0.3 #constant filtering 
    
    B = B0 + gamma*Bturb
    
    ## At this point, this field could be deleted to save memory
    del(Bturb) # Comment if you need the purely turbulent field
    
    # j = build_j(B)  # Uncomment if you also need the current density field of the total turbulent field

print('Saving the B field in root folder')
np.savez('./B.npz', B=B)

print('Saving a 2D visualization of the norm of the B field in root folder')

# A minimalistic visualization tool, as a sanity check of the generated field
from matplotlib import pyplot as plt

def plot(sf):
    plt.figure(figsize = (7, 7))
    plt.imshow(sf)
    plt.colorbar(shrink = 0.8)
    plt.title('Bnorm - 2D slice')
    plt.savefig('./Bnorm_slice.jpg', bbox_inches = 'tight')
    return

plot(np.sqrt(B[0,:,:,N//2]**2 + B[1,:,:,N//2]**2 + B[2,:,:,N//2]**2))