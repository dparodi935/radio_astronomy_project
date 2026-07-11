import bdsf
import os 

#script_dir = os.path.dirname(os.path.abspath(__file__))
fits_path = os.path.join('..','lofar_downloads')
fits_file = 'facet_27'

#creates catalog. thresh_pix and isl are the S/N ratios for the peaks and surrounding island respectively.
img = bdsf.process_image(os.path.join(fits_path,f'{fits_file}.fits'), thresh_pix=5.0, thresh_isl=4.0)
#adaptive rms box means the box used to measure noise shrinks near bright sources to capture the noise artefacts
img_adapt = bdsf.process_image(os.path.join(fits_path,f'{fits_file}.fits'), thresh_pix=5.0, thresh_isl=4.0,adaptive_rms_box=True)

img.write_catalog(outfile=os.path.join(fits_path,f'{fits_file}_sources.reg'), format='ds9')
img_adapt.write_catalog(outfile=os.path.join(fits_path, f'{fits_file}_sources_adapt.reg'), format='ds9')