from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy.io import fits
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from astropy.visualization import ImageNormalize, SinhStretch, ZScaleInterval

#create filepath of fits file
fits_filename = "facet_5"
script_dir = os.path.dirname(os.path.abspath(__file__))
fits_folder_path = os.path.join(script_dir,"..","..","lofar_downloads")
fits_filepath = os.path.join(fits_folder_path,f"{fits_filename}.fits")

#open and extract data
with fits.open(fits_filepath) as fits_file:
    data = fits_file[0].data
    coord_system = WCS(fits_file[0].header).celestial
    coord_scale = proj_plane_pixel_scales(coord_system)[1] #1 is chosen because pixels are square, and to avoid RA related issues

#open PyBDSF catalogue and create Table
catalogue_filename = f"{fits_filename}_catalogue_official" #f"{fits_filename}_sources"
catalogue_filepath = os.path.join(fits_folder_path,f"{catalogue_filename}.fits")
catalogue = Table.read(catalogue_filepath, format="fits")

#filter for interesting sources
catalogue = catalogue[(catalogue["S_Code" ] == "M") ]

#extract the columns I need
maj_list, min_list, pa_list = catalogue["Maj"], catalogue["Min"], catalogue["PA"]
ra_list, dec_list = catalogue["RA"], catalogue["DEC"]
cat_list = catalogue["Cat_id"]

number = len(ra_list)  #number of sources to cycle through
fig, ax = plt.subplots()
norm = ImageNormalize(data, interval=ZScaleInterval(), stretch=SinhStretch(a=0.1))

#cycles through every source and plots the cutout
for i in range(number):
    astronomical_pos = SkyCoord(ra_list[i], dec_list[i], unit="deg", frame="icrs")
    pixel_pos = coord_system.world_to_pixel(astronomical_pos)

    size = 80
    cutout = Cutout2D(data, pixel_pos, size)
            
    #set up image
    ax.imshow(cutout.data, origin="lower", norm=norm)
    
    #cutout_center accounts for the fact that the cutout can only cutoff at the pixel edges (so the sub-pixel position of the source will
    # not be centred)
    cutout_center = cutout.to_cutout_position(pixel_pos) 

    #draw ellipse
    gaussian = Ellipse(cutout_center, min_list[i]/coord_scale, maj_list[i]/coord_scale, angle=pa_list[i], fill=False, lw=2, zorder=10)
    ax.add_patch(gaussian)
    
    ax.set_title(cat_list[i])
    plt.draw()
    plt.waitforbuttonpress()
    ax.clear()

    #plt.show()