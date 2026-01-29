from astropy.io import fits
from pathlib import Path

src = fits.getheader("new-image.fits")
aligned_dir = Path("cal_phot/aligned")

for p in aligned_dir.glob("*.fits"):
    with fits.open(p, mode="update", memmap=False) as hdul:
        hdr = hdul[0].header
        for k in ["CD1_1","CD1_2","CD2_1","CD2_2",
                  "CTYPE1","CTYPE2","CRPIX1","CRPIX2","CRVAL1","CRVAL2",
                  "CUNIT1","CUNIT2","RADESYS","EQUINOX"]:
            if k in src:
                hdr[k] = src[k]
        hdr["WCSORIG"] = ("astrometry.net", "forced CD copy from new-image.fits")
print("done")
