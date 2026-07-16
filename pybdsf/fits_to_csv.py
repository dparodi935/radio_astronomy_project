from astropy.table import Table
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) #returns folder that this script is in
fits_path = os.path.join(script_dir,'..','..','lofar_downloads')
catalogue_name  = 'facet_5_catalogue_offical'

cat = Table.read(os.path.join(fits_path,f"{catalogue_name}.fits"), format="fits")
cat.write(os.path.join(fits_path, f"{catalogue_name}_csv.csv"), format="ascii.csv", overwrite=True)