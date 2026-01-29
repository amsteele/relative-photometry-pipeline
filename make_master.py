import numpy as np
import shutil
import os
import config_photometry as cfphot
from astropy.io import fits
from pathlib import Path
from typing import List, Tuple
import datetime as dt
from utils_fits import list_files,get_exptime
from utils_combine import sigma_clip_median, normalize_by_median
from photutils.aperture import CircularAperture,CircularAnnulus,Aperture,aperture_photometry
from photutils.background import MedianBackground,StdBackgroundRMS
from photutils.detection import DAOStarFinder
from matplotlib.dates import date2num, DateFormatter
from astropy.stats import median_absolute_deviation as mad
from astropy.stats import sigma_clipped_stats

# make master bias, flat, dark

def create_stack(paths: List[Path], crop=None):
	fits_dat=[]
	fits_hdr = []
	fhdr = None
	for p in paths:
		print(p)
		img = fits.open(p)
		if crop is not None:
			y0,y1,x0,x1 = crop
			fits_dat.append(img[0].data[y0:y1,x0:x1])
		else:
			fits_dat.append(img[0].data)
		if fhdr is None:
			fhdr = img[0].header
	stack = np.stack(fits_dat,axis=0)
	return stack,fhdr

out_directory_path = Path(cfphot.MASTER_DIR)

if out_directory_path.exists():
    shutil.rmtree(out_directory_path)

out_directory_path.mkdir(parents=True, exist_ok=False)

bias_files = list_files(cfphot.main_dir, cfphot.bias_files)
#dark_files = list_files(cfphot.main_dir, cfphot.dark_files)
flat_files = list_files(cfphot.main_dir, cfphot.flat_files)

print(f"Bias frames: {len(bias_files)}")
#print(f"Dark frames: {len(dark_files)}")
print(f"Flat frames: {len(flat_files)}")

bias_stack,bias_hdr = create_stack(bias_files,crop=cfphot.crop)
master_bias = sigma_clip_median(bias_stack,sigma=3.0,maxiters=5)
fits.writeto(cfphot.MASTER_DIR/"master_bias.fits",master_bias,header=bias_hdr,overwrite=True)
print('created master_bias.fits') 
print(np.where(master_bias==0))
 # --- Master flat (bias/dark corrected + normalized) ---
flat_stack, flat_hdr0 = create_stack(flat_files, crop=cfphot.crop)

flat_exptime = get_exptime(flat_hdr0, cfphot.EXPTIME_KEY)
#scale = float(flat_exptime / dark_exptime) if dark_exptime > 0 else 1.0
scale = 1.0

flat_corr = []
for i in range(flat_stack.shape[0]):
	img = flat_stack[i]
	img2 = (img - master_bias)# - (master_dark * scale)
	flat_corr.append(img2)

master_flat_raw = sigma_clip_median(np.stack(flat_corr, axis=0), sigma=3.0, maxiters=5)
master_flat = normalize_by_median(master_flat_raw)
fits.writeto(cfphot.MASTER_DIR / "master_flat.fits", master_flat, header=flat_hdr0,overwrite=True)

print("Wrote master_flat.fits")
print(np.where(master_flat==0))
print("Done.")
