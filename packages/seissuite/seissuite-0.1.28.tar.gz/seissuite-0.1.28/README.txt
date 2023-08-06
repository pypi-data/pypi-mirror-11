SeisSuite
========================
This project is dedicated to provide a Python framework for seismic noise tomography, 
based on [ObsPy](https://github.com/obspy/obspy/wiki) and numerical Python packages 
such as [numpy](http://www.numpy.org/) and [scipy](http://www.scipy.org/).

Requirements
------------
The code is developped and tested on Ubuntu (but should run on other platforms as well)
with Python 2.7.

In addition to [Python 2.7](https://www.python.org/download/releases/2.7/), you need
to install the following packages:

- [numpy](http://www.numpy.org/) >= 1.8.2
- [scipy](http://www.scipy.org/) >= 0.13.3
- [matplotlib](http://matplotlib.org/) >= 1.3.1
- [ObsPy](https://github.com/obspy/obspy/wiki) >= 0.9.2
- [pyshp](https://github.com/GeospatialPython/pyshp)
- [pyproj](https://code.google.com/p/pyproj/) >= 1.8.9
- [pyPdf](http://pybrary.net/pyPdf/)


It is recommended to install these packages with `pip install ...` or with your
favourite package manager, e.g., `apt-get install ...`.

Optionally, you may want to install: 
- [Computer Programs in Seismology](http://www.eas.slu.edu/eqc/eqccps.html) 
  to be able to invert your dispersion maps for a 1-D shear velocity model,
  as these programs take care of the forward modelling.

- [waveloc](https://github.com/amaggi/waveloc)
  to be able to run the kurtosis and migration-based event detector and locator,
  this would enable for an automated removal of earthquake events.

- [nonlinloc](http://alomax.free.fr/nlloc/)
  to be able to run the non-linear event detection algorithms for waveloc
  and other detection programmes. 

How to start
------------
If you are reading this, then you have either directly downloaded the tar ball or 
cloned this project from github.com/boland1992/SeisSuite/ 
In both cases, now you should cd into the SeisSuite directory and run the following
line in the terminal:

>>> python setup.py install 

This should successfully install all of the module package files required for seissuite. 
If you wish to check for a successful installation, run this line in any python shell 
that is correctly linked to your PYTHONPATH: 

>>> import seissuite

If no errors occur, then the installation has been successful. 

Next, you should start reading the example configuration file contained in:

./bin/config_example.cnf 

which contains global parameters and detailed instructions. You should then create 
your own configuration file (any name with cnf extension, \*.cnf) with your
own parameters, and place it in the same folder as the scripts. It is not advised
to simply modify `./bin/config_example.cnf`, as any update may revert your changes.

You may then process in recommended order (items and tools from the seissuite module can
be used independently of these scripts to create your own application if necessary):

- `00_setup.py` sets up the initial required file structure for the applications.

AFTER THE FILE STRUCTURE HAS BEEN INITIALISED IT IS RECOMMENDED THAT YOU THEN PLACE YOUR
MSEED RAW WAVEFORMS FILES IN THE ./INPUT/DATA FOLDER AND THE ASSOCIATED METADATA IN THE
./INPUT/XML OR THE ./INPUT/DATALESS FOLDERS. 

- `01_database_init.py` sets up the initial databases required for finding files and
general processing. It requires MSEED files to be in the ./INPUT/DATA folder, and metadata
to be in either the ./INPUT/XML or the ./INPUT/DATALESS folders. 

- `02_timeseries_process.py` takes seismic waveforms as input in order to first
preprocess the waveforms and then and export cross-correlations between 
pairs of stations,

- `03_dispersion_curves.py` takes cross-correlations as input and applies
a frequency-time analysis (FTAN) in order to extract and export group velocity
dispersion curves,

- `04_tomo_inversion_testparams.py` takes dispersion curves as input and applies
 a tomographic inversion to produce dispersion maps; the inversion parameters
 are systematically varied within user-defined ranges,

- `05_tomo_inversion_2pass.py` takes dispersion curves as input and applies
 a two-pass tomographic inversion to produce dispersion maps: an overdamped
 inversion is performed in the first pass in order to detect and reject outliers
 from the second pass.
 
- `06_1d_models.py` takes dispersion maps as input and invert them for a 1-D
  shear velocity model at selected locations, using a Markov chain Monte Carlo
  method to sample to posterior distribution of the model's parameters.
 
The scripts rely on the Python package `pysismo`, which must thus be located
in a place included in your PATH (or PYTHONPATH) environment variable. The easiest
choice is of course to place it in the same folder as the scripts.

How to update
-------------
The code is still experimental so you should regularly check for (and pull) 
updates. These will be backward-compatible, **except if new parameters appear 
in the configuration file**.

**In other words, after any update, you should check whether new parameters were added
to the example configuration file (`tomo_Brazil.cnf`) and insert them accordingly
to your own configuration file.**

References
----------
The cross-correlation procedure of ambient noise between pairs of stations follows
the steps advocated by Bensen et al. (2007). 
The measurement of dispersion curves is based on the frequency-time
analysis (FTAN) with phase-matched filtering described in Levshin and Ritzwoller (2001) 
and Bensen et al. (2007).
The tomographic inversion implements the linear inversion procedure 
with norm penalization and spatial smoothing of Barmin et al. (2001).
The Markov chain Monte Carlo method is described by Mosegaard and Tarantola (1995), 
and the forward modelling is taken care of by the Computer Programs in Seimology 
(Herrmann, 2013).

- Barmin, M. P., Ritzwoller, M. H. and Levshin, A. L. (2001). 
A fast and reliable method for surface wave tomography. 
*Pure Appl. Geophys.*, **158**, p. 1351–1375. doi:10.1007/PL00001225
\[[journal](http://link.springer.com/article/10.1007%2FPL00001225)\]
\[[pdf](http://jspc-www.colorado.edu/pubs/2001/1.pdf)\]

- Bensen, G. D. et al. (2007). Processing seismic ambient noise data to obtain 
reliable broad-band surface wave dispersion measurements. 
*Geophys. J. Int.*, **169**(3), p. 1239–1260. doi:10.1111/j.1365-246X.2007.03374.x
\[[journal](http://onlinelibrary.wiley.com/doi/10.1111/j.1365-246X.2007.03374.x/abstract)\]
\[[pdf](http://ciei.colorado.edu/pubs/2007/2.pdf)\]

- Herrmann, R. B., 2013. Computer Programs in Seismology: an evolving tool for 
instruction and research, *Seismol. Res. Let.*, **84**(6), p. 1081-1088
doi: 10.1785/0220110096
\[[pdf](http://srl.geoscienceworld.org/content/84/6/1081.full.pdf+html)\]
- Levshin, A. L. and Ritzwoller, M. H. (2001). Automated detection, extraction, 
and measurement of regional surface waves. *Pure Appl. Geophys.*, **158**, 
p. 1531–1545. doi:10.1007/PL00001233
\[[journal](http://link.springer.com/chapter/10.1007%2F978-3-0348-8264-4_11)\]
\[[pdf](http://ciei.colorado.edu/pubs/pageoph_01/Levshin_Ritzwoller_pag2001.pdf)\]

- Mosegaard, K. and Tarantola, A. (1995) Monte Carlo sampling of solutions to inverse
problems, *J. Geophys. Res.*, **100**(B7), p. 12431–12447
\[[journal](http://onlinelibrary.wiley.com/doi/10.1029/94JB03097/abstract)\]
\[[pdf](http://www.ipgp.fr/~tarantola/Files/Professional/Papers_PDF/MonteCarlo_latex.pdf)\]

- Langet N. et al (2014). Continuous Kurtosis-Based Migration for Seismic Event Detection and Location,
 with Application to Piton de la Fournaise Volcano, La Réunion.
* Bul. Seis. Soc. Am.*, **104**, p. 229-246. doi:10.1785/0120130107


