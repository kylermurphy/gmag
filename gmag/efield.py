# -*- coding: utf-8 -*-
"""
Routines for deriving induced electric fields from ground-based
magnetomtere data

Routines were simplified from Bezpy to work with generic or
somewhat generic magnetometer data.

https://github.com/greglucas/bezpy

Copyright (c) 2017 Greg Lucas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd

import gmag

def calcZ(resistivities: npt.ArrayLike | list,
          thicknesses: npt.ArrayLike | list,
          freqs: npt.ArrayLike | list,):
    """Return Derived 1-D Surface Impedence.

    Parameters
    ----------
    resistivities :Numpy Array Like | list
        Array or list of ground resistivities (Ohm-m).
    thicknesses : Numpy Array Like | list
        Array or list of thickness of each layer corresponding to resitivity array 
        in meters (m).
    freqs : Numpy Array Like | list
        Frequencies used in the derivation of the Surface Impdence. The frequencies are 
        defined by the time-series of the magnetic field data (1/s).

        
    The impedence calculation follows that outlined in
    http://www.nerc.com/comm/PC/Geomagnetic%20Disturbance%20Task%20Force%20GMDTF%202013/GIC%20Application%20Guide%202013_approved.pdf

    Similar derivations are found in:

    Nikitina, Trichtchenko, Boteler: Assessment of extreme values in geomagnetic and 
        geoelectric field variations for Canada https://doi.org/10.1002/2016SW001386
    Boteler and Pirjola: Electric field calculations for real-time space weather 
        alerting systems, https://doi.org/10.1093/gji/ggac104
    Trichtchenko, Fernberg, Boteler: One-dimensional Layered Earth Models of Canada 
        for GIC Applications, https://doi.org/10.4095/314804
    Trichtchenko, Fernberg, Danskin: Geoelectric Field Modelling  for Canadian Space 
        Weather Services, https://doi.org/10.4095/299116

    Returns
    -------
    Numpy Array
        1-D Surface impedence tensor/matrix.
        To be applied to a mangetic field measured in nT. 

        The correction factor (1.0e-3 / MU) applied to Z converts
        H -> B and in the derivation of E returns mV/km
    """    

    # pylint: disable=invalid-name
    MU = 4 * np.pi * 1e-7  # Magnetic Permeability (H/m)
    freqs = np.asarray(freqs)
    resistivities = resistivities
    thicknesses = thicknesses

    n = len(resistivities)
    nfreq = len(freqs)

    omega = 2 * np.pi * freqs
    complex_factor = 1j * omega * MU

    # eq. 5
    k = np.sqrt(1j * omega[np.newaxis, :] * MU / resistivities[:, np.newaxis])

    # eq. 6
    Z = np.zeros(shape=(n, nfreq), dtype=complex)
    # DC frequency produces divide by zero errors
    with np.errstate(divide="ignore", invalid="ignore"):
        Z[-1, :] = complex_factor / k[-1, :]

        # eq. 7 (reflection coefficient at interface)
        r = np.zeros(shape=(n, nfreq), dtype=complex)

        for i in range(n - 2, -1, -1):
            r[i, :] = (1 - k[i, :] * Z[i + 1, :] / complex_factor) / (
                1 + k[i, :] * Z[i + 1, :] / complex_factor
            )
            Z[i, :] = (
                complex_factor
                * (1 - r[i, :] * np.exp(-2 * k[i, :] * thicknesses[i]))
                / (k[i, :] * (1 + r[i, :] * np.exp(-2 * k[i, :] * thicknesses[i])))
            )

    # Fill in the DC impedance as zero
    if freqs[0] == 0.0:
        Z[:, 0] = 0.0

    # Return a 3d impedance [0, Z; -Z, 0]
    Z_output = np.zeros(shape=(4, nfreq), dtype=complex)
    # Only return the top layer impedance
    # Z_factor is conversion from H->B, 1.e-3/MU
    Z_output[1, :] = Z[0, :] * (1.0e-3 / MU)
    Z_output[2, :] = -Z_output[1, :]

    return Z_output

def calcE(mag_x: npt.ArrayLike, 
          mag_y: npt.ArrayLike, 
          resistivities: npt.ArrayLike | list,
          thicknesses: npt.ArrayLike | list,
          dt=60):
    """Conlve B with Z to derive E.

    Parameters
    ----------
    mag_x : Numpy Array Like
        North-South magnetic field (nT).
    mag_y : Numpy Array Like
        East-West magnetic field (nT).
    resistivities : Numpy Array Like or list
        Array or list of ground resistivities (Ohm-m).
    thicknesses : Numpy Array Like or list
        Array or list of thickness of each layer corresponding to resitivity array 
        in meters (m).
    dt : int, optional
        Temporal resolution of the magnetic field in seconds, by default 60 (s).

    Returns
    -------
    Numpy array
        North-South and East-West induced electric field
    """    
    # pylint: disable=invalid-name

    # Note that I use rfft, because the input is real-valued. This eliminates
    # the need to calculate complex conjugates of negative frequencies.
    # To utilize normal fft you can do the following:
    #   mag_x_fft_c = np.fft.fft(mag_x, n=N)
    #   freqs_c = np.fft.fftfreq(N, d=dt)
    #   neg_freqs = freqs_c < 0.
    #   Z_c = self.calcZ(np.abs(freqs_c))
    #   Z_c[:,neg_freqs] = np.conj(Z_c[:,neg_freqs])
    #   Ex_t = np.real(np.fft.ifft(Z_c[0,:]*mag_x_fft_c)) ...
    # That produces the same results, accounting for complex conjugates of
    # the impedances at negative frequencies.

    N0 = len(mag_x)
    # Can round N to the next highest power of 2 (+1 (makes it 2) to prevent 
    # circular convolution, but most other studies/code to not do this
    # N = 2**(int(np.log2(N0))+2)
    N = N0

    freqs = np.fft.rfftfreq(N, d=dt)
    # Z needs to be organized as: xx, xy, yx, yy
    Z_interp = calcZ(resistivities, thicknesses, freqs)

    mag_x_fft = np.fft.rfft(mag_x, n=N)
    mag_y_fft = np.fft.rfft(mag_y, n=N)

    Ex_fft = Z_interp[0, :]*mag_x_fft + Z_interp[1, :]*mag_y_fft
    Ey_fft = Z_interp[2, :]*mag_x_fft + Z_interp[3, :]*mag_y_fft

    Ex_t = np.real(np.fft.irfft(Ex_fft)[:N0])
    Ey_t = np.real(np.fft.irfft(Ey_fft)[:N0])

    return Ex_t, Ey_t

def read_res(stn: str):
    """Magntometer station resistivity profile

    Parameters
    ----------
    stn : str
        Ground Magnetometer station profile to load.
        Files are located in /gmag/stations/

    Returns
    -------
    Pandas DataFrame
        Containing the resitivity profile for the magnetometer station
    """
    res_filename = f'res_model_{stn}.txt'

    # Get location of Earth Resistivity Model Files
    home_dir = Path.home()
    res_file_1 = home_dir / '.gmag' / 'Stations' / res_filename

    module_dir = Path(gmag.__file__)
    res_file_2 = module_dir / '..' / 'Stations' / res_filename
    res_file_2 = res_file_2.resolve()

    # Configuration file for running notebooks on colab 
    res_file_3 = home_dir / 'Stations' / res_filename

    for f in [res_file_1, res_file_2, res_file_3]:
        if f.is_file():
            return pd.read_csv(str(f),comment='#')

    return -1