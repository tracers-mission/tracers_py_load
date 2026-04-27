# tracers_py_load
This is a repository containing functions that pull and plot data for the TRACERS' instrument suite. There are also routines to obtain ephemeris and attitude data.

The structure of this repository is relatively simple. Within the "lib" folder, there are subfolders for each instrument, as well as a "general" folder that contains miscellaneous routines.

Questions? Email sarah-a-henderson@uiowa.edu

## Instruments
### ACE
The Analyzer for Cusp Electrons (ACE) is an electrostatic analyzer with a field of view of 210 x 7 degrees that can measure electrons with energies spanning 20 - 13,500 eV [(Halekas et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01147-9). Within the region of interest (ROI), ACE operates at a cadence of 50 ms. In back orbit (BOR), this sampling is reduced to 6.4 s.

ACE has two scientific data products: Level 2 and Level 3. Level 2 data are the raw counts, background counts, and differential energy fluxes measured by ACE's 21 discrete anodes and 49 calibrated energy steps within BOR and ROI. Each anode has 10 degree resolution, and each energy channel exhibits 19% intrinsic resolution. Level 3 products are pitch angle distributions derived from ACE L2 and Magnetometer (MAG) L1B data and are subdivided into 18 pitch angle bins and 49 calibrated energy steps. Pitch angles span 0 - 180 degrees and exhibit 10 degree resolution.

**Note**: ACE-1 is not fully commissioned and has extremely sparse measurements in the southern cusp. ACE-2 is fully commissioned and has been operative for the duration of the TRACERS mission in both BOR and ROI periods.

### ACI
The Analyzer for Cusp Ions (ACI) is a toroidal tophat electrostatic analyzer with a field of view of 360 x 6 degrees that measures ions with energies spanning ~8 - 20,000 eV [(Fuselier et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01154-w). ACI collects data every 312 ms in ROI and every ~40 s in BOR. 

ACI currently only has Level 2 products, which are similar to those of ACE. Counts and differential energy fluxes are reported for each of ACI's 16 discrete anodes over 47 energy steps. Each anode has a resolution of 22.5 degrees, and each energy step has an intrinsic resolution of ~10%.

**Note**: ACI-1 has been in operation in the southern cusp since November 2025 and only turns on for ROI collection. ACI-2 has been in operation throughout the duration of the mission and is fully operative throughout TRACERS-2's orbit.

### EFI
The Electric Fields Instrument (EFI) comprises four spherical sensors mounted on orthogonal 3-m long stacer booms and provide a 7-m sensor-to-sensor separation on each spacecraft. Two of the four stacer booms form a dipole antenna with a separation of 4-m (stacer center to stacer center) and are used for the 10 kHz to 10 MHz snapshot E-field measurements [(Bonnell et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01202-5). EFI provides perpendicular components of the DC electric field, 2D E-field observations up to 1 kHz, and 1D E-field snapshot observations up to 10 MHz.

**Note**: EFI-1 has been in full operation since December 18, 2025 taking electric field measurements in ROI mode in the southern cusp. EFI-2 has been operational for the duration of the mission in both ROI and BOR modes.

### MAG
The Magnetometer (MAG) is a triaxial fluxgate magnetometer capable of measuring magnetic fields within the near-Earth environment spanning ±60,000 nT with a resolution of ∼9 pT [(Strangeway et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01212-3).

**Note**: MAG-1 has been in operation since late January 2026, and MAG-2 has been operating for the duration of the mission.

### MAGIC
The MAGnetometers for Innovation and Capability (MAGIC) is a triaxial fluxgate magnetometer onboard the TRACERS spacecraft with the primary objective as a technology demonstration [(Miles et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01191-5). MAGIC measures DC vector magnetic fields every 0.0078 s with 10 nT resolution. 

**Note**: MAGIC-1 was operated for a short period at the beginning of TRACERS-1 commissioning (September 24, 2025) and was subsequently turned off (December 16, 2025). MAGIC-2 has been in full operation on TRACERS-2 for the duration of the mission.

### MSC
The Magnetic Search Coil (MSC) onboard each TRACERS spacecraft provides three magnetic components of waves from ∼1 Hz to 1 kHz [(Hospodarsky et al., 2025)](https://link.springer.com/article/10.1007/s11214-025-01200-7). MSC has a sensitivity of 	
∼10<sup>−6</sup> nT<sup>2</sup>/Hz @ 10 Hz and 
∼10<sup>−8</sup> nT<sup>2</sup>/Hz @100 Hz and samples at a cadence of 16 Hz in ROI.

**Note**: MSC-1 has been in nominal operation since February 3, 2026. MSC-2 has operated for the duration of the mission.


## Other 
There are other functions within this repository that are useful for analyzing the above data products, as well as determining positional information about the spacecraft at a given time.

Ephemeris and attitude data (EAD) can also be found on the TRACERS team portal and are labelled as EAD files. These contain numerous parameters giving the attitude and position of the TRACERS spacecraft in different coordinate systems.


## Notebook 
There's a Jupyter notebook that outlines the basic calling routines for ACI, ACE, MAGIC, MSC, EFI, and EAD files. For plotting the data, all specific keywords are documented in each plotting routine file. Later entries will be added as capabilities change.
