---
layout: single
title: User Guide
permalink: /user_guide/
row:
  - image_path: /assets/images/guide1.png

  - image_path: /assets/images/guide2.png

  - image_path: /assets/images/guide3.png
---
## Requirements 
The only packages **required** to run the code are: 
- [numpy](https://numpy.org/)
- [scipy](https://scipy.org/) 

In order to run the sample visualization script, users need: 
- [Matplotlib](https://matplotlib.org/stable/) (2D plots)
- [Pyvista](https://docs.pyvista.org/version/stable/) (3D plots)

Note, however, that these packages are **not required** to run the code itself and user can use any Python data visualization library they prefer. 

## Download
The BxC toolkit is available at the [Github repository](https://github.com/danielamaci/bxc.github.io) and can easily be obtained by cloning the online repository:
```bash
git clone https://github.com/danielamaci/bxc.github.io
```
## Run the code
The code files are all stored in the folder *code* of the cloned repository. The user-controlled parameters are all contained in the file *parameters.py*. Once the desired parameters have been chosen, run the script *BxC.py* to generate your data cube of turbulent magnetic field!

**Note:** in order to let the users free to post-process the data with their own routines (i.e. power spectum, higher order statistics, 2D and 3D visualization), no such routine is implemented in the code itself. It is then suggested to run the script in a Python scientific environment. If you would rather run the code from terminal, then you need to first implent your analysis routines in the *BxC.py* and save the desired quantities. 

## The *parameters.py* file 
All the parameters that are user-controlled can be found and modified in the *parameters.py* file. Here is an overview of what the file contains.

First, all the imports are included in here. Afterwards you can find all the parameters determing the general properties of the field (resolution, background topologies, and the definition of the white noise vector). 

**Note:** All the results contained in the publications are generated with seed_wn=130.
![guide1](/assets/images/guide1.png)

In the last part of the file, you find the input parameters of the modified Biot-Savart law. These parameters are responsible for the customization of the power spectrum, accordin to the relations written in the [table](/user_guide.markdown/#power-spectrum-customization). 
![guide2](/assets/images/guide2.png)

![guide2](/assets/images/guide3.png)


## Power spectrum customization
Here you can find the set of relations for the customization of the power spectrum. For more details on the parameter study that has been conducted see the [article](https://arxiv.org/pdf/2405.09587). 

| :--: |
| Input parameters - power spectrum features relations |
|$k_i(L_R) \approx -68.5 L_R +16.4$|
|$k_c(L_R) \approx \frac{1}{\sqrt{2\pi}0.03}\exp{\left(-\frac{(L_R - 0.09)^2}{2(0.03)^2}\right)}$|
|$k_d(\eta_B) \approx 6.2\times 10^5 {\eta_B}^2 -1.2\times 10^4 \eta_B + 94$|
| $P_i(L_B; *) \approx -42.6 {L_B}^2 +35.3 L_B -0.9$ |
|$P_i (h_B; *) \approx 1.5\times 10^4 e^{-4.5h_B}$|
|$P_i(\eta_B; *) \approx 6.2\times 10^4 {\eta_B}^2 + 18\eta_B +0.5$|
|$\zeta(h_B; *) \approx -0.9 {h_B}^2 +6.4 h_B -10.1$|
|$\zeta(\eta_B; *) \approx -201.5 \eta_B -0.5$ |
|$\zeta(h_B, \eta_B; *) \approx A(\eta_B)h_B^2 + B(\eta_B)h_B + C(\eta_B)$|

Where:

| :--: |
|$A(\eta_B) \approx -4.6\times 10^3 {\eta_B}^2 + 1.13\times 10^2 \eta_B -1.2$|
|$B(\eta_B) \approx 2.1\times 10^4 {\eta_B}^2 -5.2\times 10^2 \eta_B +7.7$ |
|$C(\eta_B) \approx -2.2\times 10^4 {\eta_B}^2 +3.7\times 10^2 \eta_B -11$|