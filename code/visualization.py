import pyvista as pv
from parameters import *
from BxC import B, j ## comment this if you already have B and j saved


## Create meshes for B and j
Bmesh = pv.ImageData(dimensions=(N, N, N), spacing=(1, 1, 1), origin=(0, 0, 0))
vectors = np.empty((Bmesh.n_points, 3))
vectors[:, 0] = B[0].flatten(order="F")
vectors[:, 1] = B[1].flatten(order="F")
vectors[:, 2] = B[2].flatten(order="F")
Bmesh['vectors'] = vectors
del(vectors)

jmesh = pv.ImageData(dimensions=(N, N, N), spacing=(1, 1, 1), origin=(0, 0, 0))
vectors = np.empty((jmesh.n_points, 3))
vectors[:, 0] = j[0].flatten(order="F")
vectors[:, 1] = j[1].flatten(order="F")
vectors[:, 2] = j[2].flatten(order="F")
jmesh['vectors'] = vectors
del(vectors)

## Define plotter parameters
Bsargs = dict(
    height = 0.05,
    width = 0.9,
    position_x=0.05, 
    position_y=0.9,
    title_font_size=20,
    label_font_size=15,
    n_labels=5,
    italic=False,
    fmt="%.1f",
    font_family="times",
    color = "black", 
    title = "|B|"
)


jsargs = dict(
    height = 0.05,
    width = 0.9,
    position_x=0.05, 
    position_y=0.9,
    title_font_size=20,
    label_font_size=15,
    n_labels=5,
    italic=False,
    fmt="%.1f",
    font_family="times",
    color = "black",  
    title = "|j|"
)


""" Create the plotter for 3D viaulization of the fields """
## magnetic field
plotter = pv.Plotter(window_size = (600, 700), lighting='three lights') #, off_screen = True)
plotter.add_mesh(Bmesh, clim=[0, 0.8], scalar_bar_args=Bsargs, show_scalar_bar=True)
plotter.enable_anti_aliasing()
plotter.add_axes(color = "black", x_color = "black", y_color = 'black', z_color = 'black')
# plotter.screenshot(filename='./Bnorm.png', transparent_background=False, return_img=False, window_size=(500, 500), scale=6)
plotter.show()

## current density
plotter = pv.Plotter(window_size = (600, 700), lighting='three lights') #, off_screen = True)
plotter.add_mesh(jmesh, clim=[0, 0.8], scalar_bar_args=jsargs, show_scalar_bar=True)
plotter.enable_anti_aliasing()
plotter.add_axes(color = "black", x_color = "black", y_color = 'black', z_color = 'black')
# plotter.screenshot(filename='./jnorm.png', transparent_background=False, return_img=False, window_size=(500, 500), scale=6)
plotter.show()


""" Create the plotter for the visualization of the contours """
## magnetic field
Bcont = Bmesh.contour([0.1, 0.2, 0.3, 0.5, 0.7, 0.8]) ## Contour levels
plotter = pv.Plotter(window_size = (600, 700), lighting='three lights')
plotter.add_mesh(Bcont, clim = [0, 0.8], scalar_bar_args=Bsargs)
# plotter.screenshot(filename='contoursB.png',  transparent_background=False, return_img=False, window_size=(500, 500), scale=8)
plotter.show()

## current density
jcont = jmesh.contour([0.1, 0.2, 0.3, 0.5, 0.7, 0.8]) ## Contour levels
plotter = pv.Plotter(window_size = (600, 700), lighting='three lights')
plotter.add_mesh(jcont, clim = [0, 0.8], scalar_bar_args=jsargs)
# plotter.screenshot(filename='contoursB.png',  transparent_background=False, return_img=False, window_size=(500, 500), scale=8)
plotter.show()


""" Create the plotter for the visualization of streamlines """
## compute streamlines
Bsl = Bmesh.streamlines('vectors', return_source=False, n_points=25, source_radius=50)

## plot streamlines
plotter = pv.Plotter(window_size=(600, 700))
plotter.add_mesh(Bsl.tube(radius=1.5), clim=[0., 0.8], scalar_bar_args=Bsargs)
# plotter.screenshot(filename='./streamlines.png', transparent_background=False, return_img=False, window_size=(400, 700), scale=6)
plotter.show()
