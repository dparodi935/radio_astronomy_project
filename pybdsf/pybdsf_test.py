import bdsf
import os 

script_dir = os.path.dirname(os.path.abspath(__file__)) #returns folder that this script is in
fits_path = os.path.join(script_dir,'..','..','lofar_downloads')
fits_file = 'facet_19'

#creates catalog. thresh_pix and isl are the S/N ratios for the peaks and surrounding island respectively.
img = bdsf.process_image(os.path.join(fits_path,f'{fits_file}.fits'), thresh_pix=5.0, thresh_isl=4.0, ncores=2)

#adaptive rms box means the box used to measure noise shrinks near bright sources to capture the noise artefacts
img_adapt = bdsf.process_image(os.path.join(fits_path,f'{fits_file}.fits'), thresh_pix=5.0, thresh_isl=4.0,adaptive_rms_box=True,ncores=2)

#write catalogue file. clobber=True: existing files overwritten
img.write_catalog(outfile=os.path.join(fits_path,f'{fits_file}_sources.fits'), format='fits', clobber=True)
img_adapt.write_catalog(outfile=os.path.join(fits_path, f'{fits_file}_sources_adapt.fits'), format='fits', clobber=True)