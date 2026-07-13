from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
from astropy.table import Table
from astropy.wcs import WCS
from astropy.io import fits
import os
import matplotlib.pyplot as plt

#create filepath of fits file
fits_filename = "facet_19"
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
fits_folder_path = os.path.join(script_dir,"..","..","lofar_downloads")
fits_filepath = os.path.join(fits_folder_path,f"{fits_filename}.fits")

#open and extract data
fits_file = fits.open(fits_filepath)
data = fits_file[0].data
fits_file.close()

coord_system = WCS(fits_file[0].header).celestial

#open PyBDSF catalogue and create Table
catalogue_filename = f"{fits_filename}_sources"
catalogue_filepath = os.path.join(fits_folder_path,f"{catalogue_filename}.fits")
catalogue = Table.read(catalogue_filepath, format="fits")

ra_list = catalogue["RA"]
dec_list = catalogue["DEC"]

number = 10 #len(ra) - number of sources to cycle through

#cycles through every source and plots the cutout
for i in range(number):
    coords = SkyCoord(ra_list[i], dec_list[i], unit="deg", frame="icrs") 
    pixel_pos = coord_system.world_to_pixel(coords)
    size = 40
    cutout = Cutout2D(data, pixel_pos, size)
    
    plt.imshow(cutout.data)
    plt.show()