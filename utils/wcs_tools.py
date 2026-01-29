from __future__ import annotations
from astropy.wcs import WCS, FITSFixedWarning
from astropy.coordinates import SkyCoord
import astropy.units as u
import warnings

def skycoord_to_pixel(header, ra_deg: float, dec_deg: float):
    with warnings.catch_warnings():
        # Ignore a warning on using DATE-OBS in place of MJD-OBS
        warnings.filterwarnings('ignore', message="'datfix' made the change",category=FITSFixedWarning)
        w = WCS(header)
    if not w.has_celestial:
        raise ValueError("Header has no celestial WCS (missing RA/Dec WCS keywords).")
    wc = w.celestial
    sc = SkyCoord(ra=ra_deg*u.deg, dec=dec_deg*u.deg, frame="icrs")
    x, y = wc.world_to_pixel(sc)
    return float(x), float(y)
