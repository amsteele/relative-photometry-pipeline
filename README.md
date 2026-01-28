# time-domain-photometry
Reproducible light-curve extraction from ground-based CCD imaging

## Relative Photometry Pipeline
A modular Python pipeline for extracting relative photometric light curves from ground-based CCD time-series observations.

## Overview
This repository contains a workflow for:
- CCD calibration, bias / flat (/dark)  correction
- image alignment
- WCS-based source localization
- relative aperture photometry using multiple reference stars
- light curve visualization and FITS output

The code was refactored from a previously validated research script with the goal of improving readability, modularity, and reproducibility while preserving
scientific correctness.

## Key Features
- Fixed-pixel photometry after image alignment
- Multi-reference relative flux normalization
- Robust handling of multiple observing nights
- Minimal assumptions and explicit configuration
- Designed for real (non-ideal) observational data

## Example Output
![Example light curve](wd1145_042017.gif)

(Animated GIFs are used during validation to inspect alignment and flux stability.)

## Usage
1. Configure targets and parameters in config_photometry.py
2. Organize your data directory
3. Run make_masters.py
4. Run calibrate_images.py
5. Run align_images.py
6. This code uses RA/Dec to identify target and reference stars and determine pixel positions. If you trust the WCS information in your data headers, go to step 7.

If not, go to astrometry.net, upload the first file from cal_phot/aligned, download the wcs.fits file and new-image.fits file, use them to overwrite values in the header by running fix_wcs.py. This will update the headers in cal_phot/aligned.
7. Run phot_lightcurve.py

## Notes
- The pipeline prioritizes reproducibility and validation over the abstract.
- World Coordinate System (WCS) information is used to establish pixel positions.
- Relative flux normalization matches established practice in time-domain astronomy.

## Dependencies
- Python
- numpy
- astropy
- photutils
- matplotlib
