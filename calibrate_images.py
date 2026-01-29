from __future__ import annotations
from pathlib import Path
from astropy.io import fits
import numpy as np
import shutil
import config_photometry as cfphot
from utils_fits import list_files, read_image_and_header, write_fits, get_exptime, apply_crop

def main():
    if cfphot.CALIB_DIR.exists():
        shutil.rmtree(cfphot.CALIB_DIR)

    cfphot.CALIB_DIR.mkdir(parents=True, exist_ok=False)

    sci_files = list_files(cfphot.main_dir, cfphot.sci_files)

    master_bias, bias_hdr = read_image_and_header(cfphot.MASTER_DIR / "master_bias.fits")
    master_flat, flat_hdr = read_image_and_header(cfphot.MASTER_DIR / "master_flat.fits")
    
    print(f"Science frames: {len(sci_files)}")

    for i,p in enumerate(sci_files, start=1):
        data,hdr = read_image_and_header(p)
        data = apply_crop(data, cfphot.crop)

        expt = get_exptime(hdr, cfphot.EXPTIME_KEY)
        #dark_scale = float(expt / md_expt) if md_expt > 0 else 1.0

        # Calibration: (raw - bias - scaled_dark) / flat
        # OR Calibration: (raw - bias) / flat
        #cal = (data - master_bias) - (master_dark * dark_scale)
        cal = (data - master_bias) 
        cal = cal / master_flat

        out = cfphot.CALIB_DIR / p.name.replace(".fits", "_cal.fits")
        write_fits(out, cal, header=hdr)
        if i % 25 == 0 or i == 1 or i == len(sci_files):
            print(f"{i:4d}/{len(sci_files)}  {out}")
    print("Done.")

if __name__ == "__main__":
    main()
