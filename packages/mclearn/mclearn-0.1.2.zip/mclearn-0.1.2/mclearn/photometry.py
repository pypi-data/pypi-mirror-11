""" Procedures specific to photometric data. """

import os
import numpy as np
from urllib.request import urlopen

def reddening_correction_sfd98(extinction_r):
    """ Compute the reddening values using the SFD98 correction set.

        Parameters
        ----------
        extinction_r : array
            The uncorrected extinction values in the r-band.

        Returns
        -------
        A_u : array
            The corrected extinction values in the u-band.

        A_g : array
            The corrected extinction values in the g-band.

        A_r : array
            The corrected extinction values in the r-band.

        A_i : array
            The corrected extinction values in the i-band.

        A_z : array
            The corrected extinction values in the z-band.
    """

    E_BV = extinction_r / 2.751
    A_u = E_BV * 5.155
    A_g = E_BV * 3.793
    A_r = E_BV * 2.751
    A_i = E_BV * 2.086
    A_z = E_BV * 1.479

    return (A_u, A_g, A_r, A_i, A_z)


def reddening_correction_sf11(extinction_r):
    """ Compute the reddening values using the SF11 correction set.

        Parameters
        ----------
        extinction_r : array
            The uncorrected extinction values in the r-band.

        Returns
        -------
        A_u : array
            The corrected extinction values in the u-band.

        A_g : array
            The corrected extinction values in the g-band.

        A_r : array
            The corrected extinction values in the r-band.

        A_i : array
            The corrected extinction values in the i-band.

        A_z : array
            The corrected extinction values in the z-band.
    """

    E_BV = extinction_r / 2.751
    A_u = E_BV * 4.239
    A_g = E_BV * 3.303
    A_r = E_BV * 2.285
    A_i = E_BV * 1.698
    A_z = E_BV * 1.263

    return (A_u, A_g, A_r, A_i, A_z)

def reddening_correction_w14(extinction_r):
    """ Compute the reddening values using the W14 correction set.

        Parameters
        ----------
        extinction_r : array
            The uncorrected extinction values in the r-band.

        Returns
        -------
        A_u : array
            The corrected extinction values in the u-band.

        A_g : array
            The corrected extinction values in the g-band.

        A_r : array
            The corrected extinction values in the r-band.

        A_i : array
            The corrected extinction values in the i-band.

        A_z : array
            The corrected extinction values in the z-band.
    """

    E_BV = extinction_r / 2.751

    region_2 = np.logical_and(E_BV >= 0.04, E_BV < 0.08)
    region_3 = E_BV >= 0.08

    E_BV[region_2] = E_BV[region_2] + 0.5 * (E_BV[region_2] - 0.04)
    E_BV[region_3] = E_BV[region_3] + 0.02

    A_u = E_BV * 4.305
    A_g = E_BV * 3.288
    A_r = E_BV * 2.261
    A_i = E_BV * 1.714
    A_z = E_BV * 1.263

    return (A_u, A_g, A_r, A_i, A_z)


def correct_magnitudes(data, magnitudes, corrections, suffix):
    """ Correct the values of magntidues given a correction set.

        Parameters
        ----------
        data : DataFrame
            The DataFrame containing the magnitudes.

        magnitudes : array
            The column names of the magnitudes.

        corrections : array
            The set of correction values in the same order as `magnitudes`.
    """

    for mag, cor in zip(magnitudes, corrections):
        data[mag + suffix] = data[mag] - cor


def compute_colours(data, colours, suffix):
    """ Compute specified combinations of colours.

        Parameters
        ----------
        data : DataFrame
            The DataFrame containing the magnitudes.

        colours : array
            The list of colour combinations to be computed.

        suffix : array
            A suffix is added to the colour name to distinguish between correction sets.
    """
    
    for colour in colours:
        prefix = 'psf' if colour[0].startswith('psf') else 'petro'
        colour_name = prefix + colour[0][-2:] + colour[1][-2:]
        data[colour_name + suffix] = data[colour[0] + suffix] - data[colour[1] + suffix]




def fetch_filter(filter, download_url):
    """ Get a filter from the internet.

        Parameters
        ----------
        filter : char
            Name of the filters. Must be one of u, g, r, i, and z.

        download_url : str
            The URL where the filter can be downloaded.

        Returns
        -------
        data : array
            The downloaded filter data.

    """
    
    assert filter in 'ugriz'
    url = download_url % filter
    
    if not os.path.exists('data/filters'):
        os.makedirs('data/filters')

    loc = os.path.join('data/filters', '%s.dat' % filter)
    
    if not os.path.exists(loc):
        filter_file = urlopen(url)
        with open(loc, 'wb') as f:
            f.write(filter_file.read())

    with open(loc, 'rb') as f:
        data = np.loadtxt(f)

    return data



def fetch_spectrum(spectrum_url):
    """ Get a spectrum from the internet.

        Parameters
        ----------
        spectrum_url : str
            The URL where the spectrum can be downloaded.

        Returns
        -------
        data : array
            The downloaded spectrum data.
    """

    if not os.path.exists('data/spectra'):
        os.makedirs('data/spectra')

    refspec_file = os.path.join('data/spectra', spectrum_url.split('/')[-1])

    if not os.path.exists(refspec_file):
        spectrum_file = urlopen(spectrum_url)
        with open(refspec_file, 'wb') as f:
            f.write(spectrum_file.read())

    with open(refspec_file, 'rb') as f:
        data = np.loadtxt(f)
    
    return data


def clean_up_subclasses(classes, subclasses):
    """ Clean up the names of the subclasses in the SDSS dataset.

        Parameters
        ----------
        classes : array
            The array containing the classes. This will be prepended to the sublcasses.

        subclasses : array
            The array containing the subclasses.
    """

    # remove null references
    subclasses.replace('null', '', inplace=True)

    # remove HD catalog number (stored in brackets)
    subclasses.replace(r'\s*\(\d+\)\s*', '', regex=True, inplace=True)

    # captialise only the first leter of some subclasses
    subclasses.replace('BROADLINE', 'Broadline', inplace=True)
    subclasses.replace('STARFORMING', 'Starforming', inplace=True)
    subclasses.replace('STARBURST', 'Starburst', inplace=True)
    subclasses.replace('STARBURST BROADLINE', 'Starburst Broadline', inplace=True)
    subclasses.replace('AGN BROADLINE', 'AGN Broadline', inplace=True)
    subclasses.replace('STARFORMING BROADLINE', 'Starforming Broadline', inplace=True)

    # remove other brackets
    subclasses.replace('F8V (G_243-63)', 'F8V', inplace=True)
    subclasses.replace('K5 (G_19-24)', 'K5', inplace=True)
    subclasses.replace('sd:F0 (G_84-29)', 'sd:F0', inplace=True)
    subclasses.replace('G0 (G_101-29)', 'G0', inplace=True)
    subclasses.replace('A4 (G_165-39)', 'A4', inplace=True)
    subclasses.replace('A4p (G_37-26)', 'A4p', inplace=True)

    not_empty = subclasses != ''
    subclasses.loc[not_empty] = classes[not_empty] + ' ' + subclasses[not_empty] 


def optimise_sdss_features(sdss):
    """ Apply the SF11 reddening correction and compute key colours in the SDSS dataset.

        Parameters
        ----------
        sdss : DataFrame
            The DataFrame containing photometric features.
    """

    # compute the three sets of reddening correction
    A_u_sf11, A_g_sf11, A_r_sf11, A_i_sf11, A_z_sf11 = reddening_correction_sf11(sdss['extinction_r'])

    # useful variables
    psf_magnitudes = ['psfMag_u', 'psfMag_g', 'psfMag_r', 'psfMag_i', 'psfMag_z']
    petro_magnitudes = ['petroMag_u', 'petroMag_g', 'petroMag_r', 'petroMag_i', 'petroMag_z']
    sf11_corrections = [A_u_sf11, A_g_sf11, A_r_sf11, A_i_sf11, A_z_sf11]
    colours = [('psfMag_u', 'psfMag_g'), ('psfMag_g', 'psfMag_r'), ('psfMag_g', 'psfMag_i'),
               ('psfMag_r', 'psfMag_i'), ('psfMag_i', 'psfMag_z'), ('petroMag_i', 'petroMag_z')]

    # calculate the corrected magnitudes
    correct_magnitudes(sdss, psf_magnitudes, sf11_corrections, '_sf11')
    correct_magnitudes(sdss, petro_magnitudes, sf11_corrections, '_sf11')

    # calculate the corrected magnitudes
    compute_colours(sdss, colours, '_sf11')