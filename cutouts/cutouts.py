from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
from astropy.table import Table
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy.io import fits
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

#create filepath of fits file
fits_filename = "facet_19"
script_dir = os.path.dirname(os.path.abspath(__file__))
fits_folder_path = os.path.join(script_dir,"..","..","lofar_downloads")
fits_filepath = os.path.join(fits_folder_path,f"{fits_filename}.fits")

#open and extract data
with fits.open(fits_filepath) as fits_file:
    data = fits_file[0].data
    coord_system = WCS(fits_file[0].header).celestial
    coord_scale = proj_plane_pixel_scales(coord_system)[1] #1 is chosen because pixels are square, and to avoid RA related issues

#open PyBDSF catalogue and create Table
catalogue_filename = f"{fits_filename}_sources"
catalogue_filepath = os.path.join(fits_folder_path,f"{catalogue_filename}.fits")
catalogue = Table.read(catalogue_filepath, format="fits")

catalogue = catalogue[(catalogue["S_Code" ] == "M") & (catalogue["Peak_flux" ] > 0.005)]
maj_list, min_list, pa_list = catalogue["Maj_img_plane"], catalogue["Min_img_plane"], catalogue["PA_img_plane"]
xposn_list, yposn_list = catalogue["Xposn"], catalogue["Yposn"]

number = 5 #len(ra) - number of sources to cycle through

#cycles through every source and plots the cutout
for i in range(number):
    pixel_pos = (xposn_list[i], yposn_list[i])
    size = 40
    cutout = Cutout2D(data, pixel_pos, size)
    
    # Previous coord method:
    #coords = SkyCoord(ra_list[i], dec_list[i], unit="deg", frame="icrs")
    #pixel_pos = coord_system.world_to_pixel(coords)
    
    #set up image
    fig, ax = plt.subplots()
    ax.imshow(cutout.data, origin="lower")
    
    #cutout_center accounts for the fact that the cutout can only cutoff at the pixel edges (so the sub-pixel position of the source will
    # not be centred)
    cutout_center = cutout.to_cutout_position(pixel_pos) 

    #draw ellipse
    gaussian = Ellipse(cutout_center, min_list[i]/coord_scale, maj_list[i]/coord_scale, angle=pa_list[i], fill=False, lw=2, zorder=10)
    ax.add_patch(gaussian)
    
    plt.show()