from parameters import *

#######################################
############ Configuration ############
#######################################

## Here are some 'fixed' parameters, i.e. configuration and the geometric 
## parameters of the spirals which have not been examined in the parameter study

zero = 1.e-15 # to avoid the 'exact' 0 leading to divergences
my_dtype = np.float32

d = 0.2
c_0 = 0.3
# Width and smoothness of the intense sheets
w_i =  2.5e-5
ell_i = 7.e-3
# Width, smoothness and number of the diffuse sheets
w_d = 0.05
ell_d = 0.25  
k_d = 2*np.pi*3.
# Amplitude of diffuse sheets over the intense sheets (epsilon < 1 is relevant):
epsilon = 3.5e-3 
# Controls the steepness of the transition from 1 to 0 in the cutoff function. 
ell_cutoff = 0.2 


############################################################
############ Functions for computing the fields ############
############################################################

def build_xyz():
    return np.meshgrid(np.arange(-N/2, N/2, dtype=my_dtype)*dx, np.arange(-N/2, N/2, dtype=my_dtype)*dx, np.arange(-N/2, N/2, dtype=my_dtype)*dx, indexing = 'ij')

def fourier(arr): # real fft
    return rfftn(arr,s=(N, N, N),workers=-1)

def ifourier(arr): # real ifft
    return irfftn(arr,s=(N, N, N),workers=-1)

def fourier2(arr): # complex fft
    return fftn(arr,s=(N, N, N),workers=-1)

def ifourier2(arr): # complex ifft
    return ifftn(arr,s=(N, N, N),workers=-1)

def vorticity_fromFourierSpace(u):
    pad1,pad2,pad3=N,N,N # No zero-padding
    fourier_u=[fourier2(u[0]),fourier2(u[1]),fourier2(u[2])]
    kx,ky,kz=2*np.pi*np.fft.fftfreq(N),2*np.pi*np.fft.fftfreq(N),2*np.pi*np.fft.fftfreq(N)
    kx,ky,kz=np.meshgrid(kx,ky,kz,indexing='ij')
    eye = 0+1j
    return np.real(ifourier2(eye*(ky*fourier_u[2]-kz*fourier_u[1]))).astype(my_dtype), np.real(ifourier2(eye*(kz*fourier_u[0]-kx*fourier_u[2]))).astype(my_dtype), np.real(ifourier2(eye*(kx*fourier_u[1]-ky*fourier_u[0]))).astype(my_dtype)

def topHat(arr, w, ell):
    arr = arr/np.amax(np.abs(arr)) # set range in [-1, 1]
    return 0.5*(np.tanh((arr+w/2)/(ell+zero)) - np.tanh((arr-w/2)/(ell+zero))) # 'zero' avoids a divergence when ell = 0

def build_seed_wn(): 
    seed1, seed2, seed3 = 636+seed_wn**3, 131+seed_wn, 214+seed_wn**2
    dW1 = (np.random.default_rng(seed1).normal(loc = mean_seed_wn, scale = std_seed_wn[0], size = (N, N, N))*dx**(3./2)).astype(my_dtype) # Note the square root of the volume element 'dx**(3./2)' in factor, so that wg acts as a dW in stochastic calculus, cf the first appendix of Durrive et al 2020.
    dW2 = (np.random.default_rng(seed2).normal(loc = mean_seed_wn, scale = std_seed_wn[1], size = (N, N, N))*dx**(3./2)).astype(my_dtype)
    dW3 = (np.random.default_rng(seed3).normal(loc = mean_seed_wn, scale = std_seed_wn[2], size = (N, N, N))*dx**(3./2)).astype(my_dtype)
    return np.array([dW1, dW2, dW3], dtype=my_dtype)

def cutoff(r2, L, eta):
    ell= ell_cutoff*L # This controls the thickness of the transition from 1 to 0.
    cutoff = 0.5*(1.-np.tanh((np.sqrt(r2)-L-ell)/ell)) 
    return cutoff/np.amax(cutoff)

def kernel(i, L, h, eta):
    pos = build_xyz() 
    norm2 = pos[0]**2+pos[1]**2+pos[2]**2
    norm2[norm2==0.] = zero
    return 1./(4*np.pi)*cutoff(norm2,L, eta)*pos[i]*(norm2+(eta)**2)**(-h) 

def biot_savart(current, L, h, eta): 
    k0, k1, k2 = kernel(0, L[0], h, eta), kernel(1, L[1], h, eta), kernel(2, L[2], h, eta)
    return np.array([-ifourier(fourier(k2)*fourier(current[1])-fourier(k1)*fourier(current[2])),
                    -ifourier(fourier(k0)*fourier(current[2])-fourier(k2)*fourier(current[0])),
                    -ifourier(fourier(k1)*fourier(current[0])-fourier(k0)*fourier(current[1]))], dtype=my_dtype)

def build_r():
    c0 = build_seed_wn()
    FGF = biot_savart(c0, L_r, h_r, eta_r)
    r = np.sqrt(FGF[0]**2 + FGF[1]**2 + FGF[2]**2)
    return r/np.amax(np.abs(r)), FGF

def build_S(r):
    theta = 1/np.pi*np.arctan2(np.gradient(r, dx, axis=1), np.gradient(r, dx, axis=0))
    # Note: below we modify the 'theta' array instead of defining a new 'S' array, to save ram memory during the calculation
    theta = topHat(r - c_0 - d*theta, w_i*np.cos(0.5*np.pi*theta), ell_i) + epsilon*topHat(np.cos(k_d*(r - c_0 - d*theta)), w_d, ell_d)
    # Smoothing, to remove singular regions, where the gradient of r is too large 
    smoothing = 0.1
    theta = theta*(1 - np.exp(-smoothing*(np.gradient(r, dx, axis = 0)**2 + np.gradient(r, dx, axis = 1)**2 + np.gradient(r, dx, axis = 2)**2)))
    return theta/np.amax(np.abs(theta))

def build_B0(model):
    x,y,z = build_xyz()
    if model == 'none': 
        B0x,B0y,B0z=0.,0.,0.
        B0x,B0y,B0z = np.full(np.shape(x),B0x,dtype=my_dtype),np.full(np.shape(x),B0y,dtype=my_dtype),np.full(np.shape(x),B0z,dtype=my_dtype)
    elif model == 'uniform':
        B0 = 1**float(1)
        B0x,B0y,B0z=0.,0.,B0
        B0x,B0y,B0z=np.full(np.shape(x),B0x,dtype=my_dtype),np.full(np.shape(x),B0y,dtype=my_dtype),np.full(np.shape(x),B0z,dtype=my_dtype)
    elif model == 'braided':  ##Braided magnetic field, cf for example in https://arxiv.org/pdf/1512.05918v2.pdf
        comp = 6
        zi = [-0.2,-0.15,-0.1,0.1, 1.5,0.2] 
        r0 = 0.1
        r = 0.1

        B0x = np.full(np.shape(x), 0)
        B0y = np.full(np.shape(x), 0)
        for i in range(comp):
            B0x = B0x + np.array(-(-1)**(i+1)*np.exp(-(x**2 + y**2 + (z-zi[i])**2)/r**2)*y/r0)
            B0y = B0y + np.array((-1)**(i+1)*np.exp(-(x**2 + y**2 + (z-zi[i])**2)/r**2)*x/r0)
        B0z = np.full(np.shape(x), 1)
    elif model == 'arcade':  ##arcade with dips example in https://arxiv.org/pdf/1412.7438.pdf
        def arcade(B0, ll, k, x_center):
            alpha = np.sqrt(k**2 - ll**2) # related to the amount of shear in the arcade. For ll = k, alpha = 0, the magnetic field is purely potential and the By component is zero.
            return np.array([B0*ll/k*np.cos(k*(x-x_center))*np.exp(-ll*z), B0*alpha/k*np.cos(k*(x-x_center))*np.exp(-ll*z), -B0*np.sin(k*(x-x_center))*np.exp(-ll*z)])

        B0_1 = 2*10**float(1)
        shear_1 = float(0.75) # ll/k is related to the amount of shear in the structure. shear_1 = (0.85, 0.75, 0.65) corresponds to typical shear angles of (32, 41, 54) degrees
        k_1 = float(np.pi/2) # k is related to the lateral extension of the arcade
        ll_1 = k_1*shear_1 # ll is a measure of the vertical magnetic scale height
        xc_1 = 0.

        B0_2 = 2*10**float(1)
        k_2 = float(3*np.pi/2)
        ll_2 = np.sqrt(-k_1**2 + k_2**2 + ll_1**2) # cf eq (9) of arXiv/1412.7438
        xc_2 = float(2)

        B0x, B0y, B0z = arcade(B0_1, ll_1, k_1, xc_1) - arcade(B0_2, ll_2, k_2, xc_2)

    elif model == 'GH': ##Gold-Hoyle model cf for example in https://www.aanda.org/articles/aa/pdf/2017/12/aa31412-17.pdf
        r=np.sqrt(x**2+y**2+z**2)
        r[r<zero]=zero
        cos_phi = x/r
        sin_phi = y/r

        B0 = 2*10**float(1)
        tau = 3 #parameter related to the twist and its sign gives the field chirality

        Br = np.full(np.shape(r), 0)
        Bphi = (B0 *tau*r)/(1 + tau**2*r**2)
        Bphi = np.full(np.shape(r), Bphi)
        Bz = B0/(1 + tau**2*r**2)
        Bz =  np.full(np.shape(z), Bz)

        B0x, B0y, B0z = x/r*Br-sin_phi*Bphi, y/r*Br+cos_phi*Bphi, Bz
    return np.array([B0x, B0y, B0z])

def build_B(S, FGF, alpha):
    c0 = alpha*np.array([S*FGF[0], S*FGF[1], S*FGF[2]], dtype=my_dtype)
    c0 = c0/np.amax(np.abs(c0))
    return biot_savart(c0, L_B, h_B, eta_B)
    
def build_j(B):
    j = vorticity_fromFourierSpace(B)
    return j/np.amax(np.abs(j))
